from django.shortcuts import render, redirect, reverse  
from .models import *
from .forms import *

# Create your views here.
def product_list(request):
    context = {'productos':Product.objects.all(), 'request': request}
    return render(request, 'crud/product-list.html', context)

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.cleaned_data.get('product')
            description = form.cleaned_data.get('description')
            cameras = form.cleaned_data.get('cameras')
            channels = form.cleaned_data.get('channels')
            image = form.cleaned_data.get('image')
            obj = Product.objects.create(
                product = product,
                description = description,
                cameras = cameras,
                channels = channels,
                image = image
            )
            obj.save()
            return redirect(reverse('product-list') + '?OK')
        else:
            return redirect(reverse('add-product') + '?FAIL')
    else:    
        form = ProductForm
    return render(request,'crud/add-product.html',{'form':form})

def productlist_delete(request, id):
    try:
        product = Product.objects.get(id=id)
        product.delete()
        return redirect(reverse('product-list') + '?DELETED')
    except:
        return redirect(reverse('product-list') + '?FAIL')

def productlist_edit(request,id):
    
        product = Product.objects.get(id=id)
        form = ProductForm(instance = product)

        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance = product)

            if form.data.get('image_clear') == 'on':
                    product.image.delete(save=False)
                    form.instance.image = None  # Eliminar la referencia a la imagen en el formulario
        
            if form.is_valid():
                form.save()
                return redirect(reverse('product-list') + '?UPDATED')
            else:
                return redirect(reverse('productlist-edit') + id)

        context = {'form':form}
        return render(request,'crud/product-edit.html',context)

def product_detail(request,id):
    try:
        product = Product.objects.get(id=id)
        if product:
            context = {'producto':product}
            return render(request,'crud/detail.html',context)
        else:
            return redirect(reverse('product-list') + '?NO_EXIST')
    except:
        return redirect(reverse('product-list') + '?NO_EXIST')