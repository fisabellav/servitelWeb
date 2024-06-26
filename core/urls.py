from django.urls import path
from core import views

urlpatterns = [
    path ('', views.index, name='index'),
    path ('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/filter/', views.filter_products, name='filter_products'),
    path ('contacto/', views.contacto, name='contacto'),
    path ('producto/<id>', views.producto, name='producto'),
    
    path('editar-perfil', views.editar_perfil, name='editar-perfil'),
]