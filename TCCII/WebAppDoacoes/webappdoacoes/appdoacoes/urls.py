from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('entidades/', views.lista_entidades, name='entidades'),
    re_path(r'^entidades/(?P<pk>\d{14})/$',views.EmpresaEntidadeDetailView.as_view(),name='empresaentidade-detail'),
    path('materiais_servicos/', views.lista_materiais_servicos, name='materiais-servicos'),
]

#Urls para registro de usuário

urlpatterns += [
    path('registrar/', views.registrar_usuario, name='registrar'),
]

#Urls para criação de instancias

urlpatterns += [
    #path('cadastrar_necessidade/', views.criar_instanciamaterial, name='registrar-necessidade'),
]

