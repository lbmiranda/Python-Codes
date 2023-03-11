from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('entidades/', views.lista_entidades, name='entidades'),
    path('entidades/<str:pk>',views.EmpresaEntidadeDetailView.as_view(),name='empresaentidade-detail'),
]

