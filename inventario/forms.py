from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'  # Usará todos los campos de Producto
        #fields = ['nombre', 'categoria', 'precio', 'stock'] se puede cambiar all por esto