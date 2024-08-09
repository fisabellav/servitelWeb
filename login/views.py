from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from .forms import UserForm
import json
from django.http import JsonResponse
import requests
from django.contrib.auth.decorators import login_required, user_passes_test
from crud.utils import send_verification_email # Importa la función que envía el correo
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# from crud.utils import send_verification_email # Importa la función que envía el correo


def signup(request):
    if request.method == 'GET':
        user_form = UserForm(prefix='')
            
        context = {
            'gender_choices': UserForm.GENERO_CHOICES,
            'comuna_choices': Comuna.objects.all(),
            'user_form': user_form,
        }
        return render(request, 'login/signup.html', context)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, prefix='')
        phone_number = request.POST.get('formatted_phone_number')
            

        postData = request.POST.copy()
        postData['phone_number'] = phone_number
        errors = User.objects.validador_campos(postData, False)

        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            
            # Preserve form data in session
            request.session['registro_nombre'] = request.POST.get('name', '')
            request.session['registro_apellido'] = request.POST.get('last_name', '')
            request.session['registro_email'] = request.POST.get('email', '')
            request.session['registro_phone'] = request.POST.get('formatted_phone_number', '')
            request.session['registro_comuna'] = request.POST.get('comuna', '')
            request.session['registro_genero'] = request.POST.get('gender', '')
            request.session['registro_birthday'] = request.POST.get('birthday', '')
            request.session['level_mensaje'] = 'alert-danger'
            
            # Pass session data as context variables
            context = {
                'name': request.session['registro_nombre'],
                'last_name': request.session['registro_apellido'],
                'email': request.session['registro_email'],
                'phone_number': request.session['registro_phone'],
                'comuna': request.session['registro_comuna'],
                'birthday': request.session['registro_birthday'],
                'gender': request.session['registro_genero'],
            }
            return render(request, 'login/signup.html', context)
        
        else:
            # Clear session data
            request.session['registro_nombre'] = ""
            request.session['registro_apellido'] = ""
            request.session['registro_email'] = ""
            request.session['registro_phone'] = ""
            request.session['registro_comuna'] = ""
            request.session['registro_birthday'] = ""
            request.session['registro_genero'] = ""
            

            email = request.POST.get('email', '')
            phone_number = request.POST.get('formatted_phone_number', '')

            existing_user_email = User.objects.filter(email=email).first()
            existing_user_phone = User.objects.filter(phone_number=phone_number).first()
            
            if existing_user_email or existing_user_phone:
                existing_user = existing_user_email if existing_user_email else existing_user_phone
                
                if existing_user and not existing_user.password:
                    verification_token = get_random_string(length=32)
                    existing_user.verification_token = verification_token
                    existing_user.save()
                    
                    verification_link = reverse('complete-registration', kwargs={'token': verification_token})
                    verification_url = request.build_absolute_uri(verification_link)
                    send_verification_email(existing_user.email, verification_url)
                    
                    request.session['level_mensaje'] = 'alert-warning'
                    messages.warning(request, "El correo o teléfono ya están registrados. Se ha enviado un correo para completar tu registro.")
                    return redirect(reverse('login'))
            

                
                else:
                    request.session['level_mensaje'] = 'alert-warning'
                    messages.warning(request, "El correo o teléfono ya están registrados. Ingrese con su contraseña.")
                    return redirect(reverse('login'))
            else:
                if user_form.is_valid():
                    email = user_form.cleaned_data.get('email')
                    phone_number = user_form.cleaned_data.get('phone_number')
                    name = user_form.cleaned_data.get('name')
                    last_name = user_form.cleaned_data.get('last_name')
                    birthday = user_form.cleaned_data.get('birthday')
                    gender = user_form.cleaned_data.get('gender')
                    comuna = user_form.cleaned_data.get('comuna')

                    user = user_form.save(commit=False)
                    user.username = email  # Usar email como nombre de usuario
                    user.set_password(user_form.cleaned_data.get('password'))
                    user.save()
                    request.session['level_mensaje'] = 'alert-success'
                    messages.success(request, "Usuario registrado con éxito!")
                    return redirect(reverse('login'))
                else:
                    request.session['level_mensaje'] = 'alert-danger'
                    messages.error(request, "Formulario inválido")
                    return render(request, 'login/signup.html', {'user_form': user_form,  'form_errors': user_form.errors})
            
def login(request):
    if request.method == 'POST':
        email = request.POST['email_login']
        password = request.POST['password_login']

        try:
            user = authenticate(request, email=email, password=password)
        except:
            user = None
            

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Ingreso exitoso")
            request.session['level_mensaje'] = 'alert-success'

            usuario = User.objects.filter(email=request.POST['email_login']) #Buscamos el correo ingresado en la BD             
            
            if usuario : #Si el usuario existe

                usuario_registrado = usuario[0]

                usuario = {
                    'id':usuario_registrado.id,
                    'name':usuario_registrado.name,
                    'last_name':usuario_registrado.last_name,
                    'email':usuario_registrado.email,
                    'rol':usuario_registrado.rol,
                }

                request.session['usuario'] = usuario
            
            if user.is_staff:
                return redirect(reverse('product-list') + '?SUCCESS')
            else:
                return redirect(reverse('index') + '?SUCCESS')
        else:
            request.session['level_mensaje'] = 'alert-danger'
            messages.error(request, "Correo electrónico o contraseña incorrectos")
            return render(request, 'login/login.html')
    else:
        return render(request, 'login/login.html')
            
def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    auth_logout(request)   
    
    return redirect('/')

def complete_registration(request, token):
    try:
        user = User.objects.get(verification_token=token)
        
        if request.method == 'GET':
            return render(request, 'login/complete_registration.html', {'token': token})
        
        elif request.method == 'POST':
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            
            if password != password_confirm:
                messages.error(request, "Las contraseñas no coinciden.")
                return redirect(reverse('complete-registration', kwargs={'token': token}))
            
            
            user.set_password(password)
            user.verification_token = None  # Clear verification token after setting password
            user.save()
            request.session['level_mensaje'] = 'alert-success'
            messages.success(request, "Contraseña establecida correctamente. Ahora puedes iniciar sesión.")
            return redirect(reverse('login'))
    
    except User.DoesNotExist:
        request.session['level_mensaje'] = 'alert-danger'
        messages.error(request, "El enlace de verificación no es válido.")
        return redirect(reverse('login'))

@login_required
@user_passes_test(lambda u: u.is_staff)
def cargar_comunas_rm_desde_api(request):
    url_api_comunas = "https://gist.githubusercontent.com/juanbrujo/0fd2f4d126b3ce5a95a7dd1f28b3d8dd/raw/b8575eb82dce974fd2647f46819a7568278396bd/comunas-regiones.json"  # Reemplaza con la URL de la API de comunas
    response = requests.get(url_api_comunas)
    if response.status_code == 200:
        comunas_data = response.json()
        region_rm = next((region for region in comunas_data["regiones"] if region["region"] == "Región Metropolitana de Santiago"), None)
        if region_rm:
            for comuna in region_rm["comunas"]:
                nombre_comuna = comuna
                # Verifica si la comuna ya existe en la base de datos
                if not Comuna.objects.filter(comuna=nombre_comuna).exists():
                    comuna_obj = Comuna(comuna=nombre_comuna)
                    comuna_obj.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})