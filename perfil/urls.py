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



app_name='perfil'

urlpatterns = [

    path('', views.Login.as_view(),
         name='login'),
    path('menuinicial', views.menu_inicial,
         name='menuinicial'),
    path('logout', views.Logout.as_view(),name='logout'),

    path('tabelarh',views.Listar_colaboradores.as_view(),name='tabelarh'),
    path('listarrh/<int:colab_pk>/',views.Colaborador.as_view(),name='detalhe_colaborador'),

    path('listarrh/<int:colab_pk>/delete',views.delete_arquivos_colab,name='deletar_arquivo'),
    path('listarrh/cadastrar_colaborador',views.Cadastrar_colaborador.as_view(),name='cadastrar_colaborador'),
    path('listarrh/atualizar_colaborador/<int:colab_pk>',views.Atualizar_colaborador.as_view(),name='atualizar_colaborador'),
    path('listarrh/<int:colab_pk>/deletar',views.Deletar_colaborador.as_view(),name='deletar_colaborador'),


    path('listarrh/<int:colab_pk>/cadastrardependente/',views.Cadastrardependente.as_view(),name='cadastrardependente'),

    path('listarrh/<int:colab_pk>/dependente/<int:dep_pk>',views.Detalhedependente.as_view(),name='detalhedependente'),
    path('listarrh/<int:colab_pk>/dependente/<int:dep_pk>/atualizar/',views.Atualizardependente.as_view(),name='atualizardependente'),
    path('listarrh/<int:colab_pk>/dependente/<int:dep_pk>/deletar/',views.Deletardependente.as_view(),name='deletardependente'),



    path('listarrh/<int:colab_pk>/uniforme/<int:uniforme_pk>',views.Detalhe_uniforme_epi.as_view(),name='detalheuniforme'),
    path('listarrh/<int:colab_pk>/cadastraruniforme/',views.Cadastrar_uniforme_epi.as_view(),name='cadastraruniforme'),

    path('listarrh/<int:colab_pk>/uniforme/<int:uniforme_pk>/deletar/', views.Deletear_uniforme_epi.as_view(),
         name='deletaruniforme'),
    path('listarrh/<int:colab_pk>/uniforme/<int:uniforme_pk>/atualizar/',views.Atualizar_uniforme_epi.as_view(),
         name='atualizaruniforme'),









    #crud processo


]