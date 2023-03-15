from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.utils.translation import gettext_lazy as _ 



User = get_user_model()

class FormCriarUsuario(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','tipo_de_conta']





