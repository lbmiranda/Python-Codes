from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('livros/', views.LivroListView.as_view(), name = 'livros'),
    path('livro/<int:pk>/', views.LivroDetalheView.as_view(), name = 'livro-detail'),
    path('autores/', views.AutorListView.as_view(), name = 'autores'),
    path('autor/<int:pk>', views.AutorDetalheView.as_view(), name = 'autor-detail'),
    path('meuslivros/',views.LivroEmprestadoPorUsuarioView.as_view(), name='meus-emprestados'),
    path('livrosemprestados/', views.LivrosEmprestadosGeralView.as_view(), name='livros-emprestados'),
    path('livro/<uuid:pk>/renova', views.renova_livro_bibliotecario, name = 'renova-livro-bibliotecario'),
    path('autor/criar/', views.AutorCreate.as_view(), name = 'autor-create'),
    path('autor/<int:pk>/atualizar/', views.AutorUpdate.as_view(), name = 'autor-update'),
    path('autor/<int:pk>/deletar/', views.AutorDelete.as_view(), name = 'autor-delete'),
    path('livro/criar/', views.CriarLivro.as_view(), name = 'livro-create'),
    path('livro/<int:pk>/atualizar/', views.AtualizarLivro.as_view(), name = 'livro-update'),
    path('livro/<int:pk>/deletar/', views.DeletarLivro.as_view(), name = 'livro-delete'),
    path('erro/', TemplateView.as_view(template_name='erro_delete.html'), name='erro-deletar'),
]