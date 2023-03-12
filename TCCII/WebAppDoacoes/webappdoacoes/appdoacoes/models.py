from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    pass

from django.contrib.auth import get_user_model
User = get_user_model()

class EmpresaEntidade(models.Model):
    cnpj = models.CharField(primary_key=True, max_length=14)
    nome_fantasia = models.CharField(max_length=100)
    endereco = models.ForeignKey('Endereco', on_delete=models.CASCADE)
    email = models.EmailField(null=True)

    def get_absolute_url(self):
        return reverse("entidade", args={self.cnpj})

    def __str__(self):
        return self.nome_fantasia
      
class PessoaComunidade(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    endereco = models.ForeignKey('Endereco', on_delete=models.CASCADE)
    email = models.EmailField(null=True)    

    def __str__(self):
        return f'{self.nome}, {self.sobrenome}'
    
class EmpresaComunidade(models.Model):
    cnpj = models.CharField(primary_key=True, max_length=14)
    nome_fantasia = models.CharField(max_length=100)
    endereco = models.ForeignKey('Endereco', on_delete=models.CASCADE)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.nome_fantasia
    

class Endereco(models.Model):
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return f'{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}'
    
class DonativoMaterialOuServico(models.Model):
    id = models.AutoField(primary_key=True)
    nome_abreviado = models.CharField(max_length=100)
    descricao = models.CharField(max_length=200, unique=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)

    UNIDADES_MEDIDA = (
        ('un', 'Unidade'),
        ('p','Par'),
        ('kg', 'Quilo'),
        ('l', 'Litro'),
        ('m', 'Metro'),
        ('m2','Metro quadrado'),
        ('s','Serviço'),
    )

    unidade = models.CharField(max_length=3, choices=UNIDADES_MEDIDA, blank=True, null=True)

    def __str__(self):
        return '{0} - {1} ({2})'.format(self.id, self.nome_abreviado, self.descricao)

class InstanciaMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    material = models.ForeignKey('DonativoMaterialOuServico', null=True, on_delete=models.CASCADE)
    entidade = models.ForeignKey('EmpresaEntidade', null=True, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    def __str__(self):
        return 'ID: {0} - (Material: {1} - Entidade: {2} - Quantidade: {3})'.format(self.id, self.material.nome_abreviado,self.entidade,self.quantidade)
    
class Categoria(models.Model):
    codigo_categoria = models.AutoField(primary_key=True)
    MATERIAL = 'M'
    SERVICO = 'S'
    CATEGORIA_CHOICES = [
        (MATERIAL, 'Material'),
        (SERVICO, 'Serviço'),
    ]
    tipo = models.CharField(max_length=1, choices=CATEGORIA_CHOICES)


    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descricao