from django.contrib import admin
from .models import Producto, Categoria, Proveedor

# Register your models here.
"""
¿Por qué debe ser una clase?
Django usa el patrón de clases para configurar opciones avanzadas y comportamientos personalizados para cada modelo en el admin.
Al heredar de admin.ModelAdmin, puedes definir atributos (como list_display, search_fields, list_filter, etc.) y métodos para controlar exactamente cómo se administra el modelo.

"""


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'proveedor', 'categoria', 'creado_en')


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'email','rubro', 'creado_en')


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Proveedor, ProveedorAdmin)