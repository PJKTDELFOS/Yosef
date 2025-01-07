from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic.list import ListView,View
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404,redirect,render,HttpResponse
from . import models
from . import forms
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.db.models import Q
import os
from django.conf import settings
import shutil
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from .models import cadastrofuncionario,dependente,uniformes_EPI,Usuario_sistema
from .forms import Dependenteform,Uniformes_epi_form
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# Create your views here.

@login_required
def menu_inicial(request):
    return  render(request, 'perfil/menuinicial.html')


class Login(LoginView):
    template_name = 'perfil/login.html'
    success_url = reverse_lazy('perfil:menuinicial')
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.success_url


class Logout(View):
    def get(self,*args,**kwargs):
        logout(self.request)
        return redirect('perfil:menuinicial')


class Listar_colaboradores(LoginRequiredMixin,ListView):
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


class Colaborador(LoginRequiredMixin,DetailView):
    model = cadastrofuncionario
    template_name = 'perfil/colab.html'
    context_object_name = 'colaborador'
    pk_url_kwarg = 'colab_pk'

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
@login_required(login_url='/login/')
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

class Cadastrar_colaborador(LoginRequiredMixin,CreateView):
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


class Atualizar_colaborador(LoginRequiredMixin,UpdateView):
    model = models.cadastrofuncionario
    template_name = 'perfil/colab_att.html'
    form_class = forms.PerfilForm
    pk_url_kwarg = 'colab_pk'


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

    def get_success_url(self):
        return reverse_lazy('perfil:detalhe_colaborador', kwargs={'colab_pk': self.object.pk})


class Deletar_colaborador(LoginRequiredMixin,DeleteView):
    def post(self, request, *args, **kwargs):
        colab_id=self.kwargs['colab_pk']
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


class Cadastrardependente(LoginRequiredMixin,CreateView):
    model = models.dependente
    template_name = 'perfil/dep_cadastrar.html'
    form_class = forms.Dependenteform

    def dispatch(self, request, *args, **kwargs):
        try:
            self.funcionario = models.cadastrofuncionario.objects.get(pk=kwargs['colab_pk'])
            print(f"Funcionário recuperado no dispatch: {self.funcionario}")
        except models.cadastrofuncionario.DoesNotExist:
            messages.error(request, "Funcionário não encontrado.")
            return redirect('perfil:tabelarh')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cadastrar_dependente_form'] = context['form']
        context['cadastrar_dependente_form'] = forms.Dependenteform(nome_funcionario=self.funcionario,)
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
    def get_success_url(self):
        return reverse_lazy('perfil:detalhe_colaborador', kwargs={'colab_pk': self.funcionario.pk})


class Atualizardependente(LoginRequiredMixin,UpdateView):
    model = models.dependente
    template_name = 'perfil/dep_att.html'
    form_class = forms.Dependenteform
    pk_url_kwarg = 'dep_pk'

    def get_dependente_and_funcionario(self,dep_pk):
        try:
            dependente = models.dependente.objects.get(pk=dep_pk)
            funcionario = dependente.funcionario
            return dependente, funcionario
        except models.dependente.DoesNotExist:
            return redirect('perfil:tabelarh')

    def dispatch(self, request, *args, **kwargs):
        try:
            self.dependente,self.funcionario = self.get_dependente_and_funcionario(kwargs['dep_pk'])

            if not self.dependente:
                messages.error(self.request,'Nenhum dependente associado a este funcionario')
                return redirect('perfil:tabelarh')

            if not self.funcionario:
                messages.error(self.request,'Nenhum funcionario associado a este dependente')
                return redirect('perfil:tabelarh')

        except models.dependente.DoesNotExist:
            messages.error(self.request,'Funcionario ou dependente nao localizado')
            return redirect('perfil:tabelarh')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['att_dependente_form']=Dependenteform(instance=self.dependente, nome_funcionario=self.funcionario)
        context['funcionario']=self.funcionario
        return context

    def form_valid(self, att_dependente_form):
        att_dependente_form.instance.funcionario =self.funcionario
        messages.success(self.request,'Dependente atualizado com sucesso!')
        return  super().form_valid(att_dependente_form)

    def form_invalid(self, att_dependente_form):
        response = super().form_invalid(att_dependente_form)
        messages.warning(self.request, 'Dependente não atualizado. Verifique os campos.')
        print(f"Erros no formulário: {att_dependente_form.errors}")
        return response

    def get_success_url(self):
        if 'colab_pk' in self.kwargs:
            return reverse_lazy('perfil:detalhedependente', kwargs={ 'dep_pk': self.object.pk,
                                                                       'colab_pk': self.kwargs['colab_pk']})

class Deletardependente(LoginRequiredMixin,DeleteView):
    model = dependente
    pk_url_kwarg = 'dep_pk'
    def get_success_url(self):
        messages.success(self.request,'Dependente excluido com sucesso!')
        return reverse_lazy('perfil:detalhe_colaborador', kwargs={'colab_pk': self.object.funcionario.pk})

class Detalhedependente(LoginRequiredMixin,DetailView):
    model = dependente
    template_name = 'perfil/dependente.html'
    context_object_name = 'dependente'
    pk_url_kwarg = 'dep_pk'


class Detalhe_uniforme_epi(LoginRequiredMixin,DetailView):
    model = uniformes_EPI
    template_name = 'perfil/uniforme.html'
    context_object_name = 'uniforme'
    pk_url_kwarg = 'uniforme_pk'

class Cadastrar_uniforme_epi(LoginRequiredMixin,CreateView):
    model = uniformes_EPI
    template_name = 'perfil/uniforme_cadastro.html'
    form_class = Uniformes_epi_form

    def dispatch(self, request, *args, **kwargs):
        try:
            self.funcionario = models.cadastrofuncionario.objects.get(pk=kwargs['colab_pk'])
        except models.cadastrofuncionario.DoesNotExist:
            messages.error(request, "Funcionário não encontrado.")
            return redirect('perfil:tabelarh')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['cadastrar_uniforme_epi_form']=context['form']
        context['cadastrar_uniforme_epi_form']=forms.Uniformes_epi_form(nome_funcionario=self.funcionario,)
        context['funcionario']=self.funcionario
        return context

    def form_valid(self, cadastrar_uniforme_epi_form):
        cadastrar_uniforme_epi_form.instance.funcionario=self.funcionario
        messages.success(self.request,'Uniformos cadastrando com sucesso')
        return super().form_valid(cadastrar_uniforme_epi_form)

    def form_invalid(self, cadastrar_uniforme_epi_form):
        messages.warning(self.request,'Operação nao realizada')
        print(cadastrar_uniforme_epi_form.errors)
        return super().form_invalid(cadastrar_uniforme_epi_form)

    def get_success_url(self):
        return reverse_lazy('perfil:detalhe_colaborador', kwargs={'colab_pk':self.kwargs['colab_pk']})



class Deletear_uniforme_epi(LoginRequiredMixin,DeleteView):
    model = uniformes_EPI
    pk_url_kwarg = 'uniforme_pk'
    def get_success_url(self):
        messages.success(self.request,'Uniforme EPI excluido com sucesso!')
        return reverse_lazy('perfil:detalhe_colaborador', kwargs={'colab_pk': self.object.funcionario.pk})


class Atualizar_uniforme_epi(LoginRequiredMixin,UpdateView):
    model = uniformes_EPI
    template_name = 'perfil/uniforme_att.html'
    form_class = Uniformes_epi_form
    pk_url_kwarg = 'uniforme_pk'

    def get_uniforme_and_funcionario(self,uniforme_pk):
        try:
            uniforme=models.uniformes_EPI.objects.get(pk=uniforme_pk)
            funcionario=uniforme.funcionario
            return uniforme,funcionario
        except models.uniformes_EPI.DoesNotExist:
            return redirect('perfil:tabelarh')

    def dispatch(self, request, *args, **kwargs):
        try:
            self.uniforme,self.funcionario=self.get_uniforme_and_funcionario(kwargs['uniforme_pk'])
            if not self.uniforme:
                messages.error(self.request,'Nenhum uniforme associado a este funcionario')
                return redirect('perfil:tabelarh')
            if not self.funcionario:
                messages.error(self.request,'Nenhum funcionario associado a este uniforme')
                return redirect('perfil:tabelarh')
        except models.uniformes_EPI.DoesNotExist:
            messages.error(self.request,'Funcionario ou uniforme nao localizado')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['att_uniforme_epi_form']=Uniformes_epi_form(instance=self.uniforme, nome_funcionario=self.funcionario)
        context['funcionario']=self.funcionario
        return context

    def form_valid(self, att_uniforme_epi_form):
        att_uniforme_epi_form.instance.funcionario=self.funcionario
        messages.success(self.request,'uniforme atualizado com sucesso!')
        return super().form_valid(att_uniforme_epi_form)

    def form_invalid(self, att_uniforme_epi_form):
        messages.error(self.request,'Atualizaçao falhou, por favor verifique os dados')

    def get_success_url(self):
        if 'colab_pk' in self.kwargs:
            return reverse_lazy('perfil:detalheuniforme', kwargs={ 'uniforme_pk': self.object.pk,
                                                                       'colab_pk': self.kwargs['colab_pk']})







#fazer atualizaçao e deleção dos uniformes










#refazer os contratos e pedidos, rever o campo, para que receba o contrato e o pedido, refazxer quase tudo nesse ponto







