import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class FormRenovaLivros(forms.Form):

    data_renovacao = forms.DateField(help_text='Informe uma data entre hoje e até quatro semanas (padrão - 3 semanas)', label='Nova data de devolução')

    def clean_data_renovacao(self):
        data = self.cleaned_data['data_renovacao']

        if data < datetime.date.today():
            raise ValidationError(_('Data de renovação inválida - renovação no passado'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Data de renovação inválida - renovação em prazo maior que quatro semanas'))

        return data

        

