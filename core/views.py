import json
from django.shortcuts import render, HttpResponse, redirect, reverse
from crud.models import *
from login.models import *
from .models import *
from login.forms import UserForm
from .forms import SolicitudProductoForm


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


def producto(request, id):
    try:
        product = Product.objects.get(id=id)
        if product:
            if request.method == 'POST':
                user_form = UserForm(request.POST, prefix='user')
                solicitud_form = SolicitudProductoForm(request.POST, prefix='solicitud')
                if user_form.is_valid() :
                    name = user_form.cleaned_data.get('name')
                    last_name = user_form.cleaned_data.get('last_name')
                    birthday = user_form.cleaned_data.get('birthday')
                    prefijo_telefono = request.POST.get('prefijo_telefono')
                    phone_number = user_form.cleaned_data.get('phone_number')
                    phone_number = ''.join(phone_number.split())  # Quitamos los espacios en blanco
                    phone_number = prefijo_telefono + phone_number
                    gender = user_form.cleaned_data.get('gender')
                    comuna = user_form.cleaned_data.get('comuna')
                    email = user_form.cleaned_data.get('email')
                    password = user_form.cleaned_data.get('password')

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

                    # solicitud = SolicitudProducto.objects.create(
                    #     user=user,
                    #     product=product,
                    #     quantity=solicitud_form.cleaned_data.get('quantity')
                    # )
                    # solicitud.save()

                    return redirect(reverse('catalogo') + '?OK')

                  
                else:
                    context = {
                        'producto': product,
                        'user_form': user_form,
                        'solicitud_form': solicitud_form
                    }
                    return render(request, 'core/producto.html', context)
            else:
                user_form = UserForm(prefix='user')
                solicitud_form = SolicitudProductoForm(prefix='solicitud')
                
            context = {
                'producto': product,
                'user_form': user_form,
                'solicitud_form': solicitud_form
            }
            return render(request, 'core/producto.html', context)
        else:
            return redirect(reverse('catalogo') + '?NO_EXIST')
    except Product.DoesNotExist:
        return redirect(reverse('catalogo') + '?NO_EXIST')

def contacto(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            last_name = form.cleaned_data.get('last_name')
            birthday = form.cleaned_data.get('birthday')
            prefijo_telefono = request.POST.get('prefijo_telefono')
            phone_number = form.cleaned_data.get('phone_number')
            phone_number = ''.join(phone_number.split())  # Quitamos los espacios en blanco
            phone_number = prefijo_telefono + phone_number
            gender = form.cleaned_data.get('gender')
            comuna = form.cleaned_data.get('comuna')
            obj = User.objects.create(
                name=name,
                last_name=last_name,
                birthday=birthday,
                phone_number=phone_number,
                comuna=comuna,
                gender=gender,
            )
            obj.save()

            wishlist = request.POST.get('wishlist', '[]')
            wishlist_products = json.loads(wishlist)

            for item in wishlist_products:
                product = Product.objects.get(id=item['id'])
                SolicitudProducto.objects.create(user_id=obj.id, product=product, quantity=item['quantity'])
            return redirect(reverse('contacto') + '?OK')
        else:
            return render(request, 'core/contacto.html', {'producto': product, 'form': form})
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'core/contacto.html', context)

def editar_perfil(request, idUser):
    
        user = User.objects.get(idUser=id)
        form = ProductForm(instance = user)

        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance = product)

    
            if form.is_valid():
                form.save()
                return redirect(reverse('product-list') + '?UPDATED')
            else:
                return redirect(reverse('productlist-edit') + id)

        context = {'form':form}
        return render(request,'crud/product-edit.html',context)


