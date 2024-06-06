from django.db import models

# Create your models here.
class Product(models.Model):
    product = models.CharField(verbose_name='Producto', max_length=50)
    description = models.TextField(verbose_name='Descripción',null=True,blank=True)
    cameras = models.IntegerField(verbose_name='Cámaras')
    channels = models.IntegerField(verbose_name='Canales')
    image = models.ImageField(verbose_name='Imagen',upload_to='productos',null=True,blank=True)
    created_at = models.DateTimeField(verbose_name='Fecha registro',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Fecha actualización',auto_now=True)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['product']

    def __str__(self) -> str:
        return self.product