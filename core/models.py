from django.db import models
from crud.models import Product
from login.models import User



class SolicitudProducto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'solicitud producto'
        verbose_name_plural = 'solicitudes productos'

    def __str__(self):
        return f"{self.user} - {self.product}"