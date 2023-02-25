from django.test import TestCase

from catalog.models import Autor


class AutorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        Autor.objects.create(nome='Zé', sobrenome='das Couves')

    def test_nome_label(self):
        autor = Autor.objects.get(id=1)
        field_label = autor._meta.get_field('nome').verbose_name
        self.assertEqual(field_label, 'nome')

    def test_sobrenome_label(self):
        autor = Autor.objects.get(id=1)
        field_label = autor._meta.get_field('sobrenome').verbose_name
        self.assertEqual(field_label, 'sobrenome')

    def test_date_nascimento_label(self):
        autor = Autor.objects.get(id=1)
        field_label = autor._meta.get_field('data_nascimento').verbose_name
        self.assertEqual(field_label, 'data nascimento')

    def test_date_morte_label(self):
        autor = Autor.objects.get(id=1)
        field_label = autor._meta.get_field('data_morte').verbose_name
        self.assertEqual(field_label, 'Data da morte')

    def test_nome_max_length(self):
        autor = Autor.objects.get(id=1)
        max_length = autor._meta.get_field('nome').max_length
        self.assertEqual(max_length, 100)

    def test_sobrenome_max_length(self):
        autor = Autor.objects.get(id=1)
        max_length = autor._meta.get_field('sobrenome').max_length
        self.assertEqual(max_length, 100)

    def test_object_nome_separado_virgula_sobrenome(self):
        autor = Autor.objects.get(id=1)
        expected_object_name = '{0}, {1}'.format(autor.nome, autor.sobrenome)

        self.assertEqual(str(autor), expected_object_name)

    def test_get_absolute_url(self):
        autor = Autor.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(autor.get_absolute_url(), '/catalog/autor/1')
