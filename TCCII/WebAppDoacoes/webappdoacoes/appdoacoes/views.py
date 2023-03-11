from django.shortcuts import render
from django.views import generic

# Create your views here.

from .models import EmpresaEntidade, EmpresaComunidade, PessoaComunidade, DonativoMaterialOuServico,InstanciaMaterial

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
        
    

def lista_entidades(request):
    lista_entidade = EmpresaEntidade.objects.all()
    context = {'lista_entidade': lista_entidade}
    return render(request, 'empresaentidade_list.html', context)

class EmpresaEntidadeDetailView(generic.DetailView):
    model = EmpresaEntidade
    template_name = 'empresaentidade_detail.html'
    context_object_name = 'empresaentidade'