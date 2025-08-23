from django.shortcuts import render
from compras.models import Compra
from ventas.models import Venta
from inventario.models import Producto, Proveedor    # <--- CORREGIDO
from django.db.models import Sum, Count
#comparativa_data = [
#    {"rango": "2025-08-01", "valor": 1000},
#    {"rango": "2025-08-02", "valor": 2000},
#    {"rango": "2025-08-03", "valor": 1500},
#]

def home(request):
    # Esta view es para la PÁGINA PRINCIPAL ("/")
    return render(request, "index.html")

def dashboard(request):
    analisis = request.GET.get('analisis')
    periodo = request.GET.get('periodo')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    context = {
        "analisis": analisis,
        "periodo": periodo,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        # Agrega aquí tus datos de ventas_data, compras_data, etc.
    }

    return render(request, "dashboard.html", context)