from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import *

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

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
            context = {'producto':product}
            return render(request,'core/producto.html',context)
        else:
            return redirect(reverse('catalogo') + '?NO_EXIST')
    except:
        return redirect(reverse('catalogo') + '?NO_EXIST')

