from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from .forms import FormCriarUsuario
# Create your views here.

from .models import EmpresaEntidade, EmpresaComunidade, PessoaComunidade, Donativo,InstanciaDonativo,Categoria

def index(request):
    """Função para apresentar a página principal do aplicativo."""
    
    num_entidades = EmpresaEntidade.objects.all().count()
    num_publico = EmpresaComunidade.objects.all().count() + PessoaComunidade.objects.all().count()
    num_visitas_site = request.session.get('num_visitas_site',0)
    request.session['num_visitas_site'] = num_visitas_site+1
    
    context={
        'num_entidades': num_entidades, 
        'num_publico': num_publico,
        'num_visitas_site': num_visitas_site,
    }
    
    return render(request,'index.html', context = context)

#Entidades ListView
def lista_entidades(request):
    lista_entidade = EmpresaEntidade.objects.all()
    context = {'lista_entidade': lista_entidade}
    return render(request, 'empresaentidade_list.html', context)

class EmpresaEntidadeDetailView(generic.DetailView):
    model = EmpresaEntidade
    template_name = 'empresaentidade_detail.html'
    context_object_name = 'empresaentidade'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instanciadonativos_list = InstanciaDonativo.objects.filter(entidade=self.object)
        context['instanciadonativos_list'] = instanciadonativos_list
        return context

#Donativos ListView
def lista_donativos(request):
    lista_donativos = Donativo.objects.all()
    context = {'lista_donativos': lista_donativos}
    return render(request, 'donativos_list.html', context)

class DonativoDetailView(generic.DetailView):
    model = Donativo

class CategoriaListView(generic.ListView):
    model = Categoria

class CategoriaDetailView(generic.DetailView):
    model = Categoria

def registrar_usuario(request):
    if request.method == 'POST':
        form = FormCriarUsuario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = FormCriarUsuario()
    return render(request,'registrar.html',{'form': form})

class DonativoCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'appdoacoes.pode_criar_atualizar_donativo'
    model = Donativo
    fields = ('descricao','categoria','unidade')

class DonativoUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'appdoacoes.pode_criar_atualizar_donativo'
    model = Donativo
    fields = ('descricao','categoria','unidade')

class DonativoDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'appdoacoes.pode_deletar_donativo'
    model = Donativo
    success_url = reverse_lazy('donativo-list')

class CategoriaCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'appdoacoes.pode_criar_atualizar_categoria'
    model = Categoria
    fields = ('tipo','descricao')

class CategoriaUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'appdoacoes.pode_criar_atualizar_categoria'
    model = Categoria
    fields = ('tipo','descricao')
    success_url = reverse_lazy('categoria-list')

class CategoriaDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'appdoacoes.pode_criar_atualizar_categoria'
    model = Categoria
    success_url = reverse_lazy('categoria-list')

class RegistroNecessidadeCreate(PermissionRequiredMixin,CreateView):
    pass

class RegistroNecessidadeUpdate(PermissionRequiredMixin,UpdateView):
    pass

class RegistroNecessidadeDelete(PermissionRequiredMixin,DeleteView):
    pass

class EmpresaEntidadeCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'appdoacoes.pode_criar_atualizar_entidade'
    model = EmpresaEntidade
    fields = ['nome_fantasia', 'cnpj', 'email', 'logradouro', 'numero', 'bairro', 'cidade', 'estado']

    def form_valid(self, form):
        form.instance.usuario_responsavel = self.request.user
        return super().form_valid(form)

class EmpresaEntidadeUpdate(UserPassesTestMixin, PermissionRequiredMixin,UpdateView):
    permission_required = 'appdoacoes.pode_criar_atualizar_entidade'
    model = EmpresaEntidade
    fields = ['nome_fantasia', 'cnpj', 'email', 'logradouro', 'numero', 'bairro', 'cidade', 'estado']

    def test_func(self):
        empresa_entidade = self.get_object()
        return self.request.user == empresa_entidade.usuario_responsavel or self.request.user.is_staff

class EmpresaEntidadeDelete(UserPassesTestMixin,PermissionRequiredMixin,DeleteView):
    permission_required = 'appdoacoes.pode_deleter_entidade'
    model = Categoria
    success_url = reverse_lazy('entidades')

    def test_func(self):
        empresa_entidade = self.get_object()
        return self.request.user == empresa_entidade.usuario_responsavel or self.request.user.is_staff