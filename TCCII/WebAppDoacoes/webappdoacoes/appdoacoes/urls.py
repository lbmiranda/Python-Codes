from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('entidades/', views.lista_entidades, name='entidades'),
    re_path(r'^entidades/(?P<pk>\d{14})/$',views.EmpresaEntidadeDetailView.as_view(),name='empresaentidade-detail'),
    path('materiais_servicos/', views.lista_materiais_servicos, name='materiais-servicos'),
    path('categorias/', views.CategoriaListView.as_view(),name='categoria-list'),
    path('categorias/criar/', views.CategoriaCreate.as_view(),name='categoria-create'),
    path('categorias/<int:pk>/', views.CategoriaDetailView.as_view(),name='categoria-detail'),
    path('categorias/<int:pk>/atualizar/', views.CategoriaUpdate.as_view(),name='categoria-update'),
    path('categorias/<int:pk>/deletar/', views.CategoriaDelete.as_view(),name='categoria-delete'),
]

#Urls para registro de usuário

urlpatterns += [
    path('registrar/', views.registrar_usuario, name='registrar'),    
]

#Urls para criação de instancias

urlpatterns += [
    path('criar_donativo/', views.DonativoCreate.as_view(), name='criar-donativo'),
    #path('cadastrar_necessidade/', views.criar_instanciamaterial, name='registrar-necessidade'),
]

