from django.db import models
from crud.models import Product

class Comuna(models.Model):
    comuna = models.CharField(verbose_name='COMUNA', max_length=100)

    def __str__(self):
        return self.comuna

class Solicitud(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('SE', 'Sin especificar'),
    ]

    name  = models.CharField(verbose_name='NOMBRE', max_length=50)
    last_name =  models.CharField(verbose_name='APELLIDO', max_length=50)
    birthday = models.DateField(verbose_name='FECHA DE NACIMIENTO')
    phone_number = models.CharField(verbose_name='TELÉFONO', unique=True, max_length=15)
    gender = models.CharField(verbose_name='GÉNERO', max_length=2, choices=GENERO_CHOICES)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, verbose_name='COMUNA')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='PRODUCTO')

    class Meta:
        verbose_name = 'solicitud'
        verbose_name_plural = 'solicitudes'
        ordering = ['last_name']

    def __str__(self) -> str:
        return f"{self.name} {self.last_name}"
