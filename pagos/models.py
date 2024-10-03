from django.db import models
from core.models import Order

# Create your models here.
class Payment(models.Model):
    payment_number = models.PositiveIntegerField(verbose_name='Número de cuota')
    order = models.ForeignKey(Order, verbose_name='Pedido', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name='Monto pagado')
    payment_date = models.DateField(verbose_name='Fecha de pago')
    created_at = models.DateTimeField(verbose_name='Fecha registro',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Fecha actualización',auto_now=True)
    comments = models.TextField(verbose_name='Comentarios', blank=True, null=True)

    class Meta:
        verbose_name = 'Pago cuotas'
        verbose_name_plural = 'Pagos cuotas'

    def __str__(self):
        return f"{self.order}-{self.product}"


class Client(models.Model):
    rut =  models.CharField(verbose_name='Rut', max_length=12, null=True)
    name = models.CharField(verbose_name='Nombre', max_length=50)
    last_name = models.CharField(verbose_name='Apellido', max_length=50)
    second_last_name = models.CharField(verbose_name='Segundo Apellido', max_length=50)
    phone = models.CharField(verbose_name='Teléfono', max_length=15, null=True)
    adress = models.CharField(verbose_name='Dirección', max_length=50)


    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f"{self.name} {self.last_name}"
