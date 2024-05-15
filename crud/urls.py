from django.urls import path
from crud import views

urlpatterns = [
    path ('form/', views.form, name='form'),
]