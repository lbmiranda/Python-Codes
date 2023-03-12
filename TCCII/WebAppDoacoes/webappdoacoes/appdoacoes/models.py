from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import RegexValidator

class User(AbstractUser):
    pass

from django.contrib.auth import get_user_model
User = get_user_model()

class EmpresaEntidade(models.Model):
    cnpj = models.CharField(primary_key=True, max_length=14, validators=[RegexValidator(r'^\d{14}$', 'CNPJ deve conter 14 digitos')])
    nome_fantasia = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    usuario_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)
    logradouro = models.CharField(max_length=100, null=True,blank=True)
    numero = models.CharField(max_length=10, null=True,blank=True)
    bairro = models.CharField(max_length=50, null=True,blank=True)
    cidade = models.CharField(max_length=50, null=True,blank=True)
    estado = models.CharField(max_length=2, null=True,blank=True)

    @property
    def get_endereco(self):
        return f'{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}'

    def get_absolute_url(self):
        return reverse("empresaentidade-detail", args=[self.cnpj])

    def __str__(self):
        return self.nome_fantasia

class Comunidade(models.Model):
    email = models.EmailField()

class PessoaComunidade(Comunidade):
    cpf = models.CharField(max_length=11, primary_key=True,validators=[RegexValidator(r'^\d{11}$', 'CPF deve conter 11 digitos')])
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    comunidade_ptr = models.OneToOneField(
        Comunidade,
        on_delete=models.CASCADE,
        parent_link=True,
        related_name='pessoacomunidade_set',
        null=True
    )

    def __str__(self):
        return f'{self.nome}, {self.sobrenome}'
    
class EmpresaComunidade(Comunidade):
    cnpj = models.CharField(primary_key=True, max_length=14,validators=[RegexValidator(r'^\d{14}$', 'CNPJ deve conter 14 digitos')])
    nome_fantasia = models.CharField(max_length=100)
    comunidade_ptr = models.OneToOneField(
        Comunidade,
        on_delete=models.CASCADE,
        parent_link=True,
        related_name='empresacomunidade_set',
        null=True
    )

    def __str__(self):
        return self.nome_fantasia    

class DonativoMaterialOuServico(models.Model):
    id = models.AutoField(primary_key=True)
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
        return '{0} - {1}'.format(self.id, self.descricao)

class InstanciaMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    material = models.ForeignKey('DonativoMaterialOuServico', null=True, on_delete=models.CASCADE)
    entidade = models.ForeignKey('EmpresaEntidade', null=True, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    class Meta:
        permissions = [('pode_criar_atualizar_material_servico','Cria/Atualiza Necessidade')]

    def __str__(self):
        return 'ID: {0} - (Entidade: {1} - Quantidade: {2})'.format(self.id,self.entidade,self.quantidade)
    
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