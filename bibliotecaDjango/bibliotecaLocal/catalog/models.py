from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse

# Create your models here.

class Genero(models.Model):
    """Modelo representando um genero literario"""

    nome = models.CharField(max_length=200, help_text='Digite um genereo. Ex: Ficção científica')

    def __str__(self):       
        
        return self.name

class Livro(models.Model):

    titulo = models.CharField(max_length=200)
    #autor = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    sumario = models.TextField(max_length=1000, help_text='Digite uma descrição resumida do livro')
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='código de 13 caracteres ISBN - href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genero = models.ManyToManyField(Genero, help_text='Selecione um genero para este livro')

    def __str__(self):
        
        return self.titulo

    def get_absolute_url(self):

        return reverse('book-detail', args=[str(self.id)])

        

