from django.db import models
import re
from datetime import datetime, timedelta
from core.models import Solicitud

# Create your models here.
class UserManager(models.Manager):
    def validador_campos(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        JUST_LETTERS = re.compile(r'^[a-zA-Z.]+$')
        PASSWORD_REGEX = re.compile(r'^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$')

        errors = {}

        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email_exits'] = "Email ya registrado!!!"
        else:
            if len(postData['first_name'].strip()) < 2 or len(postData['first_name'].strip()) > 30:
                errors['first_name_len'] = "Nombre debe tener entre 2 y 30 caracteres"

            if len(postData['last_name'].strip()) < 2 or len(postData['last_name'].strip()) > 30:
                errors['last_name_len'] = "Apellido debe tener entre 2 y 30 caracteres"
            
            if not JUST_LETTERS.match(postData['first_name']) or not JUST_LETTERS.match(postData['last_name']):
                errors['just_letters'] = "Solo se permite el ingreso de letras en el nombre y apellido"
                
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = "Formato correo no válido"
            
            if not PASSWORD_REGEX.match(postData['password']):
                errors['password_format'] = "Formato contraseña no válido"

        #if len(postData['password']) < 8 or len(postData['password']) > 15:
        #    errors['password_len'] = "La cantidad de caracteres debe ser entre 8 y 15" 

        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Contraseñas no coinciden"

        return errors


class User(models.Model):

    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    email = models.EmailField(verbose_name='Correo', max_length=100, unique=True)
    password = models.CharField(verbose_name='Clave', max_length=250)
    rol = models.CharField(max_length=20, default='USER')
    created_at = models.DateTimeField(verbose_name='Fecha registro', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Fecha actualización', auto_now=True)
    objects = UserManager()

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    
        