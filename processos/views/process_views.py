
from django.shortcuts import get_object_or_404,redirect,render,HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from processos import models
from .process_forms import ProcessForm
from.contract_forms import ContractForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView
from django.contrib import messages
from django.db.models import Q
from urllib.parse import urlencode
from django.utils.decorators import method_decorator#decoradores
from django.views.decorators.cache import never_cache# para nao deixar carregar cache
import os
from django.conf import settings
from django.http import Http404

from ..models import Processo

# Create your views here.

'''
posso por um filtro de show,=true, usando .filter no  lugar do .all e 
passando o valor =True
o index vai exibir os pedidos de cara e depois vai relacionar aos contratos e processos

tambem havera uma função de acesso direto aos processos, que vai listar  os contratos dentro de processos

e os pedidos dentro de contrato 
o context da a sinformaçoes para o template da seguinte maneira a chave  'pedido' por exemplo, indica ao template o que
ele deve ler, e o valor -variavel, o que sera lido.
'''



def login(request):
    return  HttpResponse('inicial')

def index(request):
    return  HttpResponse('index')

#PROCESSOS

class listarprocessos(ListView):
    model = models.Processo
    template_name = 'processos/processo.html'
    context_object_name = 'processos'
    paginate_by = 10

#combinar as duas formas de busca, uma para busca, e outra para ordenaçao
    def get_queryset(self):
        #aqui para a search
        queryset = models.Processo.objects.filter(show=True).order_by('-id')
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(numero_processo__icontains=search_query) |
                Q(numero_licitacao__icontains=search_query) |
                Q(contratante__icontains=search_query) |
                Q(modalidade__icontains=search_query)
            ).order_by('-id')
        # ordena do maior para o menor, atençao quando lançar a logica no template, o eroo
        # era Seu template usava -data_disputa, mas o backend esperava data_disputa_asc.
        sort_param = self.request.GET.get('sort', '')# self.request captura as informaçoes do template

        if sort_param =='data_disputa':
            queryset = queryset.order_by('-data_disputa')
        elif sort_param =='data_disputa_asc':
            queryset = queryset.order_by('data_disputa')


    #filtro por categoria do models
        modalidade=self.request.GET.get('modalidade', 'None')
        status = self.request.GET.get('status', 'None')
        tipo=self.request.GET.get('tipo', 'None')
        # para consultas dinamicas ,e refinadas somente if, e para fazer
        # de forma cumulativa de maneira a ir refinando as pesquisas, essa e uma forma ultil
        if modalidade  != 'None' and modalidade:
            queryset = queryset.filter(modalidade=modalidade)
        if status  != 'None' and status:
            queryset = queryset.filter(status=status)
        if tipo  != 'None'and tipo:
            queryset = queryset.filter(tipo=tipo)

        return queryset



# tem que fazer os 2 context, e get query set
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obter as modalidades disponíveis dinamicamente
        context['modalidades'] = models.Processo.objects.values_list('modalidade', flat=True).distinct()
        context['situacao'] = models.Processo.objects.values_list('status', flat=True).distinct()
        context['tipos'] = models.Processo.objects.values_list('tipo', flat=True).distinct()
        context['query_params']=self.request.GET.urlencode()# para links mais a frente, agora
        # nao estou pensando nisso

        return context
# para capturar os filtros atuais e ir adicionando novos ao contexto sem perder a pagina
    def post(self, request, *args, **kwargs):
        parametros=request.GET.copy()
        novofiltro=request.POST.get('novofiltro', 'NONE')
        if novofiltro:
            parametros['novofiltro']=novofiltro
        return redirect(f"{self.request.path}?{urlencode(parametros)}")




class DetalharProcesso(DetailView):
    model = models.Processo
    template_name = 'processos/process.html'
    context_object_name = 'processo'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contratos']=self.get_object().contratos.all()

        processo_nome=str(self.object.pk)
        caminho_base=os.path.join(settings.MEDIA_ROOT,f'processos/{processo_nome}')#cria o acesso  pasta de processos
        #aonde estao
        if not os.path.exists(caminho_base):
            context['arquivos']={}
        else:
            tipo_arquivos={}
            for subpasta in os.listdir(caminho_base):
                caminho_subpasta=os.path.join(caminho_base, subpasta)
                tipo_arquivos[subpasta]=os.listdir(caminho_subpasta)
            context['arquivos']=tipo_arquivos
        return context





class CriarProcesso(CreateView):
    model = models.Processo
    template_name = 'processos/criar_processo.html'
    form_class = ProcessForm
    success_url = reverse_lazy('processos:processo')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['create_process_form'] = context['form']
        return context

    def form_valid(self, create_process_form):
        response=super().form_valid(create_process_form)
        messages.success(self.request, 'Processo criado com sucesso!')
        return response

    def form_invalid(self, create_process_form):
        print('algo falhando aqui')
        print(create_process_form.errors)
        messages.warning(self.request, 'processo nao criado com sucesso!')
        return super().form_invalid(create_process_form)

class DeletarProcesso(View):
    def post(self, request, *args, **kwargs):
        processo=get_object_or_404(models.Processo, pk=kwargs['pk'])
        messages.warning(self.request, 'Processo excluido com sucesso!')
        print('deletei aqui')
        processo.delete()
        return redirect('processos:processo')

def delete_arquivos(request,pk):
    if request.method == 'POST':# muito mais facil fazer desse jeito para delete, meu Deus, quase acertei, dq pouco faço so
        processo_nome=str(pk)
        caminho_base=os.path.join(settings.MEDIA_ROOT,f'processos/{processo_nome}')
        arquivo_excluir=request.POST.get('arquivo')
        subpasta=request.POST.get('tipo')
        if arquivo_excluir and subpasta:
            caminho_subpasta=os.path.join(caminho_base, subpasta)
            caminho_arquivo_excluir=os.path.join(caminho_subpasta, arquivo_excluir)
            if os.path.exists(caminho_arquivo_excluir):
                try:
                    os.remove(caminho_arquivo_excluir)
                    messages.success(request, 'Arquivo excluido com sucesso!')
                except Exception as e:
                    print(f"Erro ao deletar o arquivo: {e}")
            else:
                print("Parâmetros inválidos enviados na requisição.")

        processo_deletado=DetalharProcesso()
        if processo_deletado:
            os.remove(caminho_base)
    return redirect('processos:detalhe',pk=pk)




@method_decorator(never_cache, name='dispatch')
class UpdateProcesso(UpdateView):
    model = models.Processo
    template_name = 'processos/att_processo.html'
    form_class = ProcessForm
    success_url = reverse_lazy('processos:processo')
    # e aprendemos com isso da pior forma possivel, que  era so trocar
    # de button para a, e resolvia o Bo inteiro
    #a solução mais simples e a melhor
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['att_process_form']=context['form']
        print(context['form'].initial)


        return context

    def form_valid(self, att_process_form):
        response = super().form_valid(att_process_form)
        print('estou aqui no valido')
        print(att_process_form.cleaned_data)
        messages.success(self.request, f'Processo { self.object.numero_processo} atualizado com sucesso')
        return response

    def form_invalid(self, att_process_form):
        response=super().form_invalid(att_process_form)
        print('estou aqui no invavalido')
        print(att_process_form.errors)
        messages.warning(self.request, f'Processo { self.object.numero_processo} nao pode ser atualizado')
        return response



#CONTRATOS
class listarcontratos(ListView):
    model=models.Contratos
    template_name = 'processos/contrato.html'
    context_object_name = 'contratos'

    def get_queryset(self):
        queryset = models.Contratos.objects.filter(show=True).order_by('-id')
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(numero_processo__icontains=search_query) |
                Q(numero_licitacao__icontains=search_query) |
                Q(contratante__icontains=search_query) |
                Q(modalidade__icontains=search_query)
            ).order_by('-id')
        return queryset

class DetalharContrato(DetailView):
    model = models.Contratos
    template_name = 'processos/contract.html'
    context_object_name = 'contrato'


#captura os pedidos para a pagina do contrato, os associando
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pedidos']=self.get_object().pedidos.all()
        return context

class Criarcontrato(CreateView):
    model = models.Contratos
    template_name = 'processos/criar_contrato.html'
    form_class =ContractForm
    success_url = reverse_lazy('processos:contrato')

    def get_initial(self):
        initial=super().get_initial()
        processo=get_object_or_404(models.Processo, pk=self.kwargs['pk'])
        print(f'{processo} pk do processo')
        initial['numero_processo']=processo.numero_processo
        return initial


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['create_contract_form'] = context['form']

        return context

    def form_valid(self, create_contract_form,):
        processo=get_object_or_404(models.Processo, pk=self.kwargs['pk'])
        contrato=create_contract_form.save()
        contrato.numero_processo=processo
        print('deu certo valid')
        contrato.save()
        messages.success(self.request, f'Contrato criado com sucesso')
        return redirect(self.get_success_url)

    def form_invalid(self, create_contract_form):
        response=super().form_invalid(create_contract_form)
        print('falhando aqui invalid')
        print(create_contract_form.errors)
        messages.warning(self.request, 'contrato nao criado com sucesso!')
        return  response








#PEDIDOS
class listarpedidos(ListView):
    model=models.Pedidos
    template_name = 'processos/pedidos.html'
    context_object_name = 'pedidos'

    def get_queryset(self):
        queryset = models.Pedidos.objects.filter(show=True).order_by('-id')
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(numero_processo__icontains=search_query) |
                Q(numero_licitacao__icontains=search_query) |
                Q(contratante__icontains=search_query) |
                Q(modalidade__icontains=search_query)
            ).order_by('-id')
        return queryset



class DetalharPedido(DetailView):
    model = models.Pedidos
    template_name = 'processos/order.html'
    context_object_name = 'pedido'

    def get_object(self, **kwargs):#talvez precisar retornar somente ao self, ja estava funcionando mesmo
        return get_object_or_404(models.Pedidos, id=self.kwargs['pk'])














