from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib import messages
from .models import *
import bcrypt



def signup(request):
    if request.method == 'GET':
        return render(request, 'login/signup.html')
    
    if request.method == 'POST':
        errors = User.objects.validador_campos(request.POST)
        
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            
            # Preserve form data
            request.session['registro_nombre'] = request.POST.get('first_name', '')
            request.session['registro_apellido'] = request.POST.get('last_name', '')
            request.session['registro_email'] = request.POST.get('email', '')
            request.session['level_mensaje'] = 'alert-danger'
            
            # Pass session data as context variables
            context = {
                'first_name': request.session['registro_nombre'],
                'last_name': request.session['registro_apellido'],
                'email': request.session['registro_email'],
            }
            return render(request, 'login/signup.html', context)
        else:
            # Clear session data
            request.session['registro_nombre'] = ""
            request.session['registro_apellido'] = ""
            request.session['registro_email'] = ""
            
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            
            User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password_hash)
            messages.success(request, "Usuario registrado con éxito!!!!")
            request.session['level_mensaje'] = 'alert-success'
        
            request.session['email_login'] = email
            
            return redirect(reverse('login'))
    
    return render(request, 'login/signup.html')
            
def login(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')
    else:
        if request.method == 'POST':
            email_login = request.POST['email_login']
            request.session['email_login'] = email_login  # Store email in session
            
            user = User.objects.filter(email=request.POST['email_login']) #Buscamos el correo ingresado en la BD             
            
            if user : #Si el usuario existe

                usuario_registrado = user[0]
                
                if bcrypt.checkpw(request.POST['password_login'].encode(), usuario_registrado.password.encode()): 
                    usuario = {
                        'id':usuario_registrado.id,
                        'first_name':usuario_registrado.first_name,
                        'last_name':usuario_registrado.last_name,
                        'email':usuario_registrado.email,
                        'rol':usuario_registrado.rol,
                    }

                    request.session['usuario'] = usuario
                    

                    if usuario_registrado.rol == 'ADMIN' :
                        messages.success(request,"Ingreso exitoso")
                        request.session['level_mensaje'] = 'alert-success'
                        return redirect(reverse('product-list') + '?SUCCESS')
                        
                    else:
                        messages.success(request,"Ingreso exitoso")
                        request.session['level_mensaje'] = 'alert-success'
                        return redirect(reverse('index') + '?SUCCESS')
                else:
                    messages.error(request,"Datos mal ingresados o el usuario no existe")
                    request.session['level_mensaje'] = 'alert-danger'
                    return redirect(reverse('login') + '?FAIL')
            else:
                messages.error(request,"Datos mal ingresados o el usuario no existe")
                request.session['level_mensaje'] = 'alert-danger'
                return redirect(reverse('login') + '?FAIL')
            
def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    
    return redirect('/')

