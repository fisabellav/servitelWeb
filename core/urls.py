from django.urls import path
from core import views

urlpatterns = [
    path ('', views.index, name='index'),
    path ('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/filter/', views.filter_products, name='filter_products'),
    path ('contacto/', views.contacto, name='contacto'),
    path ('producto/<id>', views.producto, name='producto'),
    path('cargar_comunas_rm_desde_api/', views.cargar_comunas_rm_desde_api, name='cargar_comunas_rm_desde_api'),
    path('editar-perfil', views.editar_perfil, name='editar-perfil'),
]