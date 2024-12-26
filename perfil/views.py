
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404,redirect,render,HttpResponse
from . import models
from . import forms
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib import messages
from django.db.models import Q
import os
from django.conf import settings
import shutil
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from .models import cadastrofuncionario,dependente,uniformes_EPI,Usuario_sistema
from .forms import Dependenteform

# Create your views here.


def login_perfil(request):
    return render(request,'perfil/colab.html')


class Listar_colaboradores(ListView):
    model = cadastrofuncionario
    template_name = 'perfil/listar_colab.html'
    context_object_name = 'colaboradores'
    paginate_by = 2

        #filtragem do search
    def get_queryset(self):
        queryset=cadastrofuncionario.objects.order_by('-id')
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = self.model.objects.filter(
                Q(nomecompleto__icontains=search_query) |
                Q(cpf__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(telefone__icontains=search_query) |
                Q(cargo__icontains=search_query) |
                Q(setor__icontains=search_query) |
                Q(rg__icontains=search_query)
            ).order_by('-id')

        #ordenação do salario
        sort_param=self.request.GET.get('sort', '')
        sort_options={
            'salario':'-salario',
            'salario_asc':'salario',
            'nome_completo':'-nomecompleto',
            'nome_completo_asc':'nomecompleto',
        }

        if sort_param in sort_options:
            queryset = queryset.order_by(sort_options[sort_param])

        #busca pela escolaridade
        formacao_academica=self.request.GET.get('formacao_academica', 'None')
        cargo = self.request.GET.get('cargo', 'None')
        setor = self.request.GET.get('setor', 'None')

        if formacao_academica != 'None' and formacao_academica:
            queryset = queryset.filter(formacao_academica=formacao_academica)

        if setor != 'None' and setor:
            queryset = queryset.filter(setor=setor)

        if cargo != 'None' and cargo:
            queryset = queryset.filter(cargo=cargo)

        return queryset
#fazer setor, cargo, data de nascimento e ordem alfabrtica
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['formacao_academica']=models.cadastrofuncionario.objects.values_list('formacao_academica',
                                                                                     flat=True).distinct()
        context['setores']=cadastrofuncionario.objects.values_list('setor', flat=True).distinct()
        context['cargos']=cadastrofuncionario.objects.values_list('cargo', flat=True).distinct()
        return context


class Colaborador(DetailView):
    model = cadastrofuncionario
    template_name = 'perfil/colab.html'
    context_object_name = 'colaborador'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        funcionario = self.get_object()
        context['dependentes'] = self.get_object().dependente.all()#dessa forma,caso nao tenha nada ele aind exibe a pagina
        context['uniformes_EPI'] = funcionario.uniforme_epi.all()
        colab_nome=str(self.object.cpf)
        caminho_base=os.path.join(settings.MEDIA_ROOT,f'rh/{colab_nome}')
        if not os.path.exists(caminho_base):
            context['arquivos']={}
        else:
            tipo_arquivos={}
            for subpasta in os.listdir(caminho_base):
                caminho_subpasta=os.path.join(caminho_base, subpasta)
                tipo_arquivos[subpasta]=os.listdir(caminho_subpasta)
            context['arquivos']=tipo_arquivos
        return context

def delete_arquivos_colab(request,pk):
    if request.method == 'POST':# muito mais facil fazer desse jeito para delete, meu Deus, quase acertei, dq pouco faço so
        cpf=models.cadastrofuncionario.objects.get(pk=pk).cpf #forma de pegar o valor dentro do obejeto do models
        colab_cpf=str(cpf)
        print(colab_cpf,'cpf pego')
        caminho_base=os.path.join(settings.MEDIA_ROOT,f'rh/{colab_cpf}')
        arquivo_excluir=request.POST.get('arquivo')
        subpasta=request.POST.get('tipo')
        if arquivo_excluir and subpasta:
            caminho_subpasta=os.path.join(caminho_base, subpasta)
            caminho_arquivo_excluir=os.path.join(caminho_subpasta, arquivo_excluir)
            print(caminho_arquivo_excluir,'aqui 0')
            if os.path.exists(caminho_arquivo_excluir):
                try:
                    os.remove(caminho_arquivo_excluir)
                    messages.success(request, 'Arquivo excluido com sucesso!')
                    print(caminho_arquivo_excluir)
                except Exception as e:
                    print(f"Erro ao deletar o arquivo: {e}")
            else:
                print("Parâmetros inválidos enviados na requisição.")
    return redirect('perfil:detalhe_colaborador',pk=pk)

class Cadastrar_colaborador(CreateView):
    model = models.cadastrofuncionario
    template_name = 'perfil/cadastrar_colab.html'
    form_class = forms.PerfilForm
    success_url = reverse_lazy('perfil:tabelarh')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['cadastrar_colaborador_form'] = context['form']
        return context

    def form_valid(self, cadastrar_colaborador_form):
        response=super().form_valid(cadastrar_colaborador_form)
        messages.success(self.request, 'Colaborador cadastrado com sucesso!')
        return response

    def form_invalid(self, cadastrar_colaborador_form):
        response=super().form_invalid(cadastrar_colaborador_form)
        messages.warning(self.request, 'Colaborador nao cadastrado ')
        print(cadastrar_colaborador_form.errors)
        return response

class Atualizar_colaborador(UpdateView):
    model = models.cadastrofuncionario
    template_name = 'perfil/colab_att.html'
    form_class = forms.PerfilForm
    success_url = reverse_lazy('perfil:tabelarh')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['att_colaborador_form']=context['form']
        return context

    def form_valid(self, att_colaborador_form):
        response=super().form_valid(att_colaborador_form)
        messages.success(self.request, 'Colaborador atualizado com sucesso!')
        return response

    def form_invalid(self, att_colaborador_form):
        response=super().form_invalid(att_colaborador_form)
        messages.warning(self.request, 'Colaborador nao atualizado')
        print(att_colaborador_form.errors)
        return response



class Deletar_colaborador(DeleteView):
    def post(self, request, *args, **kwargs):
        colab_id=self.kwargs['pk']
        colab_obj=get_object_or_404(models.cadastrofuncionario, pk=colab_id)
        colab_cpf=str(colab_obj.cpf)
        print(colab_cpf,'cpf do deletar')
        caminho_base=os.path.join(settings.MEDIA_ROOT,f'rh/{colab_cpf}')
        colab_obj.delete()
        if os.path.exists(caminho_base):
            try:
                shutil.rmtree(caminho_base)
                messages.success(request, 'Colaborador excluido com sucesso!')
            except Exception as e:
                print(f"Erro ao deletar o arquivo: {e}")
        else:
            print("Parâmetros inválidos enviados na requisição.")
        return redirect('perfil:tabelarh')


class Cadastrardependente(CreateView):
    model = models.dependente
    template_name = 'perfil/dep_cadastrar.html'
    form_class = forms.Dependenteform
    success_url = reverse_lazy('perfil:tabelarh')

    def dispatch(self, request, *args, **kwargs):
        try:
            self.funcionario = models.cadastrofuncionario.objects.get(pk=kwargs['pk'])
            #print(f"Funcionário recuperado no dispatch: {self.funcionario}")
        except models.cadastrofuncionario.DoesNotExist:
            messages.error(request, "Funcionário não encontrado.")
            return redirect('perfil:tabelarh')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cadastrar_dependente_form'] = context['form']
        context['cadastrar_dependente_form'] = forms.Dependenteform(nome_funcionario=self.funcionario,)
        #print(f"Formulário instanciado com funcionario: {context['cadastrar_dependente_form'].instance.funcionario}")
        context['funcionario'] = self.funcionario
        return context

    def form_valid(self, form):
        form.instance.funcionario = self.funcionario
        messages.success(self.request, 'Dependente cadastrado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.warning(self.request, 'Dependente não cadastrado. Verifique os campos.')
        print(f"Erros no formulário: {form.errors}")
        return response



#refazer os contratos e pedidos, rever o campo, para que receba o contrato e o pedido, refazxer quase tudo nesse ponto







