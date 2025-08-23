from django.shortcuts import render, redirect, get_object_or_404
from .models import Compra
from inventario.models import Producto #marca en rojo es unf also positivo
from .forms import CompraForm
from django.contrib import messages

# Create your views here.
#-----------------------------------------------------------------------------------------------------------------------
def agregar_compra(request):
    """
    :param request:
    :return: '/compras/agregar/?exito=1'
    """
    if request.method == 'POST': # Verifica si el método de la solicitud es POST
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)  # No guarda aún en la base de datos
            producto = compra.producto  # Obtiene el producto de la compra
            producto.stock += compra.cantidad  # Aumenta el stock del producto
            producto.save()  # Guarda el producto con el nuevo stock
            form.save()
            messages.success(request, '¡Compra registrada exitosamente!')
            # Redirige para limpiar el formulario y evitar el doble submit
            #return redirect('compras:agregar_compra')
            # Redirige y pasa un parámetro GET para mostrar el modal
            return redirect('/compras/agregar/?exito=1')
    else:
        form = CompraForm()
    productos = Producto.objects.all()
    return render(request, 'agregar_compra.html', {'form': form, 'productos': productos})
#-----------------------------------------------------------------------------------------------------------------------
#para ver compras
def ver_compras(request):
    """:param request:
       :return: render con las compras ordenadas por fecha
    """
    compras = Compra.objects.select_related('producto', 'cliente').order_by('-fecha')
    return render(request, 'ver_compras.html', {'compras': compras})

#-----------------------------------------------------------------------------------------------------------------------
def editar_compra(request, compra_id):
    """:param request:
       :param compra_id: ID de la compra a editar
       :return: render con el formulario para editar la compra
    """
    compra = get_object_or_404(Compra, id=compra_id)
    # Aquí deberías tener un formulario para editar, ejemplo:
    if request.method == 'POST':
        # form = CompraForm(request.POST, instance=compra)
        # if form.is_valid():
        #     form.save()
        #     return redirect('compras:ver_compras')
        pass  # Quita esto cuando implementes el form
    else:
        # form = CompraForm(instance=compra)
        pass
    # return render(request, 'compras/editar_compra.html', {'form': form, 'compra': compra})
    return render(request, 'editar_compra.html', {'compra': compra})  # Solo para que no falle
#-----------------------------------------------------------------------------------------------------------------------
def eliminar_compra(request, compra_id):
    """ :param request:
        :param compra_id: ID de la compra a eliminar
        :return: render con la confirmación de eliminación
    """
    compra = get_object_or_404(Compra, id=compra_id)
    if request.method == 'POST':
        compra.delete()
        return redirect('compras:ver_compras')
    return render(request, 'compras/eliminar_compra.html', {'compra': compra})

#-----------------------------------------------------------------------------------------------------------------------
def seleccionar_editar_compra(request):
    """ :param request:
        :return: render con las compras para seleccionar y editar
    """
    compras = Compra.objects.all() # Obtiene todas las compras
    buscar = request.GET.get("buscar") # Obtiene el parámetro de búsqueda de la URL
    if buscar: # Si hay un término de búsqueda
        compras = compras.filter( # Filtra las compras por el nombre del producto, nombre del cliente o ID
            producto__nombre__icontains=buscar
        ) | compras.filter(
            cliente__nombre__icontains=buscar
        ) | compras.filter(
            id__icontains=buscar
        )
    return render(request, 'seleccionar_editar_compra.html', {"compras": compras})
#-----------------------------------------------------------------------------------------------------------------------
def seleccionar_eliminar_compra(request):
    """ :param request:
        :return: render con las compras para seleccionar y eliminar
    """
    compras = Compra.objects.all()
    buscar = request.GET.get("buscar")
    if buscar:
        compras = compras.filter(
            producto__nombre__icontains=buscar
        ) | compras.filter(
            cliente__nombre__icontains=buscar
        ) | compras.filter(
            id__icontains=buscar
        )
    return render(request, 'seleccionar_eliminar_compra.html', {"compras": compras})