from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('entidades/', views.lista_entidades, name='entidades'),
    path('entidades/<str:pk>',views.EmpresaEntidadeDetailView.as_view(),name='empresaentidade-detail'),
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

