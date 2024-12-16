from django.shortcuts import render,get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from . import models
from django.shortcuts import get_object_or_404,redirect,render,HttpResponse
from django.views import View
from . import models
from . import forms
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib import messages
from django.db.models import Q
from urllib.parse import urlencode
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
import os
from django.conf import settings
import shutil

# Create your views here.


def login_perfil(request):
    return render(request,'perfil/colab.html')


class Listar_colaboradores(ListView):
    model = models.cadastrofuncionario
    template_name = 'perfil/listar_colab.html'
    context_object_name = 'colaboradores'
    paginate_by = 10

        #filtragem do search
    def get_queryset(self):
        queryset=models.cadastrofuncionario.objects.order_by('-id')
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
        context['setores']=models.cadastrofuncionario.objects.values_list('setor', flat=True).distinct()
        context['cargos']=models.cadastrofuncionario.objects.values_list('cargo', flat=True).distinct()
        return context

