from django import forms
from django.forms import ModelForm
from .models import *

class SolicitudProductoForm(forms.ModelForm):
    class Meta:
        model = SolicitudProducto
        fields = ['user', 'product', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '1', 
                'max': '100',  # Puedes ajustar estos valores según tus necesidades
                'placeholder': 'Cantidad',
                'id': 'cantidad-seleccionada',  # Agregamos el ID para vincularlo con el input existente
                'disabled': '',  # Marcamos como deshabilitado, como está en tu ejemplo HTML
            }),
        }