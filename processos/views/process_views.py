
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
from utils.tools_utils import criar_planilha
from ..models import Processo


# Create your views here.

#PROCESSOS
class listarprocessos(ListView):
    model = models.Processo
    template_name = 'processos/processo.html'
    context_object_name = 'processos'
    paginate_by = 10

    def get_queryset(self):
        queryset = models.Processo.objects.filter(show=True).order_by('-id')
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(numero_processo__icontains=search_query) |
                Q(numero_licitacao__icontains=search_query) |
                Q(contratante__icontains=search_query) |
                Q(modalidade__icontains=search_query)
            ).order_by('-id')
        sort_param = self.request.GET.get('sort', '')
        if sort_param =='data_disputa':
            queryset = queryset.order_by('-data_disputa')
        elif sort_param =='data_disputa_asc':
            queryset = queryset.order_by('data_disputa')
        modalidade=self.request.GET.get('modalidade', 'None')
        status = self.request.GET.get('status', 'None')
        tipo=self.request.GET.get('tipo', 'None')
        if modalidade  != 'None' and modalidade:
            queryset = queryset.filter(modalidade=modalidade)
        if status  != 'None' and status:
            queryset = queryset.filter(status=status)
        if tipo  != 'None'and tipo:
            queryset = queryset.filter(tipo=tipo)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['modalidades'] = models.Processo.objects.values_list('modalidade', flat=True).distinct()
        context['situacao'] = models.Processo.objects.values_list('status', flat=True).distinct()
        context['tipos'] = models.Processo.objects.values_list('tipo', flat=True).distinct()
        return context
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
        messages.warning(self.request, 'processo nao criado com sucesso!')
        return super().form_invalid(create_process_form)

@method_decorator(never_cache, name='dispatch')
class UpdateProcesso(UpdateView):
    model = models.Processo
    template_name = 'processos/att_processo.html'
    form_class = ProcessForm
    success_url = reverse_lazy('processos:processo')
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['att_process_form']=context['form']
        return context
    def form_valid(self, att_process_form):
        response = super().form_valid(att_process_form)
        print(att_process_form.cleaned_data)
        messages.success(self.request, f'Processo { self.object.numero_processo} atualizado com sucesso')
        return response
    def form_invalid(self, att_process_form):
        response=super().form_invalid(att_process_form)
        print(att_process_form.errors)
        messages.warning(self.request, f'Processo { self.object.numero_processo} nao pode ser atualizado')
        return response
class DeletarProcesso(View):
    def post(self, request, *args, **kwargs):
        processo=get_object_or_404(models.Processo, pk=kwargs['pk'])
        messages.warning(self.request, 'Processo excluido com sucesso!')
        processo_nome=processo.pk
        caminho_base = os.path.join(settings.MEDIA_ROOT, f'processos/{processo_nome}')
        processo.delete()
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
    if request.method == 'POST':
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

class listarcontratos(ListView):
    model=models.Contratos
    template_name = 'processos/contrato.html'
    context_object_name = 'contratos'
    paginate_by = 10
    def get_queryset(self):
        queryset = models.Contratos.objects.filter(show=True).order_by('-id')
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(numero__icontains=search_query) |
                Q(objeto__icontains=search_query) |
                Q(contratante__icontains=search_query) |
                Q(processo__numero_processo__icontains=search_query)|
                Q(observacoes__icontains=search_query)
            ).order_by('-id')


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
        seguro = self.request.GET.get('seguro', 'None')
        if seguro != 'None' and seguro:
            queryset = queryset.filter(seguro=seguro)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seguros'] = models.Contratos.objects.values_list('seguro', flat=True).distinct()
        return context

class Criarcontrato(CreateView):
    model = models.Contratos
    template_name = 'processos/criar_contrato.html'
    form_class =ContractForm
    success_url = reverse_lazy('processos:listarcontratos')

    def dispatch(self, request, *args, **kwargs):
        try:
            self.numero_processo=models.Processo.objects.get(pk=self.kwargs['pk'])
            print('processo recuperado no dispatch')
        except Processo.DoesNotExist:
            messages.error(request, "PROCESSO não encontrado.")
            return redirect('processos:processo')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['create_contract_form'] = context['form']
        context['create_contract_form'] = ContractForm(processo_de_origem=self.numero_processo)
        context['processo'] = self.numero_processo
        return context

    def form_valid(self, create_contract_form,):
       create_contract_form.instance.processo = self.numero_processo
       messages.success(self.request, 'CONTRATO cadastrado com sucesso!')
       return super().form_valid(create_contract_form)

    def form_invalid(self, create_contract_form):
        super().form_invalid(create_contract_form)
        print('falhando aqui invalid')
        print(create_contract_form.errors)
        response=super().form_invalid(create_contract_form)
        messages.warning(self.request, 'Contrato sendo gerado, preencha as informaçoes com cuidado!')
        return  response

class UpdateContrato(UpdateView):
    model = models.Contratos
    template_name = 'processos/att_contrato.html'
    form_class = ContractForm

    def dispatch(self, request, *args, **kwargs):
        try:
            self.contrato=models.Contratos.objects.get(pk=self.kwargs['pk'])
            self.numero_processo = self.contrato.processo
            if not self.contrato:
                messages.error(request, "Nenhum contrato associado a este processo.")
                return redirect('processos:listarcontratos')
            print('Processo e contrato recuperados no dispatch')
        except models.Processo.DoesNotExist:
            messages.error(request, "Processo não encontrado.")
            return redirect('processos:listarcontratos')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['att_contract_form'] = ContractForm(instance=self.contrato, processo_de_origem=self.numero_processo)
        context['processo'] = self.numero_processo
        return context

    def form_valid(self, att_contract_form):
        att_contract_form.instance.processo = self.numero_processo
        messages.success(self.request, f'Contrato {self.contrato.numero} atualizado com sucesso!')
        return super().form_valid(att_contract_form)

    def form_invalid(self, att_contract_form):
        print('Erro ao atualizar contrato:')
        print(att_contract_form.errors)
        messages.warning(self.request, 'Preencha as informações do contrato com cuidado.')
        return super().form_invalid(att_contract_form)

    def get_success_url(self):
        if'processo_pk' in self.kwargs:
            return reverse_lazy('processos:detalhe_contrato', kwargs={'pk':self.object.pk,'processo_pk':self.kwargs['processo_pk']})
        else:
            return reverse_lazy('processos:detalhe_contrato_via_tabela', kwargs={'pk':self.object.pk})

class DetalharContrato(DetailView):
    model = models.Contratos
    template_name = 'processos/contract.html'
    context_object_name = 'contrato'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pedidos']=self.get_object().pedidos.all()
        processo=self.get_object().processo
        processo_nome=str(processo.pk)
        print(processo_nome,'processo_nome no contrato no get context')
        contrato_nome=self.object.pk
        print(contrato_nome,'contrato_nome no get context')
        caminho_base_contratos = os.path.join(settings.MEDIA_ROOT,
                                              f'processos/{processo_nome}/contratos/{contrato_nome}')
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
    return redirect('processos:detalhe_contrato_via_tabela',pk=pk)

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
        sort_param = self.request.GET.get('sort', '')
        sort_options = {
            'data_entrega': '-data_entrega',
            'data_entrega_asc': 'data_entrega',
            'valor': '-valor',
            'valor_asc': 'valor',
        }
        if sort_param in sort_options:
            queryset = queryset.order_by(sort_options[sort_param])

        status = self.request.GET.get('status', 'None')
        if status != 'None' and status:
            queryset = queryset.filter(status=status)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = models.Pedidos.objects.values_list('status', flat=True).distinct()
        return context

class CriarPedido(CreateView):
    model = models.Pedidos
    template_name = 'processos/criar_pedido.html'
    form_class = PedidoForms
    success_url = reverse_lazy('processos:listarpedidos')
    pk_url_kwarg = 'pedido_pk'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.contrato=models.Contratos.objects.get(pk=self.kwargs['pk'])
            print('Contrato recuperado no dispatch')
        except models.Contratos.DoesNotExist:
            messages.error(request, "contrato não encontrado.")
            return redirect('processos:listarpedidos')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        # context['create_pedido_form'] = context['form']
        context['form'] = PedidoForms(contrato_de_origem=self.contrato)
        context['contrato'] = self.contrato
        return context

    def form_valid(self,form,):
       cform.instance.contrato = self.contrato
       messages.success(self.request, 'pedido cadastrado com sucesso!')
       return super().form_valid(form)


    def form_invalid(self, form):
        print('Erro ao atualizar pedido:')
        print(form.errors)
        messages.warning(self.request, 'Preencha as informações do contrato com cuidado.')
        return super().form_invalid(form)



class UpdatePedido(UpdateView):
    model = models.Pedidos
    template_name = 'processos/att_pedido.html'
    form_class = PedidoForms
    success_url = reverse_lazy('processos:listarpedidos')
    pk_url_kwarg = 'pedido_pk'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.pedido=models.Pedidos.objects.get(pk=self.kwargs[self.pk_url_kwarg])
            self.contrato=self.pedido.contrato
            print('contrato recuperado no dispatch')
        except models.Pedidos.DoesNotExist:
            messages.error(request, "Pedido não encontrado.")
            return redirect('processos:listarpedidos')
        except models.Contratos.DoesNotExist:
            messages.error(request, "Contrato associado ao pedido não encontrado.")
            return redirect('processos:listarpedidos')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['attpedidoform'] = context['form']
        context['form'] = PedidoForms(instance=self.object, contrato_de_origem=self.contrato)
        context['contrato'] = self.contrato
        return context

    def form_valid(self, form):
        form.instance.contrato = self.contrato
        response = super().form_valid(form)
        print('estou aqui no valido')
        processo_nome = str(self.request.GET.get('processo.pk'))
        print(processo_nome, 'processo')
        contrato_nome = str(self.request.GET.get('contrato.pk'))
        print(contrato_nome, 'contrato')
        print(form.cleaned_data)
        messages.success(self.request, f'pedido {self.object.numero} atualizado com sucesso')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        print('estou aqui no invavalido')
        print(form.errors)
        messages.warning(self.request, f'pedido {self.object.numero} nao pode ser atualizado')
        return response

    def get_success_url(self):
        if 'processo_pk'in self.kwargs and  'pk'in self.kwargs and 'pedido_pk' in self.kwargs:
            return reverse_lazy('processos:detalhe_pedido_via_contrato', kwargs={'pedido_pk':self.object.pk,'processo_pk':self.kwargs['processo_pk'],'pk':self.kwargs['pk']})
        else:
            return reverse_lazy('processos:detalhe_pedido_tabela', kwargs={'pedido_pk':self.object.pk})

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

    def get_object(self, **kwargs):
        return get_object_or_404(models.Pedidos, id=self.kwargs['pedido_pk'])

def delete_arquivos_pedido(request,processo_pk,pk,pedido_pk):
    if request.method == 'POST':
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
def gerar_planilha_pedido(request, pedido_pk):
    pedido = get_object_or_404(models.Pedidos, pk=pedido_pk)

    if request.method == 'POST':
        try:
            criar_planilha(pedido)
            messages.success(request, 'Planilha do pedido gerada com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao gerar a planilha: {e}')

        return redirect('processos:detalhe_pedido_tabela', pedido_pk=pedido.pk)









