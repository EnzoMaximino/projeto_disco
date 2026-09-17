
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Disco(models.Model):

    vendedor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='discos'
    )

    titulo = models.CharField(max_length=150)

    artista = models.CharField(max_length=150)

    genero = models.CharField(max_length=100)

    preco = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    estoque = models.IntegerField(
        validators=[MinValueValidator(0)]
    )

    descricao = models.TextField()

    disponivel = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.titulo} - {self.artista}"

class Compra(models.Model):
    comprador = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    disco = models.ForeignKey(
        Disco,
        on_delete=models.CASCADE
    )

    forma_pagamento = models.CharField(
        max_length=20
    )

    data_compra = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.comprador.username} - {self.disco.titulo}"
