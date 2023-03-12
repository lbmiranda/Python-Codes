from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import User, InstanciaMaterial
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _ 

User = get_user_model()


class FormCriarUsuario(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email']


# class FormCadastrarMaterial(forms.Form):

#     def validacao_positivo(valor):
#         if valor < 0:
#             raise ValidationError('A quantidade deve ser positiva.')

#     quantidade = forms.IntegerField(validators=[validacao_positivo])
    

#     class Meta:
#         model = InstanciaMaterial


