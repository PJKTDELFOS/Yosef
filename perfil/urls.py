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
from processos import views


app_name='perfil'

urlpatterns = [
    path('index',views.index,name='index'),
     #teste
    path('login/',views.login,name='login'),
    #crud processo
    path('processos/',views.listarprocessos.as_view(),name='processo'),
    #crud contrato
    path('contratos/',views.listarcontratos.as_view(),name='listarcontratos'),
    #crud pedido
    path('',views.listarpedidos.as_view(),name='listarpedidos'),
    #detalhe

    ###############################################################################################

    #slugs
    path('processos/<int:pk>/',views.DetalharProcesso.as_view(),name='detalhe'),
    path('contratos/<int:pk>/',views.DetalharContrato.as_view(),name='detalhe_contrato'),
    path('pedidos/<int:pk>/',views.DetalharPedido.as_view(),name='detalhe_pedido'),

]