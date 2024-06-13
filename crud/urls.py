from django.urls import path
from crud import views

urlpatterns = [
    path ('product-list/', views.product_list, name='product-list'),
    path ('add-product/', views.add_product, name='add-product'),
    path('product-list/delete/<id>', views.productlist_delete, name='productlist-delete'),
    path('product-list/edit/<id>', views.productlist_edit, name='productlist-edit'),
]