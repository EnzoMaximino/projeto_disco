from django.core.serializers import python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Disco, Compra
from .forms import DiscoForm, CadastroForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages

def inicio(request):
    return render(request, 'core/inicio.html')


#  LISTAGEM
def lista_discos(request):
    discos = Disco.objects.all()

    # Pesquisa por título ou artista
    busca = request.GET.get('busca')
    if busca:
        discos = discos.filter(
            Q(titulo__icontains=busca) |
            Q(artista__icontains=busca)
        )

    # Filtro por vendedor
    vendedor = request.GET.get('vendedor')
    if vendedor:
        discos = discos.filter(
            vendedor__username__icontains=vendedor
        )

    # Filtro por gênero
    genero = request.GET.get('genero')
    if genero:
        discos = discos.filter(genero__iexact=genero)

    # Preço mínimo
    preco_min = request.GET.get('preco_min')
    if preco_min:
        discos = discos.filter(preco__gte=preco_min)

    # Preço máximo
    preco_max = request.GET.get('preco_max')
    if preco_max:
        discos = discos.filter(preco__lte=preco_max)

    # Somente disponíveis
    disponivel = request.GET.get('disponivel')
    if disponivel == '1':
        discos = discos.filter(
            disponivel=True,
            estoque__gt=0
        )

    return render(
        request,
        'core/lista_discos.html',
        {
            'discos': discos,
            'busca': busca,
            'vendedor': vendedor,
            'genero': genero,
            'preco_min': preco_min,
            'preco_max': preco_max,
            'disponivel': disponivel,
        }
    )


def detalhe_disco(request, id):
    disco = get_object_or_404(Disco, id=id)
    return render(request, 'core/detalhe_disco.html', {'disco': disco})


#  CRUD PROTEGIDO

@login_required
def criar_disco(request):

    form = DiscoForm(request.POST or None)

    if form.is_valid():

        disco = form.save(commit=False)

        # O usuário logado vira automaticamente o vendedor
        disco.vendedor = request.user

        disco.save()

        return redirect('meu_perfil')

    return render(
        request,
        'core/form_disco.html',
        {'form': form}
    )

@login_required
def editar_disco(request, id):

    disco = get_object_or_404(
        Disco,
        id=id,
        vendedor=request.user
    )

    form = DiscoForm(
        request.POST or None,
        instance=disco
    )

    if form.is_valid():
        form.save()
        return redirect('meu_perfil')

    return render(
        request,
        'core/form_disco.html',
        {'form': form}
    )

@login_required
def excluir_disco(request, id):

    disco = get_object_or_404(
        Disco,
        id=id,
        vendedor=request.user
    )

    if request.method == 'POST':
        disco.delete()
        return redirect('meu_perfil')

    return render(
        request,
        'core/excluir_disco.html',
        {'disco': disco}
    )


#  LOGIN
def login_view(request):
    erro = None

    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=senha
        )

        if user is not None:
            login(request, user)
            return redirect('inicio')

        erro = 'Usuário ou senha incorretos.'

    return render(
        request,
        'core/login.html',
        {'erro': erro}
    )



# MEU PERFIL
@login_required
def meu_perfil(request):

    discos = Disco.objects.filter(
        vendedor=request.user
    )

    return render(
        request,
        'core/meu_perfil.html',
        {
            'usuario': request.user,
            'discos': discos
        }
    )

# PERFIL DE OUTRO VENDEDOR
def perfil_usuario(request, username):

    usuario = get_object_or_404(
        User,
        username=username
    )

    discos = Disco.objects.filter(
        vendedor=usuario,
        disponivel=True,
        estoque__gt=0
    )

    return render(
        request,
        'core/perfil_usuario.html',
        {
            'usuario': usuario,
            'discos': discos
        }
    )

@login_required
def comprar_disco(request, id):

    disco = get_object_or_404(
        Disco,
        id=id,
        disponivel=True,
        estoque__gt=0
    )

    if request.method == 'POST':

        forma_pagamento = request.POST.get('forma_pagamento')

        Compra.objects.create(
            comprador=request.user,
            disco=disco,
            forma_pagamento=forma_pagamento
        )

        disco.estoque -= 1

        if disco.estoque == 0:
            disco.disponivel = False

        disco.save()

        messages.success(
            request,
            'Compra realizada com sucesso!'
        )

        return redirect('lista_discos')

    return render(
        request,
        'core/comprar_disco.html',
        {'disco': disco}
    )


#  LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


#  CADASTRO
def cadastro_view(request):
    form = CadastroForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('login')

    return render(request, 'core/cadastro.html', {'form': form})