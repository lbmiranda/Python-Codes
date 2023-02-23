import datetime
from django.shortcuts import render, get_object_or_404
from .models import Livro,Autor,InstanciaLivro
from .forms import FormRenovaLivros
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

# Create your views here.

def index(request):
    
    num_livros = Livro.objects.all().count()    
    num_instancias = InstanciaLivro.objects.all().count()
    num_instancias_disponivel = InstanciaLivro.objects.filter(status__exact='d').count()
    num_autores = Autor.objects.count()    
    num_ensaio = Livro.objects.filter(titulo__icontains = 'ensaio').count()
    num_visitas = request.session.get('num_visitas',0)

    request.session['num_visitas'] = num_visitas +1

    context = {
        'num_livros': num_livros,
        'num_instancias': num_instancias,
        'num_instancias_disponivel': num_instancias_disponivel,
        'num_autores': num_autores,
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

class LivroEmprestadoPorUsuarioView(LoginRequiredMixin, generic.ListView):
    model = InstanciaLivro
    template_name = 'catalog/instancialivro_list.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            InstanciaLivro.objects.filter(emprestado_para=self.request.user)
            .filter(status__exact='e')
            .order_by('data_devolucao')
        )

class LivrosEmprestadosGeralView(LoginRequiredMixin, generic.ListView):
    model = InstanciaLivro
    template_name = 'catalog/livrosemprestados_list.html'
    paginate_by = 10

    def get_queryset(self):
       return (
            InstanciaLivro.objects.filter(status__exact='e')
            .order_by('emprestado_para')
        )

@login_required
@permission_required('catalog.pode_renovar_livro', raise_exception=True)
def renova_livro_bibliotecario(request, pk):
    
    instancia_livro = get_object_or_404(InstanciaLivro, pk = pk)

    if request.method == 'POST':
        form = FormRenovaLivros(request.POST)

        if form.is_valid():
            instancia_livro.data_devolucao = form.cleaned_data['data_renovacao']
            instancia_livro.save()

            return HttpResponseRedirect(reverse('livros-emprestados'))
    
    else:
        data_renovacao_proposta = datetime.date.today() + datetime.timedelta(weeks=3)
        form = FormRenovaLivros(initial={'data_renovacao': data_renovacao_proposta})

    context = {
        'form': form,
        'instancia_livro': instancia_livro,
    }

    return render(request, 'catalog/renova_livro_bibliotecario.html', context)

class AutorCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'catalog.pode_criar_atualizar_autor'
    model = Autor
    fields = ['nome','sobrenome','data_nascimento','data_morte']
    
class AutorUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'catalog.pode_criar_atualizar_autor'
    model = Autor
    fields = '__all__'

class AutorDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'catalog.pode_deletar_autor'
    model = Autor
    success_url = reverse_lazy('autores')

class CriarLivro(PermissionRequiredMixin,CreateView):
    permission_required = 'catalog.pode_criar_atualizar_livro'
    model = Livro
    fields = ['titulo','autor','sumario','isbn','genero','idioma']

class AtualizarLivro(PermissionRequiredMixin,UpdateView):
    permission_required = 'catalog.pode_criar_atualizar_livro'
    model = Livro
    fields = ['titulo','autor','sumario','isbn','genero','idioma']    

class DeletarLivro(PermissionRequiredMixin,DeleteView):
    permission_required = 'catalog.pode_deletar_livro'
    model = Livro
    success_url = reverse_lazy('livros')

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return HttpResponseRedirect('/catalog/erro')

