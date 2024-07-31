from django.db import models
import re
from datetime import datetime, timedelta
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        
        if 'is_staff' in extra_fields and extra_fields['is_staff']:
            if not password:
                raise ValueError('El personal de staff debe tener una contraseña')
            user.set_password(password)
        elif password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields['rol'] = 'ADMIN'

        if not password:
            raise ValueError('Los superusuarios deben tener una contraseña')
        name = extra_fields.get('name')
        last_name = extra_fields.get('last_name')

        while not name:
            name = input('El nombre debe ser proporcionado: ')
            if not name:
                print('El nombre es obligatorio.')
        
        while not last_name:
            last_name = input('El apellido debe ser proporcionado: ')
            if not last_name:
                print('El apellido es obligatorio.')

        extra_fields['name'] = name
        extra_fields['last_name'] = last_name


        

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)

    def validador_campos(self, postData, is_staff):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        JUST_LETTERS = re.compile(r'^[a-zA-Z.]+$')
        PASSWORD_REGEX = re.compile(r'^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$')
        PHONE_REGEX = re.compile(r'^(\+\d{1,3}\d{9,15}|\+56\d{9})$')

        
        errors = {}

        email = postData.get('email', None)
        name = postData.get('name', '').strip()
        last_name = postData.get('last_name', '').strip()
        phone_number = postData.get('phone_number', '').strip()

        if not email:
            errors['email'] = "El email es obligatorio"
        elif not EMAIL_REGEX.match(email):
            errors['email_format'] = "Formato correo no válido"
        
        if not name or len(name) < 2 or len(name) > 30:
                errors['name_len'] = "Nombre debe tener entre 2 y 30 caracteres"
        if not last_name or len(last_name) < 2 or len(last_name) > 30:
            errors['last_name_len'] = "Apellido debe tener entre 2 y 30 caracteres"
        if not JUST_LETTERS.match(name) or not JUST_LETTERS.match(last_name):
            errors['just_letters'] = "Solo se permite el ingreso de letras en el nombre y apellido"
        
        if not is_staff:
            # Campos obligatorios para usuarios que no son staff
            
            comuna = postData.get('comuna', '').strip()
            birthday = postData.get('birthday', '').strip()
            gender = postData.get('gender', '').strip()

            
            if not phone_number or not PHONE_REGEX.match(phone_number):
                errors['phone_number'] = "Número de teléfono inválido"
            if not comuna:
                errors['comuna'] = "La comuna es obligatoria"
            if not birthday:
                errors['birthday'] = "La fecha de nacimiento es obligatoria"
            else:
                try:
                    birth_date = datetime.strptime(birthday, '%Y-%m-%d')
                    age = (datetime.now() - birth_date).days // 365
                    if age < 18:
                        errors['birth_date'] = "Debes ser mayor de 18 años"
                except ValueError:
                    errors['birth_date_format'] = "Formato de fecha de nacimiento no válido"
            if not gender:
                errors['gender'] = "El género es obligatorio"
        else:
            if phone_number:
                if not PHONE_REGEX.match(phone_number):
                    errors['phone_number'] = "Número de teléfono inválido"
            

        

        # Validación de contraseña (solo si está presente)
        password = postData.get('password', None)
        if password:
            if not PASSWORD_REGEX.match(password):
                errors['password_format'] = "Formato contraseña no válido"
            if postData['password'] != postData['password_confirm']:
                errors['password_confirm'] = "Contraseñas no coinciden"
            if len(postData['password']) < 8 or len(postData['password']) > 15:
                errors['password_len'] = "La cantidad de caracteres debe ser entre 8 y 15"


        birth_date = postData.get('birthday', None)  
        if birth_date:
            try:
                birth_date = datetime.strptime(birth_date, '%Y-%m-%d')  # Cambia el formato si es necesario
                age = (datetime.now() - birth_date).days // 365
                if age < 18:
                    errors['birth_date'] = "Debes ser mayor de 18 años."
            except ValueError:
                errors['birth_date_format'] = "Formato de fecha de nacimiento no válido."

        return errors

class Comuna(models.Model):
    comuna = models.CharField(verbose_name='COMUNA', max_length=100)

    def __str__(self):
        return self.comuna

def default_birthday():
    return datetime.now().date() - timedelta(days=365*18)

class User(AbstractBaseUser, PermissionsMixin):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('SE', 'Sin especificar'),
    ]

    name = models.CharField(verbose_name='NOMBRE', max_length=50, blank=True, null=True)
    last_name = models.CharField(verbose_name='APELLIDO', max_length=50, blank=True, null=True)
    birthday = models.DateField(verbose_name='FECHA DE NACIMIENTO', default=default_birthday, null=True)
    phone_number = models.CharField(verbose_name='TELÉFONO', max_length=15, blank=True, null=True)
    gender = models.CharField(verbose_name='GÉNERO', max_length=2, choices=GENERO_CHOICES, default='SE', null=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, verbose_name='COMUNA', blank=True, null=True)
    email = models.EmailField(verbose_name='CORREO', max_length=100, unique=True, blank=True)
    password = models.CharField(verbose_name='CLAVE', max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    rol = models.CharField(max_length=20, default='USER')
    created_at = models.DateTimeField(verbose_name='Fecha registro', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Fecha actualización', auto_now=True)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        
    def __str__(self):
        return f"{self.name} {self.last_name}"
    
    

    # Establece un nombre relacionado para evitar conflictos
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set', blank=True)