from django.test import TestCase


from catalog.models import Autor
from django.urls import reverse


class AutorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create autors for pagination tests
        num_autores = 13
        for autor_id in range(num_autores):
            Autor.objects.create(nome='Zé {0}'.format(autor_id),
                                  sobrenome='das Couve {0}'.format(autor_id))

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/autores/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('autores'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('autores'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/autor_list.html')


import datetime
from django.utils import timezone

from catalog.models import InstanciaLivro, Livro, Genero, Idioma
from django.contrib.auth.models import User  # Required to assign User as a borrower


class LivrosEmprestadosporUsuarioListViewTest(TestCase):

    def setUp(self):
        # Criar dois usuários
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Criar um livro
        test_autor = Autor.objects.create(nome='Bilisbau', sobrenome='Silver')
        #test_genero = Genero.objects.create(name='Matemática')
        test_idioma = Idioma.objects.create(name='Polonês')
        test_livro = Livro.objects.create(
            titulo='Titulo do Livro',
            sumario='Sumario do Livro',
            isbn='ABCDEFG',
            autor=test_autor,
            idioma=test_idioma,
            
        )
        # Criar genero
        genero_objeto_para_livro = Genero.objects.all()
        test_livro.genero.set(genero_objeto_para_livro)
        test_livro.save()

        # Criar 30 objetos de InstanciaLivro 
        numero_copias = 30
        for copia_livro in range(numero_copias):
            data_devolucao = timezone.now() + datetime.timedelta(days=copia_livro % 5)
            if copia_livro % 2:
                emprestado_para = test_user1
            else:
                emprestado_para = test_user2
            status = 'm'
            InstanciaLivro.objects.create(livro=test_livro, edicao='Sei lá, 2016', data_devolucao=data_devolucao,
                                        emprestado_para=emprestado_para, status=status)




 