#from django.http import HttpResponse
from .models import Producto, Proveedor
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductoForm, ProveedorForm # Debes tener un form para Producto
from django.contrib import messages

# Create your views here.
#-----------------------------------------------------------------------------------------------------------------------
def index(request):
    """ :param request:
        :return: render con la lista de productos
    """
    productos = Producto.objects.all()
    # productos = Producto.objects.values()  # Esto devuelve una lista de diccionarios
    # productos = Producto.objects.all()
    return render(request, "productos.html", {"productos": productos})
    # return HttpResponse("esta es la view de productos y proveedores")
#-----------------------------------------------------------------------------------------------------------------------
def inventario(request):
    """ :param request:
        :return: render con la lista de productos y proveedores, y alerta si el stock está al 90% o menos del stock mínimo
    """
    opcion = request.GET.get("tabla", "")  # "productos" o "proveedores"
    productos = Producto.objects.all() if opcion == "productos" else None
    proveedores = Proveedor.objects.all() if opcion == "proveedores" else None

    productos_alerta = []

    if productos:
        for p in productos:
            # Calcula el porcentaje del stock respecto al mínimo y lo añade como atributo
            if p.stock_minimo > 0:
                porcentaje_stock = (p.stock / p.stock_minimo) * 100
            else:
                porcentaje_stock = 100  # Si no hay mínimo, no alertar

            p.porcentaje_stock = porcentaje_stock  # Atributo dinámico

            # Si el stock está al 90% o menos del stock mínimo, alerta
            if porcentaje_stock <= 90:
                productos_alerta.append(p.id)

    return render(request, "inventario.html", {
        "opcion": opcion,
        "productos": productos,
        "proveedores": proveedores,
        "productos_alerta": productos_alerta,
    })
#-----------------------------------------------------------------------------------------------------------------------
"""def agregar_producto(request):
     :param request:
        :return: render con el formulario para agregar un producto
    
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario')  # Vuelve a la página inventario
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})"""

"""def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            # Si viene de compras, redirige de vuelta
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('listar_productos')  # O donde tú quieras
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})"""

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto agregado exitosamente! ¿Deseas agregar otro producto?')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('agregar_producto')  # Redirige a sí misma para limpiar el form
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})


#-----------------------------------------------------------------------------------------------------------------------
def seleccionar_editar_producto(request):
    """ :param request:
        :return: render con la lista de productos para seleccionar y editar
    """
    productos = Producto.objects.all()
    return render(request, 'seleccionar_editar_producto.html', {'productos': productos})
#-----------------------------------------------------------------------------------------------------------------------
def editar_producto(request, pk):
    """ :param request:
        :param pk: ID del producto a editar
        :return: render con el formulario para editar el producto
    """
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if 'recalcular_stock_minimo' in request.POST:
            # Si el usuario presionó el botón de recalcular
            if form.is_valid():
                producto = form.save(commit=False)
                producto.stock_minimo = int(producto.stock * 0.9)
                producto.save()
                return render(request, 'editar_producto.html', {
                    'form': ProductoForm(instance=producto),
                    'mensaje': 'Stock mínimo recalculado correctamente.',
                    'producto': producto
                })
        elif form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

#-----------------------------------------------------------------------------------------------------------------------
def eliminar_producto(request, id):
    """ :param request:
        :param id: ID del producto a eliminar
        :return: render con la confirmación de eliminación del producto
    """
    producto = get_object_or_404(Producto, pk=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('seleccionar_eliminar_producto')
    return render(request, 'confirmar_eliminar_producto.html', {'producto': producto})
#-----------------------------------------------------------------------------------------------------------------------
def seleccionar_eliminar_producto(request):
    """ :param request:
        :return: render con la lista de productos para seleccionar y eliminar
    """
    buscar = request.GET.get('buscar', '')
    productos = Producto.objects.filter(nombre__icontains=buscar) if buscar else Producto.objects.all()
    return render(request, 'seleccionar_eliminar_producto.html', {'productos': productos})
#-----------------------------------------------------------------------------------------------------------------------
def inicio(request):
    # para el boton de la pantalla de inicio
    """ :param request:"""
    return render(request, 'inicio.html')
#-----------------------------------------------------------------------------------------------------------------------
def agregar_proveedor(request):
    """ :param request:
        :return: render con el formulario para agregar un proveedor
    """
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario')  # Vuelve a la página inventario
    else:
        form = ProveedorForm()
    return render(request, 'agregar_proveedor.html', {'form': form})
#-----------------------------------------------------------------------------------------------------------------------
def editar_proveedor(request, proveedor_id):
    """ :param request:
        :param proveedor_id: ID del proveedor a editar
        :return: render con el formulario para editar el proveedor
    """
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'editar_proveedor.html', {'form': form})
#-----------------------------------------------------------------------------------------------------------------------
def seleccionar_editar_proveedor(request):
    """ :param request:
        :return: render con la lista de proveedores para seleccionar y editar
    """
    proveedores = Proveedor.objects.all()
    buscar = request.GET.get('buscar')
    if buscar:
        proveedores = proveedores.filter(nombre__icontains=buscar)
    return render(request, 'seleccionar_editar_proveedor.html', {'proveedores': proveedores})
#-----------------------------------------------------------------------------------------------------------------------
def eliminar_proveedor(request, proveedor_id):
    """ :param request:
        :param proveedor_id: ID del proveedor a eliminar
        :return: render con la confirmación de eliminación del proveedor
    """
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('inventario')
    return render(request, 'eliminar_proveedor.html', {'proveedor': proveedor})
#-----------------------------------------------------------------------------------------------------------------------
def seleccionar_eliminar_proveedor(request):
    """ :param request:
        :return: render con la lista de proveedores para seleccionar y eliminar
    """
    proveedores = Proveedor.objects.all()
    buscar = request.GET.get('buscar', '')
    if buscar:
        proveedores = proveedores.filter(nombre__icontains=buscar)
    return render(request, 'seleccionar_eliminar_proveedor.html', {'proveedores': proveedores})
#-----------------------------------------------------------------------------------------------------------------------
