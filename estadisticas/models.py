from django.db import models
# from django.utils import timezone

# Create your models here.
# Clase Estadistica que almacena información sobre las ventas y compras
# y sus ganancias y pérdidas en un periodo de tiempo determinado.
class Estadistica(models.Model):
    tipo_venta = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total_ventas = models.DecimalField(max_digits=10, decimal_places=2)
    total_compras = models.DecimalField(max_digits=10, decimal_places=2)
    ganancias = models.DecimalField(max_digits=10, decimal_places=2)
    perdidas = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Estadistica {self.tipo_venta} desde {self.fecha_inicio} hasta {self.fecha_fin}"
