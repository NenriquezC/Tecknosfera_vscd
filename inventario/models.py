from django.db import models
from django.utils import timezone


# Create your models here.
# Clase Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


# Clase Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    stock_minimo = models.IntegerField(default=0)
    proveedor = models.ForeignKey('inventario.Proveedor', on_delete=models.CASCADE, related_name='productos')
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name='productos')
    creado_en = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre


# Clase Proveedor
class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    tipo_usuario = models.CharField(max_length=50, choices=[
        ('empresa', 'Empresa'),
        ('particular', 'Particular')
    ])
    # proveedor = models.ForeignKey('productos.Producto', on_delete=models.CASCADE, related_name='proveedores')
    rubro = models.CharField(max_length=100)
    creado_en = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre