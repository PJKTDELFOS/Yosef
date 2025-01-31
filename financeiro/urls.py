"""
URL configuration for setor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views



app_name='financeiro'

urlpatterns = [

    path('contasapagar', views.Lista_Contas_a_Pagar.as_view(),
         name='listacontasapagar'),
    path('contasapagar/<int:pgto_pk>', views.Conta_a_pagar.as_view(),
         name='conta_a_pagar'),
    path('contasapagar/criar_conta', views.Criar_Pagamento.as_view(),
         name='cadastrar_pagamento'),
    path('contasapagar/atualizarpagamento/<int:pgto_pk>', views.Atualizar_Pgto.as_view(),
         name='atualizar_pagamento'),
    path('contasapagar/<int:pgto_pk>/deletarpagamento', views.Deletepgt.as_view(),
         name='delete_pagamento'),


#recebimentos



    path('contasareceber', views.Lista_Contas_a_Receber.as_view(),
         name='listacontasareceber'),

    # path('contasareceber', views.Contas_a_Receber.as_view(),
    #      name='listacontasareceber'),

    #crud processo


]