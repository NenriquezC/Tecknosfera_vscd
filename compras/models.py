from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.
# Clase Categoria
# Si quieres que el campo cliente esté relacionado con un usuario, SIEMPRE usa ForeignKey. Así puedes acceder a todos los datos del usuario y mantener integridad referencial.
User = get_user_model()  # para hacer referencia a un tipo de usuario(cliente o proveedor) que se ha creado en el sistema

#-----------------------------------------------------------------------------------------------------------------------
# Clase Producto
class Compra(models.Model):
    producto = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE, related_name='compras')
    #proveedor = models.ForeignKey('inventario.Proveedor', on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compras')  # aquí uso el modelo de usuario que se ha creado en el sistema
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    #precio_venta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cantidad = models.IntegerField()
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    ganancia = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Porcentaje de ganancia sobre el precio de compra (ejemplo: 20.00 para 20%)" )
    creado_en = models.DateTimeField(default=timezone.now)

    # El decorador @property convierte el método precio_venta en una propiedad de solo lectura.
    # Permite que puedas acceder a compra.precio_venta como si fuera un atributo, sin usar paréntesis (no compra.precio_venta(), sino compra.precio_venta).
    @property
    def precio_venta(self):
        """Calcula el precio de venta basado en el precio_unitario y la ganancia."""
        return self.precio_unitario * (1 + self.ganancia / 100)

    #def save(self, *args, **kwargs):
    #    # Calcular el precio_venta antes de guardar
    #    if self.precio_unitario is not None and self.ganancia is not None:
    #        self.precio_venta = self.precio_unitario * (1 + self.ganancia / 100)
    #    # Calcular total de compra
    #    if self.precio_unitario and self.cantidad:
    #        self.total_compra = self.precio_unitario * self.cantidad
    #  super().save(*args, **kwargs)


    # Este método __str__ es para que cuando imprimas una instancia de Compra, te muestre el nombre del producto.
    def __str__(self):
        if self.producto: # and  hasattr(self.producto, "nombre"):
            return str(self.producto.nombre)
        else:
            return "Sin producto"


#-----------------------------------------------------------------------------------------------------------------------
# Clase Proveedor
class Compra_Producto(models.Model):
    compra_id = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='compra_productos')
    producto_id = models.ForeignKey('inventario.producto', on_delete=models.CASCADE, related_name='compra_productos')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    creado_en = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.compra_id) if self.compra_id is not None else "Sin compra"

#-----------------------------------------------------------------------------------------------------------------------