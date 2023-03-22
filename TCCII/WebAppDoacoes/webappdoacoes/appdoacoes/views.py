from django.shortcuts import render, redirect,get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin,LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from .forms import FormCriarUsuario, FormPerfilUsuario, FormEntidadeCreate,FormEmpresaComunidadeCreate,FormPessoaComunidadeCreate
from django.db.models import Q



from .models import EmpresaEntidade, EmpresaComunidade, PessoaComunidade, Donativo,InstanciaDonativo,Categoria,PerfilUsuario

def index(request):
    """Função para apresentar a página principal do aplicativo."""
    
    num_entidades = EmpresaEntidade.objects.all().count()
    num_publico = EmpresaComunidade.objects.all().count() + PessoaComunidade.objects.all().count()
    num_categorias = Categoria.objects.all().count()
    num_donativos = Donativo.objects.all().count()
    num_necessidades = InstanciaDonativo.objects.all().count()
    num_visitas_site = request.session.get('num_visitas_site',0)
    request.session['num_visitas_site'] = num_visitas_site+1
    
    context={
        'num_entidades': num_entidades, 
        'num_publico': num_publico,
        'num_visitas_site': num_visitas_site,
        'num_categorias': num_categorias,
        'num_donativos': num_donativos,
        'num_necessidades': num_necessidades,
    }
    
    return render(request,'index.html', context = context)

@login_required
def perfil_usuario(request):
    
    usuario_logado = request.user
    perfil_usuario = get_object_or_404(PerfilUsuario, usuario=usuario_logado)
    entidade_perfil = perfil_usuario.usuario.entidade
    pf_perfil = perfil_usuario.usuario.comunidade_pf
    pj_perfil = perfil_usuario.usuario.comunidade_pj
    
    
    form_atualizar_perfil = FormPerfilUsuario(request.POST or None, instance = perfil_usuario)
    form_criar_entidade = FormEntidadeCreate(request.POST or None, instance=EmpresaEntidade())
    form_criar_pf = FormPessoaComunidadeCreate(request.POST or None, instance = PessoaComunidade()) 
    form_criar_pj = FormEmpresaComunidadeCreate(request.POST or None, instance=EmpresaComunidade())
    
    if form_atualizar_perfil.is_valid():
        form_atualizar_perfil.save()

    if form_criar_entidade.is_valid():
        empresa_entidade = form_criar_entidade.save(commit=False)
        empresa_entidade.usuario_responsavel = usuario_logado                 
        empresa_entidade.save()
        perfil_usuario.usuario.entidade = empresa_entidade
        perfil_usuario.usuario.save()
    
    if form_criar_pf.is_valid():
        comunidade_pf = form_criar_pf.save(commit=False)
        perfil_usuario.usuario.comunidade_pf = comunidade_pf
        form_criar_pf.save()
        perfil_usuario.usuario.save()

    if form_criar_pj.is_valid():
        comunidade_pj = form_criar_pj.save(commit=False)
        perfil_usuario.usuario.comunidade_pj = comunidade_pj
        form_criar_pj.save()
        perfil_usuario.usuario.save()

    context = {
        'perfil_usuario': perfil_usuario,
        'form_atualizar_perfil': form_atualizar_perfil,
        'form_criar_entidade': form_criar_entidade,
        'form_criar_pf': form_criar_pf,
        'form_criar_pj': form_criar_pj,
        'entidade_perfil': entidade_perfil,
        'pj_perfil': pj_perfil,
        'pf_perfil': pf_perfil,
    }
    return render(request,'perfil.html',context)

#Entidades ListView
def lista_entidades(request):
    
    termo_pesquisado = request.GET.get('search', '')
    lista_entidade = EmpresaEntidade.objects.all()
    
    if termo_pesquisado:
        lista_entidade = lista_entidade.filter(
            Q(cnpj__icontains=termo_pesquisado) |
            Q(nome_fantasia__icontains=termo_pesquisado)            
        )

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

#Entidades Update-Delete
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
    
    termo_pesquisado = request.GET.get('search', '')
    tipo = request.GET.get('tipo', '')
    lista_donativos = Donativo.objects.all()    
    
    if tipo:
        lista_donativos = lista_donativos.filter(categoria__tipo=tipo)

    if termo_pesquisado:
        lista_donativos = lista_donativos.filter(
            Q(id__icontains=termo_pesquisado) |
            Q(descricao__icontains=termo_pesquisado) |
            Q(categoria__tipo__icontains=termo_pesquisado) |
            Q(unidade__icontains=termo_pesquisado)
        )


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

    def get_queryset(self):
            qs = super().get_queryset()

            # Filtrar por tipo
            tipo = self.request.GET.get('tipo')
            if tipo:
                qs = qs.filter(tipo=tipo)

            termo_pesquisado = self.request.GET.get('search')
            if termo_pesquisado:
                qs = qs.filter(
                    Q(descricao__icontains=termo_pesquisado) |
                    Q(codigo_categoria__icontains=termo_pesquisado) |
                    Q(tipo__icontains=termo_pesquisado)
                )

            return qs
    
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

    def get_queryset(self):
            qs = super().get_queryset()

            selecao = self.request.GET.get('selecao')
            if selecao == 'entidade':
                qs = qs.order_by('entidade')
            elif selecao == 'donativo':
                qs = qs.order_by('donativo')
            elif selecao == 'quantidade':
                qs = qs.order_by('quantidade')
            elif selecao == 'unidade':
                qs = qs.order_by('unidade')
            else:
                qs = qs


            termo_pesquisado = self.request.GET.get('search')
            if termo_pesquisado:
                qs = qs.filter(                    
                    Q(quantidade__icontains=termo_pesquisado) |
                    Q(entidade__cnpj__icontains=termo_pesquisado) |
                    Q(donativo__unidade__icontains=termo_pesquisado) |
                    Q(donativo__descricao__icontains=termo_pesquisado) 
                )

            return qs
    
#InstanciaDonativo DetailView
class RegistroNecessidadeDetailView(generic.DetailView):
    model=InstanciaDonativo

#InstanciaDonativo Create-Update-Delete
class RegistroNecessidadeCreate(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    permission_required = 'appdoacoes.pode_criar_atualizar_necessidade'
    model = InstanciaDonativo
    fields = ('donativo','entidade','quantidade')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_staff:
            entidade_queryset = EmpresaEntidade.objects.filter(usuario_responsavel=self.request.user)
        else:
            entidade_queryset = EmpresaEntidade.objects.all()    
        form.fields['entidade'].queryset = entidade_queryset
        return form

    def test_func(self):
        instancia_donativo = self.get_object()
        return self.request.user == instancia_donativo.entidade.usuario_responsavel or self.request.user.is_staff
    
    def form_valid(self, form):    
        donativo = form.cleaned_data['donativo']
        entidade = form.cleaned_data['entidade']
        quantidade = form.cleaned_data['quantidade']

        try:
            instancia_donativo = InstanciaDonativo.objects.get(donativo=donativo, entidade=entidade)
        except InstanciaDonativo.DoesNotExist:            
            return super().form_valid(form)

        instancia_donativo.quantidade += quantidade
        instancia_donativo.save()

        return redirect(instancia_donativo)

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
            return redirect(('login')) 
    else:
        form = FormCriarUsuario()
    return render(request,'registrar.html',{'form': form})

