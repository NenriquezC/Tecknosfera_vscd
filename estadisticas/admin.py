from django.contrib import admin
from .models import Estadistica


# Register your models here.

class EstadisticaAdmin(admin.ModelAdmin):
    list_display = ('tipo_venta', 'fecha_inicio', 'fecha_fin', 'total_ventas', 'total_compras', 'ganancias', 'perdidas')


admin.site.register(Estadistica, EstadisticaAdmin)
