from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('livros/', views.LivroListView.as_view(), name = 'livros'),
    path('livro/<int:pk>', views.LivroDetalheView.as_view(), name = 'detalhe-livro'),
]