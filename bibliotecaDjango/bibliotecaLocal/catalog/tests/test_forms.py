from django.test import TestCase
import datetime
from catalog.forms import FormRenovaLivros


class FormRenovaLivrosTest(TestCase):

    def test_renova_form_data_no_passado(self):
        
        data = datetime.date.today() - datetime.timedelta(days=1)
        form = FormRenovaLivros(data={'data_renovacao': data})
        self.assertFalse(form.is_valid())

    def test_renova_form_data_futuro_distante(self):
        
        data = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = FormRenovaLivros(data={'data_renovacao': data})
        self.assertFalse(form.is_valid())

    def test_renova_form_data_hoje(self):
        data = datetime.date.today()
        form = FormRenovaLivros(data={'data_renovacao': data})
        self.assertTrue(form.is_valid())

    def test_renova_form_data_max(self):
        data = datetime.date.today() + datetime.timedelta(weeks=4)
        form = FormRenovaLivros(data={'data_renovacao': data})
        self.assertTrue(form.is_valid())

    def test_renova_form_label_campo_data(self):
        form = FormRenovaLivros()
        self.assertTrue(
            form.fields['data_renovacao'].label is None or
            form.fields['data_renovacao'].label == 'Nova data de devolução')

    def test_renova_form_campo_texto_ajuda_da_data(self):
        form = FormRenovaLivros()
        self.assertEqual(
            form.fields['data_renovacao'].help_text,
            'Informe uma data entre hoje e até quatro semanas (padrão - 3 semanas)')