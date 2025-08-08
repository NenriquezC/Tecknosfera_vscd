from django.http import HttpResponse
from .models import Producto, Proveedor
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductoForm  # Debes tener un form para Producto

# Create your views here.
def index(request):
    productos = Producto.objects.all()
    #productos = Producto.objects.values()  # Esto devuelve una lista de diccionarios
    # productos = Producto.objects.all()
    return render(request, "productos.html", {"productos": productos})
    #return HttpResponse("esta es la view de productos y proveedores")


def inventario(request):
    opcion = request.GET.get("tabla", "")  # "productos" o "proveedores"
    productos = Producto.objects.all() if opcion == "productos" else None
    proveedores = Proveedor.objects.all() if opcion == "proveedores" else None

    # Procesar productos para el aviso de bajo stock
    #productos_alerta = []
    #if productos:
    #    for p in productos:
    #        if p.stock_minimo:  # Evita división por cero
    #            porcentaje = p.stock / p.stock_minimo * 100
    #            if porcentaje <= 10:
    #                productos_alerta.append(p.id)  # Guardamos el id para resaltar en la tabla
    productos_alerta = []
    if productos:
        for p in productos:
            if p.stock <= p.stock_minimo:
                productos_alerta.append(p.id)
                
    return render(request, "inventario.html", {
        "opcion": opcion,
        "productos": productos,
        "proveedores": proveedores,
        "productos_alerta": productos_alerta,
        

    })

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario')  # Vuelve a la página inventario
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('inventario')
    return render(request, 'eliminar_producto.html', {'producto': producto})

def inicio(request): #para el boton de la pantalla de inicio
    return render(request, 'inicio.html')