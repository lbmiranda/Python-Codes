from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import User, PerfilUsuario,EmpresaEntidade, PessoaComunidade,EmpresaComunidade
from django.utils.translation import gettext_lazy as _ 



User = get_user_model()

class FormCriarUsuario(UserCreationForm):

    error_messages = {
        'password_mismatch': "As senhas não coincidem.",
        'password_too_short': "Sua senha precisa conter pelo menos 8 caracteres.",
        'password_common_words': "Sua senha não pode ser uma senha comumente utilizada.",
        'password_entirely_numeric': "Sua senha não pode ser inteiramente numérica."
    }      

    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Escolha um nome de usuário com até 30 caracteres'})
    )


    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Informe seu e-mail'}))

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Informe sua senha'})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme sua senha'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Usuário'
        self.fields['email'].label = 'E-mail'
        self.fields['tipo_de_conta'].label = 'Tipo de conta'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmar senha'      

    class Meta:
        model = User
        fields = ('username', 'email', 'tipo_de_conta', 'password1', 'password2' )
        help_texts = {''}

class FormPerfilUsuario(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['detalhes'] 

class FormEntidadeCreate(forms.ModelForm):
    class Meta:
        model = EmpresaEntidade    
        permission_required = 'appdoacoes.pode_criar_atualizar_entidade'    
        fields = ['nome_fantasia', 'cnpj', 'email', 'logradouro', 'numero', 'bairro', 'cidade', 'estado']

class FormEmpresaComunidadeCreate(forms.ModelForm):
    class Meta:
        model = EmpresaComunidade
        fields = ['cnpj','nome_fantasia']

class FormPessoaComunidadeCreate(forms.ModelForm):
    class Meta:
        model = PessoaComunidade
        fields = ['cpf','nome','sobrenome']


