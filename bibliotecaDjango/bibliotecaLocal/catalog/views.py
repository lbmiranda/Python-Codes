from django.shortcuts import render
from .models import Livro,Autor,InstanciaLivro,Genero
from django.views import generic

# Create your views here.

def index(request):
    
    num_livros = Livro.objects.all().count()    
    num_instancias = InstanciaLivro.objects.all().count()
    num_instancias_disponivel = InstanciaLivro.objects.filter(status__exact='d').count()
    num_autores = Autor.objects.count()
    num_generos = Livro.objects.all().count()
    num_ensaio = Livro.objects.filter(titulo__icontains = 'ensaio').count()
    num_visitas = request.session.get('num_visitas',0)

    request.session['num_visitas'] = num_visitas +1

    context = {
        'num_livros': num_livros,
        'num_instancias': num_instancias,
        'num_instancias_disponivel': num_instancias_disponivel,
        'num_autores': num_autores,
        'num_generos': num_generos,
        'num_ensaio': num_ensaio,
        'num_visitas': num_visitas,
    }

    return render(request, 'index.html', context=context)

class LivroListView(generic.ListView):
    model = Livro     

class LivroDetalheView(generic.DetailView):
    model = Livro
    paginate_by = 10
     
class AutorListView(generic.ListView):
    model = Autor

class AutorDetalheView(generic.DetailView):
    model = Autor

