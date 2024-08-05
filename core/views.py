import json
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.utils.crypto import get_random_string
from crud.models import *
from login.models import *
from .models import *
from .forms import *
from login.forms import *
from crud.forms import *
from mailersend import emails
from crud.utils import send_order_status_email  # Importa la función que envía el correo
from django.conf import settings


# Create your views here.
def index(request):
    context = {'productos':Product.objects.all(), 'request': request}
    return render(request, 'core/index.html', context)

def catalogo(request):
    camera_filter = list(set(Product.objects.all().values_list('cameras', flat=True)))
    channel_filter = list(set(Product.objects.all().values_list('channels', flat=True)))

    selected_cameras = request.GET.getlist('cameras')
    selected_channels = request.GET.getlist('channels')

    filtered_products = Product.objects.all()

    if selected_cameras:
        filtered_products = filtered_products.filter(cameras__in=selected_cameras)

    if selected_channels:
        filtered_products = filtered_products.filter(channels__in=selected_channels)

    context = {
        'filtro_canal': channel_filter,
        'filtro_camara': camera_filter,
        'productos': filtered_products,
        'request': request,
        'selected_cameras': selected_cameras,
        'selected_channels': selected_channels
    }
    return render(request, 'core/catalogo.html', context)

def accesorios(request):
    productos_filtrados = Product.objects.filter(category='AC')
    context = {'productos':productos_filtrados, 'request': request}
    return render(request, 'core/accesorios.html', context)

def filter_products(request):
    camera_filter = list(set(Product.objects.all().values_list('cameras', flat=True)))
    channel_filter = list(set(Product.objects.all().values_list('channels', flat=True)))

    selected_cameras = request.GET.getlist('cameras')
    selected_channels = request.GET.getlist('channels')

    filtered_products = Product.objects.all()

    if selected_cameras:
        filtered_products = filtered_products.filter(cameras__in=selected_cameras)

    if selected_channels:
        filtered_products = filtered_products.filter(channels__in=selected_channels)

    context = {
        'filtro_canal': channel_filter,
        'filtro_camara': camera_filter,
        'filtered_products': filtered_products,
        'selected_cameras': selected_cameras,
        'selected_channels': selected_channels,
        'request': request
    }
    return render(request, 'core/catalogo.html', context)

def send_dynamic_order_email(user_email, order_number):
    mailer = emails.NewEmail(settings.MAILERSEND_API_KEY)
    mail_body = {}

    mail_from = {
        "name": "Servitel",
        "email": settings.DEFAULT_FROM_EMAIL,
    }

    recipients = [
        {
            "email": user_email,
        }
    ]

    personalization = [
        {
            "email": user_email,
            "data": {
                "order_number": order_number
            }
        }
        
    ]

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject("Pedido recibido", mail_body)
    mailer.set_template("351ndgwnvnqgzqx8", mail_body)
    mailer.set_advanced_personalization(personalization, mail_body)

    response = mailer.send(mail_body)

    print(response)
    return response

def producto(request, id):
    try:
        producto = Product.objects.get(id=id)

        if request.method == 'POST':
            user_form = UserForm(request.POST, prefix='')
            orderdetail_form = OrderDetailForm(request.POST, prefix='order-detail')
            order_form = OrderForm(request.POST, prefix='order')

            # Obtener datos del formulario POST
            name = request.POST.get('name')
            last_name = request.POST.get('last_name')
            birthday = request.POST.get('birthday')
            comuna = request.POST.get('comuna')
            gender = request.POST.get('gender')
            phone_number = request.POST.get('formatted_phone_number')
            email = request.POST.get('email')
            password = request.POST.get('password', '')

            # Comprueba si ya existe un usuario con el correo electrónico o el número de teléfono
            existing_user_email = User.objects.filter(email=email).first()
            existing_user_phone = User.objects.filter(phone_number=phone_number).first()
            
            if existing_user_email or existing_user_phone:
                existing_user = existing_user_email if existing_user_email else existing_user_phone

                if password:
                    if existing_user and not existing_user.password:
                        # Generate a unique token for verification
                        verification_token = get_random_string(length=32)
                        
                        # Save the token with the user record
                        existing_user.verification_token = verification_token
                        existing_user.save()
                        
                        # Send an email with a link for completing registration
                        verification_link = reverse('complete-registration', kwargs={'token': verification_token})
                        verification_url = request.build_absolute_uri(verification_link)
                        
                        send_verification_email(existing_user.email, verification_url)

                        request.session['level_mensaje'] = 'alert-warning'
                        messages.warning(request, "El correo o teléfono ya están registrados. Se ha enviado un correo para completar tu registro.")
                        return redirect(reverse('login'))
                else:   
                
                    context = {
                        'user_form': user_form,
                        'orderdetail_form': orderdetail_form,
                        'order_form': order_form,
                        'producto': producto
                    }
                    request.session['level_mensaje'] = 'alert-warning'
                    messages.warning(request, "El correo o teléfono ya están asociados a una cuenta. Inicie sesión, ingrese una contraseña para registrarse o corrija sus datos.")
                    return render(request, 'core/producto.html', context)
            else:

                if user_form.is_valid() and  orderdetail_form.is_valid():

                    name = user_form.cleaned_data.get('name')
                    last_name = user_form.cleaned_data.get('last_name')
                    birthday = user_form.cleaned_data.get('birthday')
                    comuna = user_form.cleaned_data.get('comuna')
                    gender = user_form.cleaned_data.get('gender')
                    phone_number = user_form.cleaned_data.get('formatted_phone_number')

                    email = user_form.cleaned_data.get('email')
                    password = user_form.cleaned_data.get('password', '')

                    quantity = orderdetail_form.cleaned_data.get('quantity')
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
                            'user_form': user_form,
                            'orderdetail_form': orderdetail_form,
                            'order_form': order_form,
                            'producto': producto  
                        }
                        return render(request, 'core/producto.html', context)
                    
                    else:
                        # Clear session data
                        request.session['registro_nombre'] = ""
                        request.session['registro_apellido'] = ""
                        request.session['registro_email'] = ""
                        request.session['registro_phone'] = ""
                        request.session['registro_comuna'] = ""
                        request.session['registro_birthday'] = ""
                        request.session['registro_genero'] = ""

                        user = User.objects.create(
                            name=name,
                            last_name=last_name,
                            birthday=birthday,
                            phone_number=phone_number,
                            comuna=comuna,
                            gender=gender,
                            email=email,
                            password=password,
                        )
                        user.save()

                    
                        total = producto.price * quantity
                        order = Order.objects.create(
                            user=user,
                            total=total,

                        )
                        order.save()

                        order_detail = OrderDetail.objects.create(
                            order=order,
                            product=producto,
                            quantity=quantity,
                            unit_price=producto.price,
                            subtotal=total,
                        )
                        order_detail.save()
                        request.session['level_mensaje'] = 'alert-success'
                        messages.success(request, 'Pedido enviado. En breve le llegará el correo de confirmación')
                        
                        send_dynamic_order_email(email, order.id)
                        return redirect(reverse('catalogo') + '?OK')
            
        if request.method == 'GET':
            user_form = UserForm(prefix='')
            orderdetail_form = OrderDetailForm(prefix='order-detail')
            order_form = OrderForm(prefix='order')
            context = {
                'user_form': user_form,
                'orderdetail_form': orderdetail_form,
                'order_form': order_form,
                'producto': producto
            }
            return render(request, 'core/producto.html', context)
    except Product.DoesNotExist:
        return redirect(reverse('catalogo') + '?NO_EXIST')

def new_order_wishlist(request):
    if 'usuario' in request.session:
        usuario_info = request.session['usuario']
        user_instance = User.objects.get(id=usuario_info['id'])

        if request.method == 'POST':
            # Obtener los datos del carrito del formulario
            data = json.loads(request.body.decode('utf-8'))
            items = data.get('items', [])

            # Crear la orden
            order = Order.objects.create(
                user=user_instance,
                total=0  # El total se actualizará más adelante
            )

            total_order = 0
            # Procesar cada producto en el carrito
            for item in items:
                product_id = item.get('id')
                quantity = item.get('quantity', 1) 

                try:
                    product = Product.objects.get(id=product_id)
                    subtotal = product.price * quantity
                    # Crear el detalle del pedido
                    OrderDetail.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        unit_price=product.price,
                        subtotal=subtotal
                    )

                    # Actualizar el total de la orden
                    total_order += subtotal

                    

                except Product.DoesNotExist:
                    # Maneja el caso donde el producto no existe
                    request.session['level_mensaje'] = 'alert-danger'
                    messages.error(request, 'El producto no existe')
                    return redirect(reverse('catalogo') + '?FAIL')
                    
                # Actualizar el total de la orden
            order.total = total_order
            order.save()
                

            # Mensaje de éxito y redirección
            request.session['level_mensaje'] = 'alert-success'
            messages.success(request, 'Pedido realizado. Pronto te llegará un mail de confirmación')
            send_dynamic_order_email(user_instance.email, order.id)
            
            return JsonResponse({'success': True})
        
        else:
            # Si el método no es POST, puede manejarlo según tu lógica específica
            orderdetail_form = OrderDetailForm(prefix='')

            return render(request, 'core/producto.html', {
                'producto':  product # Aquí puedes pasar el producto si lo necesitas para la vista
            })

    else:
        # Manejar el caso donde el usuario no está autenticado
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        request.session['level_mensaje'] = 'alert-danger'
        return redirect(reverse('login'))

def new_order(request, id):
    if 'usuario' in request.session:
        usuario_info = request.session['usuario']
        user_instance = User.objects.get(id=usuario_info['id'])

        producto = get_object_or_404(Product, id=id)

        if request.method == 'POST':
            quantity = int(request.POST.get('quantity', 1))
            total = producto.price * quantity

            order = Order.objects.create(
                user=user_instance,
                total=total,
            )
            order.save()
            if 'wishlist' in request.POST:
                wishlist = request.POST.get('wishlist', '[]')
                wishlist_products = json.loads(wishlist)
                
                for item in wishlist_products:
                    product = Product.objects.get(id=item['id'])
                    quantity = item['quantity']
                    subtotal = product.price * quantity

                    OrderDetail.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        unit_price=product.price,
                        subtotal=subtotal,
                    )
                    order_details.append({
                            "product": producto.product,
                            "quantity": quantity,
                        })
            else:
                # Si no hay wishlist, solo añadir el producto actual al pedido
                OrderDetail.objects.create(
                    order=order,
                    product=producto,
                    quantity=quantity,
                    unit_price=producto.price,
                    subtotal=total,
                )


            request.session['level_mensaje'] = 'alert-success'
            messages.success(request, 'Pedido enviado. En breve le llegará el correo de confirmación')
            send_dynamic_order_email(user_instance.email, order.id)
            return redirect(reverse('catalogo') + '?OK')  # Redirigir a una página de éxito después de crear el pedido

        else:
            orderdetail_form = OrderDetailForm(prefix='')

        return render(request, 'core/producto.html', {
            'producto': producto,
        })
    else:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        request.session['level_mensaje'] = 'alert-danger'
        return redirect(reverse('login'))

def contacto(request):
    try:
        if request.method == 'POST':
            user_form = UserForm(request.POST, prefix='user')
            order_form = OrderForm(request.POST, prefix='order')
            orderdetail_form = OrderDetailForm(request.POST, prefix='order-detail')

            # Obtener datos del formulario POST
            name = request.POST.get('user-name')
            last_name = request.POST.get('user-last_name')
            birthday = request.POST.get('user-birthday')
            comuna = request.POST.get('user-comuna')
            gender = request.POST.get('user-gender')
            phone_number = request.POST.get('user-phone_number')
            email = request.POST.get('user-email')
            password = request.POST.get('user-password', '')

            # Comprueba si ya existe un usuario con el correo electrónico o el número de teléfono
            existing_user_email = User.objects.filter(email=email).first()
            existing_user_phone = User.objects.filter(phone_number=phone_number).first()

            if existing_user_email or existing_user_phone:
                existing_user = existing_user_email if existing_user_email else existing_user_phone

                if password:
                    if existing_user and not existing_user.password:
                        # Genera un token único para la verificación
                        verification_token = get_random_string(length=32)
                        
                        # Guarda el token con el registro del usuario
                        existing_user.verification_token = verification_token
                        existing_user.save()
                        
                        # Envía un correo electrónico con un enlace para completar el registro
                        verification_link = reverse('complete-registration', kwargs={'token': verification_token})
                        verification_url = request.build_absolute_uri(verification_link)
                        
                        send_verification_email(existing_user.email, verification_url)

                        request.session['level_mensaje'] = 'alert-warning'
                        messages.warning(request, "El correo o teléfono ya están registrados. Se ha enviado un correo para completar tu registro.")
                        return redirect(reverse('login'))
                else:
                    context = {
                        'user_form': user_form,
                        'order_form': order_form,
                        'orderdetail_form': orderdetail_form,
                    }
                    request.session['level_mensaje'] = 'alert-warning'
                    messages.warning(request, "El correo o teléfono ya están asociados a una cuenta. Inicie sesión, ingrese una contraseña para registrarse o corrija sus datos.")
                    return render(request, 'core/contacto.html', context)
            else:
                if user_form.is_valid():
                    name = user_form.cleaned_data.get('name')
                    last_name = user_form.cleaned_data.get('last_name')
                    birthday = user_form.cleaned_data.get('birthday')
                    comuna = user_form.cleaned_data.get('comuna')
                    gender = user_form.cleaned_data.get('gender')
                    phone_number = user_form.cleaned_data.get('formatted_phone_number')

                    email = user_form.cleaned_data.get('email')
                    password = user_form.cleaned_data.get('password', '')

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
                            'user_form': user_form,
                            'orderdetail_form': orderdetail_form,
                            'order_form': order_form,
                            'producto': producto  
                        }
                        return render(request, 'core/contacto.html', context)
                    
                    else:
                        user = User.objects.create(
                            name=name,
                            last_name=last_name,
                            birthday=birthday,
                            phone_number=phone_number,
                            comuna=comuna,
                            gender=gender,
                            email=email,
                            password=password,
                        )
                        user.save()

                        order = Order.objects.create(
                            user=user,
                            total=0,  # Inicialmente en 0, se actualizará más tarde
                        )
                        order.save()

                        wishlist = request.POST.get('wishlist', '[]')
                        wishlist_products = json.loads(wishlist)

                        total = 0
                        for item in wishlist_products:
                            product = Product.objects.get(id=item['id'])
                            quantity = item['quantity']
                            subtotal = product.price * quantity
                            total += subtotal

                            OrderDetail.objects.create(
                                order=order,
                                product=product,
                                quantity=quantity,
                                unit_price=product.price,
                                subtotal=subtotal,
                            )

                            order.total = total
                            order.save()
                            

                        request.session['level_mensaje'] = 'alert-success'
                        messages.success(request, 'Solicitud enviada. En breve le llegará el correo de confirmación')
                        send_dynamic_order_email(email, order.id)
                        return redirect(reverse('contacto') + '?OK')
                else:
                    context = {
                        'user_form': user_form,
                        'order_form': order_form,
                        'orderdetail_form': orderdetail_form,
                    }
                    request.session['level_mensaje'] = 'alert-success'
                    messages.warning(request, 'ALGO NO FUNCIONA')
                    return render(request, 'core/contacto.html', context)
        else:
            user_form = UserForm(prefix='user')
            order_form = OrderForm(prefix='order')
            orderdetail_form = OrderDetailForm(prefix='order-detail')
            
        context = {
            'user_form': user_form,
            'order_form': order_form,
            'orderdetail_form': orderdetail_form,
        }
        return render(request, 'core/contacto.html', context)
    except Product.DoesNotExist:
        return redirect(reverse('contacto') + '?NO_EXIST')


def order_list(request):
    if 'usuario' in request.session:
        usuario_info = request.session['usuario']
        user_instance = User.objects.get(id=usuario_info['id'])

        orders = Order.objects.filter(user=user_instance)
        context = {
            'orders': orders
        }
        return render(request, 'core/myorders.html', context)
    else:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        request.session['level_mensaje'] = 'alert-danger'
        return redirect(reverse('login'))

def order_detail(request, id):
    if 'usuario' in request.session:
        usuario_info = request.session['usuario']
        user_instance = User.objects.get(id=usuario_info['id'])

        order = get_object_or_404(Order, id=id)
        order_details = OrderDetail.objects.filter(order=order)

        context = {
            'order': order,
            'order_details': order_details
        }
        return render(request, 'core/order.html', context)
    else:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        request.session['level_mensaje'] = 'alert-danger'
        return redirect(reverse('login'))


def editar_perfil(request, id):
    user = get_object_or_404(User, id=id)
    old_password = user.password
    staff = user.is_staff
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            postData = request.POST.copy()
            errors = User.objects.validador_campos(postData, staff)

            if errors:
                for key, value in errors.items():
                    messages.error(request, value)

                request.session['level_mensaje'] = 'alert-danger'
                return redirect(reverse('editar-perfil', args=[id]))
            else:
                # Guardar la nueva contraseña del formulario
                new_password = postData.get('password').strip()

                # Guardar el formulario
                user_instance = form.save(commit=False)

                if new_password:
                    # Si se proporciona una nueva contraseña, establecerla usando set_password
                    user_instance.set_password(new_password)
                else:
                    # Si no se proporciona una nueva contraseña, usar la contraseña existente
                    user_instance.password = old_password

                # Guardar el usuario con la posible nueva contraseña y otros cambios
                user_instance.save()

                request.session['level_mensaje'] = 'alert-success'
                messages.success(request, 'Perfil actualizado')

                user.refresh_from_db()

                birthday_formatted = user.birthday.strftime('%Y-%m-%d') if user.birthday else None
                request.session['usuario'] = {
                    'id': user.id,
                    'name': getattr(user, 'name', None),
                    'last_name': getattr(user, 'last_name', None),
                    'email': getattr(user, 'email', None),
                    'phone_number': getattr(user, 'phone_number', None),
                    'comuna': getattr(user.comuna, 'comuna', None) if user.comuna else None,
                    'gender': user.get_gender_display() if user.gender else None,
                    'birthday': birthday_formatted,
                    'rol': getattr(user, 'rol', None),
                }
                return redirect(reverse('index') + '?UPDATED')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
            return redirect(reverse('editar-perfil', args=[id]))
    else:
        context = {'form': form}
        return render(request, 'core/perfil.html', context)

def about(request):
    return render(request, 'core/about.html')

