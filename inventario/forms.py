from django import forms # Importa el módulo de formularios de Django
from .models import Producto, Proveedor # Importa el modelo Producto definido en tu proyecto.
#el formulario de Productos
class ProductoForm(forms.ModelForm): #Hereda de forms.ModelForm, lo que significa que es un formulario basado en un modelo (en este caso, Producto).
    class Meta:
        model = Producto #Le dice al formulario que se base en el modelo Producto.
        fields = '__all__'  # Usará todos los campos de Producto
        #fields = ['nombre', 'categoria', 'precio', 'stock'] se puede cambiar all por esto
        widgets = { # Define los widgets para los campos del formulario
            'stock_minimo': forms.NumberInput(attrs={'readonly': 'readonly'}),}
#El formulario de Proveedores
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'