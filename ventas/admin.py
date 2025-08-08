from django.contrib import admin
from .models import Venta, Venta_Producto


# Register your models here.

class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cliente', 'cantidad', 'fecha', 'total', 'creado_en')


class Venta_ProductoAdmin(admin.ModelAdmin):
    list_display = ('venta_id', 'producto_id', 'cantidad', 'precio_unitario', 'creado_en')


admin.site.register(Venta, VentaAdmin)
admin.site.register(Venta_Producto, Venta_ProductoAdmin)