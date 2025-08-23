from django import forms #Importa el módulo de formularios de Django (forms), que te permite crear formularios HTML directamente desde Python.
from .models import Compra  # Asegúrate de tener el modelo Compra
#-----------------------------------------------------------------------------------------------------------------------
class CompraForm(forms.ModelForm): #Creas una clase CompraForm que hereda de forms.ModelForm.
    class Meta:  #La clase interna Meta sirve para darle a Django instrucciones sobre cómo construir el formulario.
        model = Compra #Le dices a Django que este formulario se basa en el modelo Compra.
        fields = ['producto', 'cliente', 'precio_unitario', 'cantidad', 'fecha', 'total','ganancia', 'creado_en']
        widgets = {
            'precio_unitario': forms.TextInput(),
            'total': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
#-----------------------------------------------------------------------------------------------------------------------