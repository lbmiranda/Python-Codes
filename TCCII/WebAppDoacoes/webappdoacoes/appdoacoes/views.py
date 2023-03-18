from django.shortcuts import render, redirect,get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin,LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from .forms import FormCriarUsuario
# Create your views here.

from .models import EmpresaEntidade, EmpresaComunidade, PessoaComunidade, Donativo,InstanciaDonativo,Categoria,PerfilUsuario

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


@login_required
def perfil_usuario_update(request):
    usuario_logado = request.user
    perfil_usuario = get_object_or_404(PerfilUsuario, usuario=usuario_logado)
    context = {'perfil_usuario': perfil_usuario}
    return render(request,'perfil.html',context)
    

#Entidades ListView
def lista_entidades(request):
    lista_entidade = EmpresaEntidade.objects.all()
    context = {'lista_entidade': lista_entidade}
    return render(request, 'empresaentidade_list.html', context)

#Entidades DetailView
class EmpresaEntidadeDetailView(generic.DetailView):
    model = EmpresaEntidade
    template_name = 'empresaentidade_detail.html'
    context_object_name = 'empresaentidade'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registronecessidade_list = InstanciaDonativo.objects.filter(entidade=self.object)
        context['registronecessidade_list'] = registronecessidade_list
        return context

#Entidades Create-Update-Delete
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

#Donativos ListView
def lista_donativos(request):
    lista_donativos = Donativo.objects.all()
    context = {'lista_donativos': lista_donativos}
    return render(request, 'donativos_list.html', context)

#Donativos DetailView
class DonativoDetailView(generic.DetailView):
    model = Donativo

#Donativos Create-Update-Delete
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

#Categoria ListView
class CategoriaListView(generic.ListView):
    model = Categoria

#Categoria DetailView
class CategoriaDetailView(generic.DetailView):
    model = Categoria

#Categoria Create-Update-Delete
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

#InstanciaDonativo ListView
class RegistroNecessidadeListView(generic.ListView):
    model=InstanciaDonativo

#InstanciaDonativo DetailView
class RegistroNecessidadeDetailView(generic.DetailView):
    model=InstanciaDonativo

#InstanciaDonativo Create-Update-Delete
class RegistroNecessidadeCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'appdoacoes.pode_criar_atualizar_necessidade'
    model = InstanciaDonativo
    fields = ('donativo','entidade','quantidade')

    def test_func(self):
        instancia_donativo = self.get_object()
        return self.request.user == instancia_donativo.entidade.usuario_responsavel or self.request.user.is_staff

class RegistroNecessidadeUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'appdoacoes.pode_criar_atualizar_necessidade'    
    model = InstanciaDonativo
    fields = ('donativo','entidade','quantidade')

    def test_func(self):
        instancia_donativo = self.get_object()
        return self.request.user == instancia_donativo.entidade.usuario_responsavel or self.request.user.is_staff

class RegistroNecessidadeDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'appdoacoes.pode_deleter_necessidade'
    model = InstanciaDonativo
    success_url = reverse_lazy('necessidades-list')

    def test_func(self):
        instancia_donativo = self.get_object()
        return self.request.user == instancia_donativo.entidade.usuario_responsavel or self.request.user.is_staff

#Registro de usuário
def registrar_usuario(request):
    if request.method == 'POST':
        form = FormCriarUsuario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = FormCriarUsuario()
    return render(request,'registrar.html',{'form': form})