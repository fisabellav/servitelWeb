from django import forms
from django.forms import ModelForm
from .models import *

class ProductForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'resize: none; height:80px'})
    )

    class Meta:
        model = Product
        fields = ['product', 'description', 'cameras', 'channels','price', 'image', 'category']
        widgets = {
            'product': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'cameras': forms.NumberInput(attrs={'class': 'form-control'}),
            'channels': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }