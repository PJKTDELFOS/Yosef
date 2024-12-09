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
from processos import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include




app_name='processos'

urlpatterns = [
    path('index',views.index,name='index'),
     #teste
    path('login/',views.login,name='login'),
    #crud processo
    path('processos/',views.listarprocessos.as_view(),name='processo'),
    path('processos/adicionarprocesso/',views.CriarProcesso.as_view(),name='inserirprocesso'),
    path('processo/<int:pk>/deletarprocesso',views.DeletarProcesso.as_view(),name='deletarprocesso'),
    path('processos/atualizarprocesso/<int:pk>/',views.UpdateProcesso.as_view(),name='atualizarprocesso'),
    path('detalhe/<int:pk>/',views.DetalharProcesso.as_view(),name='detalhe'),
    path('detalhe/<int:pk>/delete',views.delete_arquivos,name='delete'),

#POOSSO MANDAR A URL DIRETO PELA FUNÇÃO QUE ELE TA, SEM PASSAR PELAS OUTRAS BOM SABER

    #crud contrato
    path('contratos/',views.listarcontratos.as_view(),name='listarcontratos'),
    path('detalhe/<int:processo_pk>/contratos/<int:pk>/',
         views.DetalharContrato.as_view(),name='detalhe_contrato'),
    path('contratos/<int:pk>/',views.DetalharContrato.as_view(),name='detalhe_contrato'),

    #path('processo/criarcontrato/',views.Criarcontrato.as_view(),name='criarcontrato'),
    path('processo/criarcontrato/<int:pk>/',views.Criarcontrato.as_view(),name='criarcontrato'),
    path('detalhe/<int:processo_pk>/detalhe_contrato/<int:pk>/delete/',views.Deletarcontrato.as_view(),name='deletarcontrato'),

    path('contratos/atualizarcontrato/<int:pk>',views.UpdateContrato.as_view(),name='atualizarcontrato'),
    path('detalhe/<int:processo_pk>/detalhe_contrato/<int:pk>/',
         views.delete_arquivos_contrato,name='deletefilescontract'),



#faze 3 sendo
    # url para pedido., uma vindo de processo, para contrato para pedido,
    #  uma vindo de contrato para pedido
    # e uma de tabela pedido


    #crud pedido
        path('',views.listarpedidos.as_view(),name='listarpedidos'),
        path('contratos/<int:pk>/pedido/<int:pedido_pk>/',
         views.DetalharPedido.as_view(),name='detalhe_pedido'),
        path('pedidos/<int:pedido_pk>/',
            views.DetalharPedido.as_view(),name='detalhe_pedido_tabela'),

     path('detalhe/<int:processo_pk>/contratos/<int:pk>/pedidos/<int:pedido_pk>/',
         views.DetalharPedido.as_view(),name='detalhe_pedido_via_contrato'),
        path('contrato/criarpedido/<int:pk>/',views.CriarPedido.as_view(),name='criarpedido'),

        path('detalhe/<int:processo_pk>/contratos/<int:pk>/pedidos/<int:pedido_pk>/delete/',
            views.DeletarPedido.as_view(),name='delete_pedido'),

    path('detalhe/<int:processo_pk>/contratos/<int:pk>/pedidos/<int:pedido_pk>/deleteaquivo',
         views.delete_arquivos_pedido,name='deletearquivospedido'),

    path('pedidos/atualizarpedido/<int:pedido_pk>/',views.UpdatePedido.as_view(),name='atualizarpedido'),



    #path('pedidos/atualizarpedido/<int:pedido_pk>',views.UpdatePedido.as_view(),name='atualizarpedido'),


    ###############################################################################################


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




'''
 path('detalhe/<int:processo_pk>/contratos/<int:pk>/pedidos/<int:pedido_pk>/',
         views.DetalharPedido.as_view(),name='detalhe_pedido_via_contrato'),
'''