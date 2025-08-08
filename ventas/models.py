from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.
# Clase Categoria
# Si quieres que el campo cliente esté relacionado con un usuario, SIEMPRE usa ForeignKey. Así puedes acceder a todos los datos del usuario y mantener integridad referencial.
User = get_user_model()  # para hacer referencia a un tipo de usuario(cliente o proveedor) que se ha creado en el sistema


# Clase Producto
class Venta(models.Model):
    producto = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE, related_name='ventas')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='ventas')  # aquí uso el modelo de usuario que se ha creado en el sistema
    cantidad = models.IntegerField()
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    creado_en = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.producto.nombre


# Clase Proveedor
class Venta_Producto(models.Model):
    venta_id = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='venta_productos')
    producto_id = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE, related_name='venta_productos')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    creado_en = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.venta_id
