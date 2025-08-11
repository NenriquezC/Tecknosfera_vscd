from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from .models import Venta, Venta_Producto
from inventario.models import Producto
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from decimal import Decimal

User = get_user_model()

# Create your views here.
def index(request):
    """Vista principal de ventas - lista todas las ventas"""
    ventas = Venta.objects.all().order_by('-creado_en')
    
    # Filtros de búsqueda
    search_query = request.GET.get('search', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    
    if search_query:
        ventas = ventas.filter(
            Q(producto__nombre__icontains=search_query) |
            Q(cliente__username__icontains=search_query) |
            Q(cliente__first_name__icontains=search_query) |
            Q(cliente__last_name__icontains=search_query)
        )
    
    if fecha_desde:
        ventas = ventas.filter(fecha__gte=fecha_desde)
    
    if fecha_hasta:
        ventas = ventas.filter(fecha__lte=fecha_hasta)
    
    # Paginación
    paginator = Paginator(ventas, 10)  # 10 ventas por página
    page_number = request.GET.get('page')
    ventas_page = paginator.get_page(page_number)
    
    # Estadísticas básicas
    total_ventas = ventas.aggregate(total=Sum('total'))['total'] or 0
    cantidad_ventas = ventas.count()
    
    context = {
        'ventas': ventas_page,
        'search_query': search_query,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'total_ventas': total_ventas,
        'cantidad_ventas': cantidad_ventas,
    }
    
    return render(request, 'ventas/index.html', context)


def detalle_venta(request, venta_id):
    """Vista para mostrar el detalle de una venta específica"""
    venta = get_object_or_404(Venta, id=venta_id)
    venta_productos = Venta_Producto.objects.filter(venta_id=venta)
    
    context = {
        'venta': venta,
        'venta_productos': venta_productos,
    }
    
    return render(request, 'ventas/detalle_venta.html', context)


@login_required
def nueva_venta(request):
    """Vista para crear una nueva venta"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            cliente_id = request.POST.get('cliente_id')
            productos_data = request.POST.getlist('productos')
            cantidades = request.POST.getlist('cantidades')
            
            cliente = get_object_or_404(User, id=cliente_id)
            
            # Validar que hay productos seleccionados
            if not productos_data or not cantidades:
                messages.error(request, 'Debe seleccionar al menos un producto.')
                return redirect('nueva_venta')
            
            total_venta = Decimal('0.00')
            productos_venta = []
            
            # Validar productos y calcular total
            for i, producto_id in enumerate(productos_data):
                if i < len(cantidades) and cantidades[i]:
                    producto = get_object_or_404(Producto, id=producto_id)
                    cantidad = int(cantidades[i])
                    
                    # Verificar stock disponible
                    if producto.stock < cantidad:
                        messages.error(request, f'Stock insuficiente para {producto.nombre}. Stock disponible: {producto.stock}')
                        return redirect('nueva_venta')
                    
                    precio_unitario = producto.precio
                    subtotal = precio_unitario * cantidad
                    total_venta += subtotal
                    
                    productos_venta.append({
                        'producto': producto,
                        'cantidad': cantidad,
                        'precio_unitario': precio_unitario,
                        'subtotal': subtotal
                    })
            
            # Crear la venta principal
            venta = Venta.objects.create(
                producto=productos_venta[0]['producto'],  # Producto principal
                cliente=cliente,
                cantidad=sum(item['cantidad'] for item in productos_venta),
                fecha=timezone.now().date(),
                total=total_venta
            )
            
            # Crear los detalles de la venta y actualizar stock
            for item in productos_venta:
                Venta_Producto.objects.create(
                    venta_id=venta,
                    producto_id=item['producto'],
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio_unitario']
                )
                
                # Actualizar stock
                item['producto'].stock -= item['cantidad']
                item['producto'].save()
            
            messages.success(request, f'Venta creada exitosamente. Total: ${total_venta}')
            return redirect('detalle_venta', venta_id=venta.id)
            
        except Exception as e:
            messages.error(request, f'Error al crear la venta: {str(e)}')
            return redirect('nueva_venta')
    
    # GET request - mostrar formulario
    productos = Producto.objects.filter(stock__gt=0).order_by('nombre')
    clientes = User.objects.all().order_by('username')
    
    context = {
        'productos': productos,
        'clientes': clientes,
    }
    
    return render(request, 'ventas/nueva_venta.html', context)


def buscar_productos(request):
    """API endpoint para buscar productos por AJAX"""
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(
        nombre__icontains=query,
        stock__gt=0
    ).values('id', 'nombre', 'precio', 'stock')[:10]
    
    return JsonResponse(list(productos), safe=False)


def estadisticas_ventas(request):
    """Vista para mostrar estadísticas de ventas"""
    # Estadísticas generales
    total_ventas = Venta.objects.aggregate(total=Sum('total'))['total'] or 0
    cantidad_ventas = Venta.objects.count()
    
    # Ventas por mes (últimos 6 meses)
    from django.db.models import Count
    from datetime import datetime, timedelta
    
    seis_meses_atras = timezone.now().date() - timedelta(days=180)
    ventas_por_mes = Venta.objects.filter(
        fecha__gte=seis_meses_atras
    ).extra(
        select={'mes': "strftime('%%Y-%%m', fecha)"}
    ).values('mes').annotate(
        total=Sum('total'),
        cantidad=Count('id')
    ).order_by('mes')
    
    # Productos más vendidos
    productos_mas_vendidos = Venta_Producto.objects.values(
        'producto_id__nombre'
    ).annotate(
        total_vendido=Sum('cantidad'),
        total_ingresos=Sum('cantidad') * Sum('precio_unitario')
    ).order_by('-total_vendido')[:10]
    
    # Clientes que más compran
    mejores_clientes = Venta.objects.values(
        'cliente__username',
        'cliente__first_name',
        'cliente__last_name'
    ).annotate(
        total_compras=Sum('total'),
        cantidad_compras=Count('id')
    ).order_by('-total_compras')[:10]
    
    context = {
        'total_ventas': total_ventas,
        'cantidad_ventas': cantidad_ventas,
        'ventas_por_mes': ventas_por_mes,
        'productos_mas_vendidos': productos_mas_vendidos,
        'mejores_clientes': mejores_clientes,
    }
    
    return render(request, 'ventas/estadisticas.html', context)

