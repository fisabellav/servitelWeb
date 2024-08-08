from django.shortcuts import render, redirect, reverse
from django.contrib import messages  
from .models import *
from core.models import *
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .utils import send_order_status_email  # Importa la función que envía el correo



@login_required
@user_passes_test(lambda u: u.is_staff)
def product_list(request):
    context = {'productos':Product.objects.all(), 'request': request}
    return render(request, 'crud/product-list.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_product(request):
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.cleaned_data.get('product')
            description = form.cleaned_data.get('description')
            price = form.cleaned_data.get('price')
            image = form.cleaned_data.get('image')
            category = form.cleaned_data.get('category')
            cameras = form.cleaned_data.get('cameras')
            channels = form.cleaned_data.get('channels')

            errors = Product.objects.validador_campos(request.POST)

            if errors:
                for key, value in errors.items():
                    messages.error(request, value)

                request.session['level_mensaje'] = 'alert-danger'
                return redirect(reverse('add-product') + '?FAIL')
            
            else:

                # Crear el objeto Product usando los datos limpios
                obj = Product.objects.create(
                    product=product,
                    description=description,
                    price=price,
                    image=image,
                    category=category,
                    cameras=cameras,
                    channels=channels
                )

                obj.save()

                request.session['level_mensaje'] = 'alert-success'
                messages.success(request, "Producto añadido correctamente.")
                return redirect(reverse('product-list') + '?OK')
        else:
            return redirect(reverse('add-product') + '?FAIL')
    else:
        form = ProductForm()

    return render(request, 'crud/add-product.html', {'form': form})
    # except:
    #     messages.error(request, "Algo salió mal. Intenta nuevamente")
    #     request.session['level_mensaje'] = 'alert-danger'
    #     return redirect('login')

@login_required
@user_passes_test(lambda u: u.is_staff)
def productlist_delete(request, id):
    try:
        product = Product.objects.get(id=id)
        product.delete()
        return redirect(reverse('product-list') + '?DELETED')
    except:
        return redirect(reverse('product-list') + '?FAIL')

@login_required
@user_passes_test(lambda u: u.is_staff)
def productlist_edit(request,id):
    if 'usuario' in request.session:
        usuario = request.session['usuario']
        if usuario.get('rol') == 'ADMIN':
            product = Product.objects.get(id=id)
            form = ProductForm(instance=product)

            if request.method == 'POST':
                form = ProductForm(request.POST, request.FILES, instance=product)

                errors = Product.objects.validador_campos(request.POST)

                if errors:
                    for key, value in errors.items():
                        messages.error(request, value)
                    
                    request.session['level_mensaje'] = 'alert-danger'
                    return redirect(reverse('productlist-edit', args=[id]) + '?ERROR')
                
                else:
                    if form.data.get('image_clear') == 'on':
                        product.image.delete(save=False)
                        form.instance.image = None  # Eliminar la referencia a la imagen en el formulario

                    if form.is_valid():
                        form.save()
                        request.session['level_mensaje'] = 'alert-success'
                        messages.success(request, "Producto modificado correctamente.")
                        return redirect(reverse('product-list') + '?UPDATED')
                    else:
                        messages.success(request, "No se realizaron cambios. Intente nuevamente.")
                        request.session['level_mensaje'] = 'alert-danger'
                        return redirect(reverse('productlist-edit', args=[id]) + '?ERROR')
            else:
                context = {'form': form}
                return render(request, 'crud/product-edit.html', context)
        else:
            messages.error(request, "No tienes permisos para ver esta página.")
            request.session['level_mensaje'] = 'alert-danger'
            return redirect(reverse('login'))
    else:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        request.session['level_mensaje'] = 'alert-danger'
        return redirect(reverse('login'))

@login_required
@user_passes_test(lambda u: u.is_staff)
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

@login_required
@user_passes_test(lambda u: u.is_staff)
def update_order_status(request, order_id, status):
    try:
        # Validar que el estado enviado esté entre las opciones válidas
        valid_statuses = ['PC', 'CF', 'EP', 'EN', 'CN']
        if status not in valid_statuses:
            return JsonResponse({'success': False, 'error': 'Estado no válido.'}, status=400)

        # Obtener el pedido
        try:
            order = Order.objects.get(id=order_id)
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'error': 'Pedido no encontrado.'}, status=404)

        order.status = status
        order.save()

        # Enviar correo electrónico al usuario
        user_email = order.user.email
        user_name = order.user.name
        order_id = order.id
        send_order_status_email(user_email, user_name, order_id, status)
        return JsonResponse({'success': True})
    except Exception as e:
        # En caso de error, devolver una respuesta JSON con el mensaje de error
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@user_passes_test(lambda u: u.is_staff)
def order_list(request):
        
        # Obtener todas las órdenes
        pedidos = Order.objects.all()

        # Obtener las opciones de estado del modelo Order
        estado_choices = Order.STATUS_CHOICES

        # Filtrar por estado si se envía un estado válido en la solicitud GET
        estado_seleccionado = request.GET.get('estado')
        if estado_seleccionado in dict(estado_choices).keys():
            pedidos = pedidos.filter(status=estado_seleccionado)

        context = {
            'pedidos': pedidos,
            'estado_choices': estado_choices,  # Pasar las opciones de estado al contexto
            'estado_seleccionado': estado_seleccionado,  # Pasar el estado seleccionado para mantener el filtro
            'request': request,
        }
        return render(request, 'crud/order-list.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def order_detail(request, id):
    try:
        order = get_object_or_404(Order, id=id)
        detalles = OrderDetail.objects.filter(order=order)

        if request.method == 'POST':
            new_status = request.POST.get('status')
            if new_status and new_status in dict(Order.STATUS_CHOICES):
                order.status = new_status
                order.save()
                messages.success(request, "Estado del pedido actualizado exitosamente.")
                request.session['level_mensaje'] = 'alert-success'
            else:
                messages.error(request, "Estado no válido.")
                request.session['level_mensaje'] = 'alert-danger'
            return redirect(reverse('order-detail', args=[order.id]))

        return render(request, 'crud/order-detail.html', {'order': order, 'detalles': detalles})
    except:
        messages.error(request, "Algo salió mal. Intenta nuevamente")
        request.session['level_mensaje'] = 'alert-danger'
        return render(request, 'crud/order-detail.html', {'order': order, 'detalles': detalles})