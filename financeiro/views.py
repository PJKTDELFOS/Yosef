from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
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
# from .forms import Centro_de_custo_form,Contas_a_pagar_form,Contas_a_receber_form
from .models import Centro_de_custo,Contas_a_pagar,Contas_a_receber
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.falta fazer a injeção de arquivos, terminar os templates,



class Lista_Contas_a_Pagar(LoginRequiredMixin,ListView):
    model = Contas_a_pagar
    template_name = 'financeiro/lista_contas_a_pagar.html'
    context_object_name = 'pagamentos'
    paginate_by = 2

    #fazer o restante da logica
class Conta_a_pagar(LoginRequiredMixin,DetailView):
    model = Contas_a_pagar
    template_name = 'financeiro/pagamento.html'
    context_object_name = 'pagamento'
    pk_url_kwarg = 'pgto_pk'
class Criar_Pagamento(LoginRequiredMixin,CreateView):
    model = Contas_a_pagar
    template_name = 'financeiro/novo_pgto.html'
    form_class = forms.Contas_a_pagar_form
    success_url = reverse_lazy('financeiro:listacontasapagar')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['cadastrar_pgto_form']=context['form']
        return context

    def form_valid(self, cadastrar_pgto_form):
        response=super().form_valid(cadastrar_pgto_form)
        messages.success(self.request, 'Pagamento cadastrado com sucesso!')
        return response

    def form_invalid(self, cadastrar_pgto_form):
        response=super().form_invalid(cadastrar_pgto_form)
        messages.success(self.request, 'Pagamento nao cadastrado!')
        return response
class Atualizar_Pgto(LoginRequiredMixin,UpdateView):
    model = Contas_a_pagar
    form_class = forms.Contas_a_pagar_form
    pk_url_kwarg = 'pgto_pk'
    template_name ='financeiro/att_pgto.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['att_pgto_form']=context['form']
        return context


    def form_valid(self, att_pgto_form):
        response=super().form_valid(att_pgto_form)
        messages.success(self.request, 'Pagamento atualizado com sucesso!')
        return response

    def form_invalid(self, att_pgto_form):
        response = super().form_invalid(att_pgto_form)
        messages.warning(self.request, 'Operação nao efetuada!')
        return response

    def get_success_url(self):
        return reverse_lazy('financeiro:conta_a_pagar',kwargs={'pgto_pk':self.object.pk})
class Deletepgt(LoginRequiredMixin,DeleteView):
    model = Contas_a_pagar
    success_url = reverse_lazy('financeiro:listacontasapagar')
    pk_url_kwarg = 'pgto_pk'

    def post(self, request, *args, **kwargs):
        messages.success(self.request,'pagamento deletado com sucesso!')



class Lista_Contas_a_Receber(LoginRequiredMixin,ListView):
    model = Contas_a_pagar
    template_name = 'financeiro/lista_contas_a_receber.html'
    context_object_name = 'recebimentos'
    paginate_by = 2

    #fazer o restante da logica

class Conta_a_receber(LoginRequiredMixin,DetailView):
    model = Contas_a_receber
    template_name = 'financeiro/recebimento.html'
    context_object_name = 'recebimento'
    pk_url_kwarg = 'recebimento_pk'

class Criar_Recebimento(LoginRequiredMixin,CreateView):
    model = Contas_a_receber
    template_name = 'financeiro/novo_pgto.html'
    form_class = forms.Contas_a_receber_form
    success_url = reverse_lazy('financeiro:listacontasareceber')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['cadastrar_rcbm_form']=context['form']
        return context

    def form_valid(self, cadastrar_rcbm_form):
        response=super().form_valid(cadastrar_rcbm_form)
        messages.success(self.request, 'Recebimento cadastrado com sucesso!')
        return response

    def form_invalid(self, cadastrar_rcbm_form):
        response=super().form_invalid(cadastrar_rcbm_form)
        messages.success(self.request, 'Recebimento nao cadastrado!')
        return response

class Atualizar_Rcbmto(LoginRequiredMixin,UpdateView):
    model = Contas_a_receber
    form_class = forms.Contas_a_receber_form
    pk_url_kwarg = 'recebinenbto_pk'
    template_name ='financeiro/att_rcbmt.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['att_recebimento_form']=context['form']

    def form_valid(self, att_recebimento_form):
        response=super().form_valid(att_recebimento_form)
        messages.success(self.request, 'recebimento atualizado com sucesso!')
        return response

    def form_invalid(self, att_recebimento_form):
        response = super().form_invalid(att_recebimento_form)
        messages.warning(self.request, 'Operação nao efetuada!')
        return response

class DeleteRcbmt(LoginRequiredMixin,DeleteView):
    model = Contas_a_receber
    success_url = reverse_lazy('financeiro:listacontasareceber')

    def post(self, request, *args, **kwargs):
        messages.success(self.request,'recebimento deletado com sucesso!')