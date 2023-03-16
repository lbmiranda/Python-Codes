from django.urls import path, re_path
from . import views

#Página principal

urlpatterns = [
    path('', views.index, name='index'), 
]

#Listas e views detalhadas

urlpatterns += [
    path('entidades/', views.lista_entidades, name='entidade-list'),
    re_path(r'^entidades/(?P<pk>\d{14})/$',views.EmpresaEntidadeDetailView.as_view(),name='entidade-detail'),
    path('donativos/', views.lista_donativos, name='donativo-list'),
    path('donativos/<int:pk>/', views.DonativoDetailView.as_view(), name='donativo-detail'),
    path('categorias/', views.CategoriaListView.as_view(),name='categoria-list'),
    path('categorias/<int:pk>/', views.CategoriaDetailView.as_view(),name='categoria-detail'),
    path('necessidades/', views.RegistroNecessidadeListView.as_view(),name='necessidades-list'),
    path('necessidades/<int:pk>/', views.RegistroNecessidadeDetailView.as_view(),name='necessidade-detail'),
    path('perfil/<int:usuario>/', views.PerfilUsuarioDetailView.as_view(),name='perfil-detail'),    
]

#Urls para registro de usuário

urlpatterns += [
    path('registrar/', views.registrar_usuario, name='registrar'),    
]

#Urls para criar, atualizar e deletar instancias

urlpatterns += [
    path('donativos/criar/', views.DonativoCreate.as_view(), name='donativo-create'),
    path('donativos/<int:pk>/atualizar/', views.DonativoUpdate.as_view(), name='donativo-update'),
    path('donativos/<int:pk>/deletar/', views.DonativoDelete.as_view(), name='donativo-delete'),
    path('entidades/criar/', views.EmpresaEntidadeCreate.as_view(), name='entidade-create'),
    re_path(r'^entidades/(?P<pk>\d{14})/$/atualizar',views.EmpresaEntidadeUpdate.as_view(),name='entidade-update'),
    re_path(r'^entidades/(?P<pk>\d{14})/$/deletar',views.EmpresaEntidadeDelete.as_view(),name='entidade-delete'),
    path('categorias/criar/', views.CategoriaCreate.as_view(),name='categoria-create'),    
    path('categorias/<int:pk>/atualizar/', views.CategoriaUpdate.as_view(),name='categoria-update'),
    path('categorias/<int:pk>/deletar/', views.CategoriaDelete.as_view(),name='categoria-delete'),
    path('necessidades/criar/', views.RegistroNecessidadeCreate.as_view(),name='necessidade-create'),    
    path('necessidades/<int:pk>/atualizar/', views.RegistroNecessidadeUpdate.as_view(),name='necessidade-update'),
    path('necessidades/<int:pk>/deletar/', views.RegistroNecessidadeDelete.as_view(),name='necessidade-delete'),
    path('perfil/<int:usuario>/atualizar', views.perfil_usuario_update,name='perfil-update'),
]

