from django import forms
from django.forms import ModelForm
from .models import *

class SolicitudForm(ModelForm):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('SE', 'Sin especificar'),
    ]
    
    gender = forms.ChoiceField(choices=GENERO_CHOICES, label='Género', widget=forms.Select(attrs={'class': 'form-select', 'id': 'genero-select'}))

    class Meta:
        model = Solicitud
        fields = [
            'name',
            'last_name',
            'birthday',
            'phone_number',
            'comuna',
            'gender',  # Agregar el campo de género al formulario
        ]
        labels = {
            'name': 'Nombre',
            'last_name': 'Apellido',
            'birthday': 'Fecha de nacimiento',
            'phone_number': 'Teléfono',
            'comuna': 'Comuna',
            'gender': 'Género',  # Etiqueta para el campo de género
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre', 'id': 'idNombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido', 'id': 'idApellido'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'idFecha_nac'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '9 1234 5678', 'type': 'tel', 'id': 'idFono'}),
            'comuna': forms.Select(attrs={'class': 'form-select', 'id': 'comuna-select'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'id': 'genero-select'}),  # Widget para el campo de género
        }
