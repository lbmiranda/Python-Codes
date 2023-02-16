from django.shortcuts import render
from .models import Livro,Autor,InstanciaLivro,Genero

# Create your views here.

def index(request):
    
    num_livros = Livro.objects.all().count()    
    num_instancias = InstanciaLivro.objects.all().count()
    num_instancias_disponivel = InstanciaLivro.objects.filter(status__exact='d').count()
    num_autores = Autor.objects.count()
    num_generos = Livro.objects.all().count()
    num_ensaio = Livro.objects.filter(titulo__icontains = 'ensaio').count()

    context = {
        'num_livros': num_livros,
        'num_instancias': num_instancias,
        'num_instancias_disponivel': num_instancias_disponivel,
        'num_autores': num_autores,
        'num_generos': num_generos,
        'num_ensaio': num_ensaio,
    }

    return render(request, 'index.html', context=context)


from django.views import generic

class LivroListView(generic.ListView):
    model = Livro 
        

class LivroDetalheView(generic.DetailView):
    model = Livro
     

class AutorListView(generic.ListView):
    model = Autor


class AutorDetalheView(generic.DetailView):
    model = Autor