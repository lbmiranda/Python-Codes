from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import RegexValidator

class User(AbstractUser):
    COMUNIDADEPF = 'comunidade-PF'
    COMUNIDADEPJ = 'comunidade-PJ'
    ENTIDADE = 'entidade'
    TIPO_CONTA_CHOICES = (
        (COMUNIDADEPF, 'Comunidade PF'),
        (COMUNIDADEPJ, 'Comunidade PJ'),
        (ENTIDADE, 'Entidade'),
    )
    tipo_de_conta = models.CharField(max_length=20, choices=TIPO_CONTA_CHOICES)

    entidade = models.ForeignKey("EmpresaEntidade", verbose_name=("Entidade"), on_delete=models.RESTRICT, null=True,blank=True)
    comunidade_pf = models.ForeignKey("PessoaComunidade",verbose_name=('Comunidade PF'),on_delete=models.RESTRICT, null=True,blank=True)
    comunidade_pj = models.ForeignKey("EmpresaComunidade",verbose_name=('Comunidade PJ'),on_delete=models.RESTRICT, null=True,blank=True)

from django.contrib.auth import get_user_model
User = get_user_model()

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    detalhes = models.CharField(max_length=10000,blank=True,null=True)

class EmpresaEntidade(models.Model):
    cnpj = models.CharField(primary_key=True, max_length=14, validators=[RegexValidator(r'^\d{14}$', 'CNPJ deve conter 14 digitos')])
    nome_fantasia = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    usuario_responsavel = models.OneToOneField(User, on_delete=models.SET_NULL, null=True,blank=True)
    logradouro = models.CharField(max_length=100, null=True,blank=True)
    numero = models.IntegerField(null=True,blank=True)
    bairro = models.CharField(max_length=50, null=True,blank=True)
    cidade = models.CharField(max_length=50, null=True,blank=True)
    
    ESTADOS = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins')
    ]
    
    estado = models.CharField(max_length=2, choices=ESTADOS, null=True,blank=True)

    class Meta:
        permissions = [('pode_criar_atualizar_entidade','Cria/Atualiza Entidade'),('pode_deletar_entidade','Deleta Entidade')]

    @property
    def get_endereco(self):
        return f'{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}'

    def get_absolute_url(self):
        return reverse("entidade-detail", args=[self.cnpj])

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

class Donativo(models.Model):
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

    class Meta:
        permissions = [('pode_criar_atualizar_donativo','Cria/Atualiza Donativo'),('pode_deletar_donativo','Deleta Donativo')]

    def __str__(self):
        return '{0} - {1}'.format(self.id, self.descricao)
    
    def get_absolute_url(self):
        return reverse("donativo-detail", args=[self.id])

class InstanciaDonativo(models.Model):
    id = models.AutoField(primary_key=True)
    donativo = models.ForeignKey('Donativo', null=True, on_delete=models.CASCADE)
    entidade = models.ForeignKey('EmpresaEntidade', null=True, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    class Meta:
        permissions = [('pode_criar_atualizar_necessidade','Cria/Atualiza necessidade'),('pode_deletar_necessidade','Deleta necessidade')]
    
    def __str__(self):
        return 'ID: {0} - (Entidade: {1} - Quantidade: {2})'.format(self.id,self.entidade,self.quantidade)
    
    def get_absolute_url(self):
        return reverse("necessidade-detail", args=[self.id])
    
class Categoria(models.Model):
    codigo_categoria = models.AutoField(primary_key=True)
    MATERIAL = 'Material'
    SERVICO = 'Serviço'
    CATEGORIA_CHOICES = [
        (MATERIAL, 'Material'),
        (SERVICO, 'Serviço'),
    ]
    tipo = models.CharField(max_length=8, choices=CATEGORIA_CHOICES)


    descricao = models.CharField(max_length=100, unique=True)

    class Meta:
        permissions = [('pode_criar_atualizar_categoria','Cria/Atualiza categoria'),('pode_deletar_categoria','Deleta categoria')]

    def __str__(self):
        return self.descricao
    
    def get_absolute_url(self):
        return reverse("categoria-detail", args=[self.codigo_categoria])