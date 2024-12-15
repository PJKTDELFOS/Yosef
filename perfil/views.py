from django.shortcuts import render,get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from . import models
from django.shortcuts import get_object_or_404,redirect,render,HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from processos import models
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


def login_perfil(request):
    return render(request,'perfil/listar_colab.html')