from django.urls import path
from core import views
from crud.views import update_order_status

urlpatterns = [
    path ('', views.index, name='index'),
    path ('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/filter/', views.filter_products, name='filter_products'),
    path ('accesorios/', views.accesorios, name='accesorios'),
    path ('contacto/', views.contacto, name='contacto'),
    path ('producto/<id>', views.producto, name='producto'),
    path ('neworder/', views.new_order_wishlist, name='new-order-wishlist'),
    path ('neworder/<id>', views.new_order, name='new-order'),
    path('orders/<int:id>/', views.order_detail, name='myorder-detail'),
    path('orders/', views.order_list, name='my-orders'),
    path('editar-perfil/<id>', views.editar_perfil, name='editar-perfil'),
    path('about/', views.about, name='about'),
    path('order/update-status/<int:order_id>/<str:status>/', update_order_status, name='update-order-status')
]