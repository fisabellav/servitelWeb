from django.urls import path
from crud import views

urlpatterns = [
    path ('product-list/', views.product_list, name='product-list'),
    path ('add-product/', views.add_product, name='add-product'),
    path ('order-list/', views.order_list, name='order-list'),
    path('order/<int:id>/', views.order_detail, name='order-detail'),
    path('product-list/delete/<id>', views.productlist_delete, name='productlist-delete'),
    path('product-list/edit/<id>', views.productlist_edit, name='productlist-edit'),
    path('product-list/detail/<id>', views.product_detail, name='product-detail'),
]