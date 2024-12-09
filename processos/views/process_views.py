
from django.shortcuts import get_object_or_404,redirect,render,HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from processos import models
from .process_forms import ProcessForm
from.contract_forms import ContractForm
from.pedido_forms import PedidoForms
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib import messages
from django.db.models import Q
from urllib.parse import urlencode
from django.utils.decorators import method_decorator#decoradores
from django.views.decorators.cache import never_cache# para nao deixar carregar cache
import os
from django.conf import settings
import shutil


# Create your views here.


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
        # era template usava -data_disputa, mas o backend esperava data_disputa_asc.
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
        #filtragem por  categorias em dropdown
        # Obter as modalidades disponíveis dinamicamente
        context['modalidades'] = models.Processo.objects.values_list('modalidade', flat=True).distinct()
        context['situacao'] = models.Processo.objects.values_list('status', flat=True).distinct()
        context['tipos'] = models.Processo.objects.values_list('tipo', flat=True).distinct()
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
        context['contratos']=self.get_object().contratos.all() # captura os contratos
        processo_nome=str(self.object.pk)
        print(processo_nome,'processo-pk do context data do processo')
        caminho_base=os.path.join(settings.MEDIA_ROOT,f'processos/{processo_nome}')
        #cria o acesso  pasta de processos#aonde estao
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
        # print('algo falhando aqui')
        # print(create_process_form.errors)
        messages.warning(self.request, 'processo nao criado com sucesso!')
        return super().form_invalid(create_process_form)

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
        #print(context['att_process_form'].initial)
        return context
    def form_valid(self, att_process_form):
        response = super().form_valid(att_process_form)
        #print('estou aqui no valido')
        print(att_process_form.cleaned_data)
        messages.success(self.request, f'Processo { self.object.numero_processo} atualizado com sucesso')
        return response
    def form_invalid(self, att_process_form):
        response=super().form_invalid(att_process_form)
        #print('estou aqui no invavalido')
        print(att_process_form.errors)
        messages.warning(self.request, f'Processo { self.object.numero_processo} nao pode ser atualizado')
        return response
class DeletarProcesso(View):
    def post(self, request, *args, **kwargs):
        processo=get_object_or_404(models.Processo, pk=kwargs['pk'])
        messages.warning(self.request, 'Processo excluido com sucesso!')
        processo_nome=processo.pk
        caminho_base = os.path.join(settings.MEDIA_ROOT, f'processos/{processo_nome}')
        processo.delete()#deletar o processo
        if os.path.exists(caminho_base):
            try:
                shutil.rmtree(caminho_base)
                messages.success(request, 'Processo excluido com sucesso!')
            except Exception as e:
                print(f"Erro ao deletar o arquivo: {e}")
        else:
            print("Parâmetros inválidos enviados na requisição.")

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
                    print(caminho_arquivo_excluir)
                except Exception as e:
                    print(f"Erro ao deletar o arquivo: {e}")
            else:
                print("Parâmetros inválidos enviados na requisição.")
    return redirect('processos:detalhe',pk=pk)



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
                Q(numero__icontains=search_query) |
                Q(objeto__icontains=search_query) |
                Q(contratante__icontains=search_query) |
                Q(processo__numero_processo__icontains=search_query)|
                #  quando for foreing por a variavel loca, pegando a que ela usa na foreigin
                Q(observacoes__icontains=search_query)
            ).order_by('-id')


#ordenação por multiplos fatores
        sort_param = self.request.GET.get('sort', '')  # self.request captura as informaçoes do template
        sort_options={
            'fim_contrato':'-fim_contrato',
            'fim_contrato_asc':'fim_contrato',
            'valor_total':'-valor_total',
            'valor_total_asc':'valor_total',
            'executado':'-executado',
            'executado_asc':'executado',
            'executavel':'-executavel',
            'executavel_asc':'executavel',
        }

        if sort_param in sort_options:
            queryset = queryset.order_by(sort_options[sort_param])
        # filtro por categoria do models
        seguro = self.request.GET.get('seguro', 'None')
        if seguro != 'None' and seguro:
            queryset = queryset.filter(seguro=seguro)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #filtragem por  categorias em dropdown
        # Obter as modalidades disponíveis dinamicamente
        context['seguros'] = models.Contratos.objects.values_list('seguro', flat=True).distinct()

        return context

class Criarcontrato(CreateView):
    model = models.Contratos
    template_name = 'processos/criar_contrato.html'
    form_class =ContractForm
    success_url = reverse_lazy('processos:listarcontratos')


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['create_contract_form'] = context['form']
        return context

    # def get_form_kwargs(self):
    #     kwargs=super().get_form_kwargs()
    #     pk_processo=self.kwargs.get('pk')
    #     processo=get_object_or_404(models.Processo, pk=pk_processo)
    #     kwargs['processo2']=processo
    #     return kwargs

    def form_valid(self, create_contract_form,):
        pk_processo=self.kwargs.get('pk')
        processo=get_object_or_404(models.Processo, pk=pk_processo)
        create_contract_form.instance.processo=processo
        if create_contract_form.is_valid():
            print(create_contract_form.cleaned_data)
            create_contract_form.save(commit=False)
            messages.success(self.request, f'Contrato criado com sucesso')
            return super().form_valid(create_contract_form)
        else:
            messages.error(self.request, f'Existem campos a serem preenchidos')

#numero_processo=self.kwargs['numero_processo']
    def form_invalid(self, create_contract_form):
        super().form_invalid(create_contract_form)
        print('falhando aqui invalid')
        print(create_contract_form.errors)
        response=super().form_invalid(create_contract_form)
        messages.warning(self.request, 'Contrato sendo gerado, preencha as informaçoes com cuidado!')
        return  response


class DetalharContrato(DetailView):
    model = models.Contratos
    template_name = 'processos/contract.html'
    context_object_name = 'contrato'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pedidos']=self.get_object().pedidos.all()#captura os pedidos para a pagina do contrato, os associando
        processo=self.get_object().processo
        processo_nome=str(processo.pk)
        print(processo_nome,'processo_nome no contrato no get context')
        contrato_nome=self.object.pk
        print(contrato_nome,'contrato_nome no get context')
        caminho_base_contratos = os.path.join(settings.MEDIA_ROOT, f'processos/{processo_nome}/contratos/{contrato_nome}')
        # cria o acesso  pasta de processos#aonde estao
        if not os.path.exists(caminho_base_contratos):
            context['arquivos_contrato'] = {}
        else:
            tipo_arquivos = {}
            for subpasta in os.listdir(caminho_base_contratos):
                caminho_subpasta = os.path.join(caminho_base_contratos, subpasta)
                tipo_arquivos[subpasta] = os.listdir(caminho_subpasta)
            context['arquivos'] = tipo_arquivos
            if self.request.method == 'POST':
                print(caminho_base_contratos)
        return context
class UpdateContrato(UpdateView):
    model = models.Contratos
    template_name = 'processos/att_contrato.html'
    form_class = ContractForm
    success_url = reverse_lazy('processos:listarcontratos')
    # e aprendemos com isso da pior forma possivel, que  era so trocar
    # de button para a, e resolvia o Bo inteiro
    #a solução mais simples e a melhor
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['att_contract_form']=context['form']
        return context
    def form_valid(self, att_contract_form):
        response = super().form_valid(att_contract_form)
        print('estou aqui no valido')
        processo_nome = str(self.request.GET.get('processo.pk'))
        print(processo_nome, 'processo')
        contrato_nome = str(self.request.GET.get('contrato.pk'))
        print(contrato_nome, 'contrato')
        print(att_contract_form.cleaned_data)
        messages.success(self.request, f'Contrato { self.object.numero} atualizado com sucesso')
        return response
    def form_invalid(self, att_process_form):
        response=super().form_invalid(att_process_form)
        print('estou aqui no invavalido')
        print(att_process_form.errors)
        messages.warning(self.request, f'Contrato { self.object.numero} nao pode ser atualizado')
        return response

#  aqui tentar fazer a logica do processo, mais extendida ao contrato, ele vai pegar so o  fim do caminho base
class Deletarcontrato(View):
    def post(self, request, *args, **kwargs):
        processo_pk=kwargs.get('processo_pk')# para pegar a pk da url,  kwargs.get
        contrato_pk=kwargs.get('pk')
        processo=get_object_or_404(models.Processo, pk=processo_pk)
        print(processo,'processo post deletecontratos')
        contrato=get_object_or_404(models.Contratos, pk=contrato_pk)
        print(contrato, 'processo post deletecontratos')
        processo_nome=str(processo.pk)
        contrato_nome=str(contrato.pk)
        caminho_base=os.path.join(settings.MEDIA_ROOT, f'processos/{processo_nome}/contratos/{contrato_nome}')
        if os.path.exists(caminho_base):
            try:
                contrato.delete()
                shutil.rmtree(caminho_base)
                messages.success(self.request, 'Contrato Excluido com Sucesso o!')  # deletar o processo
            except Exception as e:
                print(f"Erro ao deletar o arquivo: {e}")
            else:
                print("Parâmetros inválidos enviados na requisição.")
        return redirect('processos:listarcontratos')

def delete_arquivos_contrato(request,pk,processo_pk):
    if request.method == 'POST':
        # muito mais facil fazer desse jeito para delete, meu Deus, quase acertei, dq pouco faço so
        processo_nome=str(processo_pk)
        print(processo_nome,'processo_nome no contrato do post')
        contrato_nome=str(pk)
        print(contrato_nome,'contrato_nome no contrato do post')
        caminho_base=os.path.join(settings.MEDIA_ROOT, f'processos/{processo_nome}/contratos/{contrato_nome}')
        arquivo_excluir=request.POST.get('arquivo')
        subpasta=request.POST.get('tipo')
        if arquivo_excluir and subpasta:
            caminho_subpasta=os.path.join(caminho_base, subpasta)
            caminho_arquivo_excluir=os.path.join(caminho_subpasta, arquivo_excluir)
            if os.path.exists(caminho_arquivo_excluir):
                try:
                    os.remove(caminho_arquivo_excluir)
                    messages.success(request, 'Arquivo excluido com sucesso!')
                    print(caminho_arquivo_excluir)
                except Exception as e:
                    print(f"Erro ao deletar o arquivo: {e}")
            else:
                print("Parâmetros inválidos enviados na requisição.")
    return redirect('processos:detalhe_contrato',pk=pk)



#PEDIDOS
class listarpedidos(ListView):
    model=models.Pedidos
    template_name = 'processos/pedidos.html'
    context_object_name = 'pedidos'
    paginate_by = 10

    def get_queryset(self):
        queryset = models.Pedidos.objects.filter(show=True).order_by('-id')
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(contrato__numero__icontains=search_query) |
                Q(numero__icontains=search_query) |
                Q(contratante__icontains=search_query) |
                Q(objeto__icontains=search_query)
            ).order_by('-id')

        sort_param = self.request.GET.get('sort', '')  # self.request captura as informaçoes do template
        sort_options = {
            'data_entrega': '-data_entrega',
            'data_entrega_asc': 'data_entrega',
            'valor': '-valor',
            'valor_asc': 'valor',
        }# key e a variavel, e value e a forma de ordeneção
        if sort_param in sort_options:
            queryset = queryset.order_by(sort_options[sort_param])
        # filtro por categoria do models
        status = self.request.GET.get('status', 'None')
        if status != 'None' and status:
            queryset = queryset.filter(status=status)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #filtragem por  categorias em dropdown
        # Obter as modalidades disponíveis dinamicamente
        context['status'] = models.Pedidos.objects.values_list('status', flat=True).distinct()

        return context








class CriarPedido(CreateView):
    model = models.Pedidos
    template_name = 'processos/criar_pedido.html'
    form_class = PedidoForms
    success_url = reverse_lazy('processos:listarpedidos')
    pk_url_kwarg = 'pedido_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_pedido_form'] = context['form']
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        pk_contrato = self.kwargs.get('pk')
        contrato = get_object_or_404(models.Contratos, pk=pk_contrato)
        kwargs['contrato'] = contrato
        return kwargs

    def form_valid(self, create_pedido_form, ):
        pk_contrato = self.kwargs.get('pk')
        contrato = get_object_or_404(models.Contratos, pk=pk_contrato)
        create_pedido_form.instance.contrato = contrato
        if create_pedido_form.is_valid():
            print(create_pedido_form.cleaned_data)
            create_pedido_form.save(commit=False)
            messages.success(self.request, f'PEDIDO criado com sucesso')
            return super().form_valid(create_pedido_form)
        else:
            messages.error(self.request, f'Existem campos a serem preenchidos')
#depois rever isso daqui, dos forms valids,e invalids
    # numero_processo=self.kwargs['numero_processo']
    def form_invalid(self, create_pedido_form):
        super().form_invalid(create_pedido_form)
        print('falhando aqui invalid')
        print(create_pedido_form.errors)
        response = super().form_invalid(create_pedido_form)
        messages.warning(self.request, 'PEDIDO sendo gerado, preencha as informaçoes com cuidado!')
        return response

class UpdatePedido(UpdateView):
    model = models.Pedidos
    template_name = 'processos/att_pedido.html'
    form_class = PedidoForms
    success_url = reverse_lazy('processos:listarpedidos')
    pk_url_kwarg = 'pedido_pk'

    # e aprendemos com isso da pior forma possivel, que  era so trocar
    # de button para a, e resolvia o Bo inteiro
    # a solução mais simples e a melhor
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attpedidoform'] = context['form']
        return context

    def form_valid(self, attpedidoform):
        response = super().form_valid(attpedidoform)
        print('estou aqui no valido')
        processo_nome = str(self.request.GET.get('processo.pk'))
        print(processo_nome, 'processo')
        contrato_nome = str(self.request.GET.get('contrato.pk'))
        print(contrato_nome, 'contrato')
        print(attpedidoform.cleaned_data)
        messages.success(self.request, f'pedido {self.object.numero} atualizado com sucesso')
        return response

    def form_invalid(self, attpedidoform):
        response = super().form_invalid(attpedidoform)
        print('estou aqui no invavalido')
        print(attpedidoform.errors)
        messages.warning(self.request, f'pedido {self.object.numero} nao pode ser atualizado')
        return response


class DeletarPedido(DeleteView):
    def post(self, request, *args, **kwargs):
        processo_pk=self.kwargs.get('processo_pk')
        print(processo_pk,'pk processo post deletepedidos')# para pegar a pk da url,  kwargs.get
        contrato_pk=kwargs.get('pk')
        print(contrato_pk, 'pk contrato post deletepedidos')
        pedido_pk=kwargs.get('pedido_pk')
        print(pedido_pk, 'pk pedido post deletepedidos')
        processo=get_object_or_404(models.Processo, pk=processo_pk)
        print(processo,'processo post get deletepedidos')
        contrato=get_object_or_404(models.Contratos, pk=contrato_pk)
        print(contrato, 'contrato post get deletepedidos')
        pedido=get_object_or_404(models.Pedidos, pk=pedido_pk)
        print(pedido, 'pedido post deletepedidos')

        processo_nome=str(processo.pk)
        contrato_nome=str(contrato.pk)
        pedido_nome=str(pedido.pk)
        caminho_base=os.path.join(settings.MEDIA_ROOT,
                                  f'processos/{processo_nome}/contratos/{contrato_nome}/pedidos/{pedido_nome}')
        print(caminho_base,'caminho o base no delete pedidos')
        if os.path.exists(caminho_base):
            try:
                pedido.delete()
                shutil.rmtree(caminho_base)
                messages.success(self.request, 'Contrato Excluido com Sucesso  no delete pedido!')  # deletar o processo
            except Exception as e:
                print(f"Erro ao deletar o arquivo: {e}")
            else:
                print("Parâmetros inválidos enviados na requisição.")
        return redirect('processos:listarpedidos')


class DetalharPedido(DetailView):
    model = models.Pedidos
    template_name = 'processos/order.html'
    context_object_name = 'pedido'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['pedidos']=self.get_object().pedidos.all()#captura os pedidos para a pagina do contrato, os associando
        processo=self.get_object().contrato.processo#pegar o processo dentro do contrto dentro do pedido
        processo_nome=str(processo.pk) #lembrei ta pegando o pk da classe pela instancia , associaçao eu acho
        print(processo_nome,'processo_nome no contrato no get context do detalha pedido')
        contrato=self.get_object().contrato
        contrato_nome = str(contrato.pk)
        print(contrato_nome,'contrato_nome no get context detalha pedido')
        pedido_nome=self.object.pk
        print(pedido_nome,'pedido_nome no get context detalha pedido')
        caminho_base_pedidos = os.path.join(settings.MEDIA_ROOT, f'processos/{processo_nome}/contratos/{contrato_nome}/pedidos/{pedido_nome}')
        print(caminho_base_pedidos)
        # cria o acesso  pasta de processos#aonde estao
        if not os.path.exists(caminho_base_pedidos):
            context['arquivos_pedido'] = {}
        else:
            tipo_arquivos = {}
            for subpasta in os.listdir(caminho_base_pedidos):
                caminho_subpasta = os.path.join(caminho_base_pedidos, subpasta)
                tipo_arquivos[subpasta] = os.listdir(caminho_subpasta)
            context['arquivos'] = tipo_arquivos
        return context

    def get_object(self, **kwargs):#talvez precisar retornar somente ao self, ja estava funcionando mesmo
        return get_object_or_404(models.Pedidos, id=self.kwargs['pedido_pk'])#apenas trocar pelo que o



def delete_arquivos_pedido(request,processo_pk,pk,pedido_pk):
    if request.method == 'POST':
        # muito mais facil fazer desse jeito para delete, meu Deus, quase acertei, dq pouco faço so
        processo_nome=str(processo_pk)
        print(processo_nome,'processo_nome no contrato do post')
        contrato_nome=str(pk)
        print(contrato_nome,'contrato_nome no contrato do post')
        pedido_nome = str(pedido_pk)
        print(pedido_nome, 'pedido no contrato do post')
        caminho_base_pedido=os.path.join(settings.MEDIA_ROOT, f'processos/{processo_nome}/contratos/{contrato_nome}/pedidos/{pedido_nome}')
        subpasta = request.POST.get('tipo')
        arquivo_excluir=request.POST.get('arquivo')
        if arquivo_excluir and subpasta:
            caminho_subpasta=os.path.join(caminho_base_pedido, subpasta)
            caminho_arquivo_excluir=os.path.join(caminho_subpasta, arquivo_excluir)
            if os.path.exists(caminho_arquivo_excluir):
                try:
                    os.remove(caminho_arquivo_excluir)
                    messages.success(request, 'Arquivo excluido com sucesso!')
                    print(caminho_arquivo_excluir)
                except Exception as e:
                    print(f"Erro ao deletar o arquivo: {e}")
            else:
                print("Parâmetros inválidos enviados na requisição.")
    return redirect('processos:detalhe_pedido_via_contrato',processo_pk,pk,pedido_pk)#passar os argumentos para
#a formaçao da url










