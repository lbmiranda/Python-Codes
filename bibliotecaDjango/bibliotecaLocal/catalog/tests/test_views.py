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

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('autores'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['autor_list']), 10)

    def test_lists_all_autors(self):
        response = self.client.get(reverse('autores')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['autor_list']), 3)


import datetime
from django.utils import timezone

from catalog.models import InstanciaLivro, Livro, Genero, Idioma
from django.contrib.auth.models import User  # Required to assign User as a borrower


class LoanedInstanciaLivrosByUserListViewTest(TestCase):

    def setUp(self):
        # Criar dois usuários
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Criar um livro
        test_autor = Autor.objects.create(nome='Bilisbau', sobrenome='Silver')
        test_genero = Genero.objects.create(name='Matemática')
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

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('meus-emprestados'))
        self.assertRedirects(response, '/contas/login/?next=/catalog/meuslivros/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('meus-emprestados'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'catalog/livrosemprestados_list.html')

    def test_only_borrowed_livros_in_list(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('meus-emprestados'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check that initially we don't have any livros in list (none on loan)
        self.assertTrue('instancialivro_list' in response.context)
        self.assertEqual(len(response.context['instancialivro_list']), 0)

        # Now change all livros to be on loan
        get_ten_livros = InstanciaLivro.objects.all()[:10]

        for copy in get_ten_livros:
            copy.status = 'e'
            copy.save()


        response = self.client.get(reverse('meus-emprestados'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        self.assertTrue('instancialivro_list' in response.context)


        for livroitem in response.context['instancialivro_list']:
            self.assertEqual(response.context['user'], livroitem.borrower)
            self.assertEqual(livroitem.status, 'e')

    def test_pages_paginated_to_ten(self):


        for copy in InstanciaLivro.objects.all():
            copy.status = 'e'
            copy.save()

        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('meus-emprestados'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Confirm that only 10 items are displayed due to pagination
        # (if pagination not enabled, there would be 15 returned)
        self.assertEqual(len(response.context['instancialivro_list']), 10)

    def test_pages_ordered_by_due_date(self):

        # Change all livros to be on loan
        for copy in InstanciaLivro.objects.all():
            copy.status = 'e'
            copy.save()

        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('meus-emprestados'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Confirm that of the items, only 10 are displayed due to pagination.
        self.assertEqual(len(response.context['instancialivro_list']), 10)

        last_date = 0
        for copy in response.context['instancialivro_list']:
            if last_date == 0:
                last_date = copy.data_devolucao
            else:
                self.assertTrue(last_date <= copy.data_devolucao)


from django.contrib.auth.models import Permission  # Required to grant the permission needed to set a livro as returned.


# class RenewInstanciaLivrosViewTest(TestCase):

#     def setUp(self):
#         # Create a user
#         test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
#         test_user1.save()

#         test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
#         test_user2.save()
#         permission = Permission.objects.get(name='Set livro as returned')
#         test_user2.user_permissions.add(permission)
#         test_user2.save()

#         # Create a livro
#         test_autor = Autor.objects.create(nome='John', sobrenome='Smith')
#         test_genre = Genero.objects.create(name='Fantasy')
#         test_language = Idioma.objects.create(name='English')
#         test_livro = Livro.objects.create(title='Livro Title', summary='My livro summary',
#                                         isbn='ABCDEFG', autor=test_autor, language=test_language,)
#         # Create genre as a post-step
#         genre_objects_for_livro = Genero.objects.all()
#         test_livro.genre.set(genre_objects_for_livro)
#         test_livro.save()

#         # Create a InstanciaLivro object for test_user1
#         data_devolucao = datetime.date.today() + datetime.timedelta(days=5)
#         self.test_livroinstance1 = InstanciaLivro.objects.create(livro=test_livro,
#                                                               imprint='Unlikely Imprint, 2016', data_devolucao=data_devolucao,
#                                                               borrower=test_user1, status='o')

#         # Create a InstanciaLivro object for test_user2
#         data_devolucao = datetime.date.today() + datetime.timedelta(days=5)
#         self.test_livroinstance2 = InstanciaLivro.objects.create(livro=test_livro, imprint='Unlikely Imprint, 2016',
#                                                               data_devolucao=data_devolucao, borrower=test_user2, status='o')

#     def test_redirect_if_not_logged_in(self):
#         response = self.client.get(reverse('renew-livro-librarian', kwargs={'pk': self.test_livroinstance1.pk}))
#         # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(response.url.startswith('/accounts/login/'))

#     def test_forbidden_if_logged_in_but_not_correct_permission(self):
#         login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
#         response = self.client.get(reverse('renew-livro-librarian', kwargs={'pk': self.test_livroinstance1.pk}))
#         self.assertEqual(response.status_code, 403)


#     def test_logged_in_with_permission_borrowed_livro(self):
#         login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
#         response = self.client.get(reverse('renew-livro-librarian', kwargs={'pk': self.test_livroinstance2.pk}))

#         # Check that it lets us login - this is our livro and we have the right permissions.
#         self.assertEqual(response.status_code, 200)

#     def test_logged_in_with_permission_another_users_borrowed_livro(self):
#         login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
#         response = self.client.get(reverse('renew-livro-librarian', kwargs={'pk': self.test_livroinstance1.pk}))

#         # Check that it lets us login. We're a librarian, so we can view any users livro
#         self.assertEqual(response.status_code, 200)

#     def test_uses_correct_template(self):
#         login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
#         response = self.client.get(reverse('renew-livro-librarian', kwargs={'pk': self.test_livroinstance1.pk}))
#         self.assertEqual(response.status_code, 200)

#         # Check we used correct template
#         self.assertTemplateUsed(response, 'catalog/livro_renew_librarian.html')

#     def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
#         login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
#         response = self.client.get(reverse('renew-livro-librarian', kwargs={'pk': self.test_livroinstance1.pk}))
#         self.assertEqual(response.status_code, 200)

#         date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
#         self.assertEqual(response.context['form'].initial['renewal_date'], date_3_weeks_in_future)

#     def test_form_invalid_renewal_date_past(self):
#         login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')

#         date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
#         response = self.client.post(reverse('renew-livro-librarian', kwargs={'pk': self.test_livroinstance1.pk}),
#                                     {'renewal_date': date_in_past})
#         self.assertEqual(response.status_code, 200)
#         self.assertFormError(response, 'form', 'renewal_date', 'Invalid date - renewal in past')

#     def test_form_invalid_renewal_date_future(self):
#         login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        
#         invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
#         response = self.client.post(reverse('renew-livro-librarian', kwargs={'pk': self.test_livroinstance1.pk}),
#                                     {'renewal_date': invalid_date_in_future})
#         self.assertEqual(response.status_code, 200)
#         self.assertFormError(response, 'form', 'renewal_date', 'Invalid date - renewal more than 4 weeks ahead')

#     def test_redirects_to_all_borrowed_livro_list_on_success(self):
#         login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
#         valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)
#         response = self.client.post(reverse('renew-livro-librarian', kwargs={'pk': self.test_livroinstance1.pk}),
#                                     {'renewal_date': valid_date_in_future})
#         self.assertRedirects(response, reverse('all-borrowed'))

#     def test_HTTP404_for_invalid_livro_if_logged_in(self):
#         import uuid
#         test_uid = uuid.uuid4()  # unlikely UID to match our livroinstance!
#         login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
#         response = self.client.get(reverse('renew-livro-librarian', kwargs={'pk': test_uid}))
#         self.assertEqual(response.status_code, 404)


# class AutorCreateViewTest(TestCase):
#     """Test case for the AutorCreate view (Created as Challenge)."""

#     def setUp(self):
#         # Create a user
#         test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
#         test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

#         test_user1.save()
#         test_user2.save()

#         permission = Permission.objects.get(name='Set livro as returned')
#         test_user2.user_permissions.add(permission)
#         test_user2.save()

#         # Create a livro
#         test_autor = Autor.objects.create(nome='John', sobrenome='Smith')

#     def test_redirect_if_not_logged_in(self):
#         response = self.client.get(reverse('autor-create'))
#         self.assertRedirects(response, '/accounts/login/?next=/catalog/autor/create/')

#     def test_forbidden_if_logged_in_but_not_correct_permission(self):
#         login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
#         response = self.client.get(reverse('autor-create'))
#         self.assertEqual(response.status_code, 403)

#     def test_logged_in_with_permission(self):
#         login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
#         response = self.client.get(reverse('autor-create'))
#         self.assertEqual(response.status_code, 200)

#     def test_uses_correct_template(self):
#         login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
#         response = self.client.get(reverse('autor-create'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'catalog/autor_form.html')

#     def test_form_date_of_death_initially_set_to_expected_date(self):
#         login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
#         response = self.client.get(reverse('autor-create'))
#         self.assertEqual(response.status_code, 200)

#         expected_initial_date = datetime.date(2020, 6, 11)
#         response_date = response.context['form'].initial['date_of_death']
#         response_date = datetime.datetime.strptime(response_date, "%d/%m/%Y").date()
#         self.assertEqual(response_date, expected_initial_date)

#     def test_redirects_to_detail_view_on_success(self):
#         login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
#         response = self.client.post(reverse('autor-create'),
#                                     {'nome': 'Christian Name', 'sobrenome': 'Surname'})
#         # Manually check redirect because we don't know what autor was created
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(response.url.startswith('/catalog/autor/'))