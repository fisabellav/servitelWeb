from django.urls import path
from core import views

urlpatterns = [
    path ('', views.index, name='index'),
    path ('catalogo/', views.catalogo, name='catalogo'),
    path ('contacto/', views.contacto, name='contacto'),
    path ('catalogo/producto/<id>', views.producto, name='producto'),
    path ('catalogo/<int:cameras>/', views.filter_by_cameras, name='filter-cameras'),
    path('cargar_comunas_rm_desde_api/', views.cargar_comunas_rm_desde_api, name='cargar_comunas_rm_desde_api'),
]