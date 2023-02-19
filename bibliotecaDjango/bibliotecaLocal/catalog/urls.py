from django.urls import path
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
]