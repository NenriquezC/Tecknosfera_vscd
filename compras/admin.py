from django.contrib import admin
from . models import Compra, Compra_Producto



# Register your models here.

class CompraAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cliente', 'precio_unitario',  'cantidad', 'fecha', 'total', 'creado_en')


class Compra_ProductoAdmin(admin.ModelAdmin):
    list_display = ('compra_id', 'producto_id', 'cantidad', 'precio_unitario', 'creado_en')



admin.site.register(Compra, CompraAdmin)
admin.site.register(Compra_Producto, Compra_ProductoAdmin)
