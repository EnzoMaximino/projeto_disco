
from django.urls import path

from .views import (
    comprar_disco,
    inicio,
    lista_discos,
    detalhe_disco,
    criar_disco,
    editar_disco,
    excluir_disco,
    login_view,
    logout_view,
    cadastro_view,
    meu_perfil,
    perfil_usuario,
)

urlpatterns = [

    # Página inicial
    path('', inicio, name='inicio'),

    # Discos
    path('discos/', lista_discos, name='lista_discos'),

    path(
        'discos/<int:id>/',
        detalhe_disco,
        name='detalhe_disco'
    ),

    path(
        'discos/novo/',
        criar_disco,
        name='criar_disco'
    ),

    path(
        'discos/editar/<int:id>/',
        editar_disco,
        name='editar_disco'
    ),

    path(
        'discos/excluir/<int:id>/',
        excluir_disco,
        name='excluir_disco'
    ),

    # Perfis
    path(
        'perfil/',
        meu_perfil,
        name='meu_perfil'
    ),

    path(
        'perfil/<str:username>/',
        perfil_usuario,
        name='perfil_usuario'
    ),

    # Autenticação
    path(
        'login/',
        login_view,
        name='login'
    ),

    path(
        'logout/',
        logout_view,
        name='logout'
    ),

    path(
        'cadastro/',
        cadastro_view,
        name='cadastro'
    ),

    path(
    'disco/<int:id>/comprar/',
    comprar_disco,
    name='comprar_disco'
),
]

