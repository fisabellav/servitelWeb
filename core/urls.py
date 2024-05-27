from django.urls import path
from core import views

urlpatterns = [
    path ('', views.index, name='index'),
    path ('catalogo/', views.catalogo, name='catalogo'),
    path ('catalogo/producto/<id>', views.producto, name='producto'),
    path ('catalogo/<int:cameras>/', views.filter_by_cameras, name='filter-cameras'),
]