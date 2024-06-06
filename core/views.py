from django.shortcuts import render, HttpResponse, redirect, reverse
from crud.models import *
from .models import *
from .forms import *
from django.http import JsonResponse
import requests

# Create your views here.
def index(request):
    context = {'productos':Product.objects.all(), 'request': request}
    return render(request, 'core/index.html', context)

def catalogo(request):
    filters = list(set(Product.objects.all().values_list('cameras', flat=True)))
    context = {'filtros': filters, 'productos':Product.objects.all(), 'request': request}
    return render(request, 'core/catalogo.html', context)

def filter_by_cameras(request, cameras):
    try:
        filters = list(set(Product.objects.all().values_list('cameras', flat=True)))
        filtered_products = Product.objects.filter(cameras=cameras)
        if filtered_products:
            context = {'filtros': filters, 'filtered_products': filtered_products, 'request': request}
            return render(request,'core/catalogo.html',context)
        else:
            return redirect(reverse('catalogo') + '?FAIL')
    except:
        return redirect(reverse('catalogo') + '?FAIL')

def producto(request, id):
    try:
        product = Product.objects.get(id=id)
        if product:
            if request.method == 'POST':
                form = SolicitudForm(request.POST, request.FILES)
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
                    obj = Solicitud.objects.create(
                        name=name,
                        last_name=last_name,
                        birthday=birthday,
                        phone_number=phone_number,
                        comuna=comuna,
                        gender=gender,
                        product=product
                    )
                    obj.save()
                    return redirect(reverse('catalogo') + '?OK')
                else:
                    return render(request, 'core/producto.html', {'producto': product, 'form': form})
            else:
                form = SolicitudForm
            context = {'producto': product, 'form': form}
            return render(request, 'core/producto.html', context)
        else:
            return redirect(reverse('catalogo') + '?NO_EXIST')
    except Product.DoesNotExist:
        return redirect(reverse('catalogo') + '?NO_EXIST')

def contacto(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST, request.FILES)
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
            obj = Solicitud.objects.create(
                name=name,
                last_name=last_name,
                birthday=birthday,
                phone_number=phone_number,
                comuna=comuna,
                gender=gender,
            )
            obj.save()
            return redirect(reverse('contacto') + '?OK')
        else:
            return render(request, 'core/contacto.html', {'producto': product, 'form': form})
    else:
        form = SolicitudForm
    context = {'form': form}
    return render(request, 'core/contacto.html', context)



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
