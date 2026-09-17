
from django import forms
from .models import Disco
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class DiscoForm(forms.ModelForm):

    class Meta:
        model = Disco
        fields = [
            'titulo',
            'artista',
            'genero',
            'preco',
            'estoque',
            'descricao',
            'disponivel',
        ]

        labels = {
            'titulo': 'Título',
            'artista': 'Artista',
            'genero': 'Gênero',
            'preco': 'Preço',
            'estoque': 'Estoque',
            'descricao': 'Descrição',
            'disponivel': 'Disponível',
        }


class CadastroForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

