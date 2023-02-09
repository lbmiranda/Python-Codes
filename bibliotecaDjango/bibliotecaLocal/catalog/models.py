from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse

# Create your models here.

class Genero(models.Model):
    """Modelo representando um genero literario"""

    nome = models.CharField(max_length=200, help_text='Informe um genero literário. Ex: Ficção científica')

    def __str__(self):       
        
        return self.nome


class Idioma(models.Model):
    name = models.CharField(max_length=200, help_text='Informe o idioma do livro')

    def __str__(self):
        return self.name

class Livro(models.Model):

    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)
    sumario = models.TextField(max_length=1000, help_text='Digite uma descrição resumida do livro')
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='código de 13 caracteres ISBN - <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genero = models.ManyToManyField(Genero, help_text='Selecione um genero para este livro')
    idioma = models.ForeignKey('Idioma', on_delete=models.SET_NULL, null = True)

    def __str__(self):
        
        return self.titulo

    def get_absolute_url(self):

        return reverse('book-detail', args=[str(self.id)])

    def mostra_genero(self):

        return ', '.join([genero.nome for genero in self.genero.all()[:3]])
        

    mostra_genero.short_description = 'Genero'


import uuid    

class InstanciaLivro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID único para este livro em particular')
    livro = models.ForeignKey('Livro', on_delete=models.RESTRICT, null = True)
    edicao = models.CharField(max_length=200)
    data_devolucao = models.DateField(null=True, blank=True)

    STATUS_EMPRESTIMO = (
        ('m', 'Manutenção'),
        ('e', 'Emprestado'),
        ('d', 'Disponível'),
        ('r', 'Reservado'),
    )

    status = models.CharField(
        max_length=1,
        choices= STATUS_EMPRESTIMO,
        blank=True,
        default= 'm',
        help_text= 'Disponibilidade',
    )

    class Meta:
        ordering = ['data_devolucao']

    def __str__(self):
        return f'{self.id}({self.livro.titulo})'


class Autor(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    data_morte = models.DateField('Data da morte', null= True, blank= True)

    class Meta:
        ordering = ['nome','sobrenome']

    def get_absolute_url(self):
        return reverse('autor-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.nome}, {self.sobrenome}'
    

