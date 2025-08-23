from django import forms #Importa el módulo de formularios de Django (forms), que te permite crear formularios HTML directamente desde Python.
from .models import Venta  # Asegúrate de tener el modelo Compra
#-----------------------------------------------------------------------------------------------------------------------
class VentaForm(forms.ModelForm): #Creas una clase CompraForm que hereda de forms.ModelForm.
    class Meta:  #La clase interna Meta sirve para darle a Django instrucciones sobre cómo construir el formulario.
        model = Venta #Le dices a Django que este formulario se basa en el modelo Compra.
        fields = ['producto', 'cliente', 'precio_unitario', 'descuento',  'cantidad', 'total', 'fecha', 'creado_en']
        widgets = {
            'precio_unitario': forms.TextInput(attrs={'readonly': 'readonly'}),
            'total': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
#-----------------------------------------------------------------------------------------------------------------------