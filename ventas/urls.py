from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ventas_index'),
    path('nueva/', views.nueva_venta, name='nueva_venta'),
    path('detalle/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    path('estadisticas/', views.estadisticas_ventas, name='estadisticas_ventas'),
    path('api/buscar-productos/', views.buscar_productos, name='buscar_productos'),
]
