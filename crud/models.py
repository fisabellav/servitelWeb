from django.db import models
import re

# Create your models here.
class ProductManager(models.Manager):
    def validador_campos(self, postData):
        JUST_LETTERS_NUMBERS = re.compile(r'^[a-zA-Z0-9\sáéíóúÁÉÍÓÚñÑ]+$')
        
        errors = {}
        
        # Validar nombre del producto
        if len(postData['product'].strip()) < 2 or len(postData['product'].strip()) > 50:
            errors['product_len'] = "El nombre del producto debe tener entre 2 y 50 caracteres"
        
        if not JUST_LETTERS_NUMBERS.match(postData['product']):
            errors['just_letters_numbers'] = "El nombre del producto solo puede contener letras, números y espacios"

        # Validar descripción
        if postData.get('description') and len(postData['description'].strip()) > 500:
            errors['description_len'] = "La descripción no puede tener más de 500 caracteres"

        # Validar categoría
        if postData['category'] not in ['CA', 'KI', 'AC']:
            errors['category'] = "Categoría no válida"

        # Validar precio
        try:
            price = int(postData['price'])
            if price < 0:
                errors['price'] = "El precio no puede ser negativo"
        except ValueError:
            errors['price'] = "El precio debe ser un número entero"

        # Validar cámaras y canales si la categoría es 'Kits'
        if postData['category'] == 'KI':
            if 'cameras' not in postData or not postData['cameras'].isdigit() or int(postData['cameras']) <= 0:
                errors['cameras'] = "Debes ingresar un número de cámaras para la categoría 'Kits'"
            if 'channels' not in postData or not postData['channels'].isdigit() or int(postData['channels']) <= 0:
                errors['channels'] = "Debes ingresar un número de canales para la categoría 'Kits'"
        else:
            # Validar cámaras
            if postData.get('cameras'):
                try:
                    cameras = int(postData['cameras'])
                    if cameras < 0:
                        errors['cameras'] = "El número de cámaras no puede ser negativo"
                except ValueError:
                    errors['cameras'] = "El número de cámaras debe ser un número entero"

            # Validar canales
            if postData.get('channels'):
                try:
                    channels = int(postData['channels'])
                    if channels < 0:
                        errors['channels'] = "El número de canales no puede ser negativo"
                except ValueError:
                    errors['channels'] = "El número de canales debe ser un número entero"
        
        return errors
# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('CA', 'Cámaras'),
        ('KI', 'Kits'),
        ('AC', 'Accesorios'),
    ]

    product = models.CharField(verbose_name='Producto', max_length=50)
    description = models.TextField(verbose_name='Descripción',null=True,blank=True)
    category = models.CharField(verbose_name='Categoría', max_length=2, choices=CATEGORY_CHOICES, default='KI')
    price = models.PositiveIntegerField(verbose_name='Precio', blank=True, default=0)
    cameras = models.PositiveIntegerField(verbose_name='Cámaras', null=True, blank=True)
    channels = models.PositiveIntegerField(verbose_name='Canales', null=True, blank=True)
    image = models.ImageField(verbose_name='Imagen',upload_to='productos',null=True,blank=True)
    created_at = models.DateTimeField(verbose_name='Fecha registro',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Fecha actualización',auto_now=True)
    objects = ProductManager()

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['product']

    def __str__(self) -> str:
        return self.product