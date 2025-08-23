from django.urls import path
from . import views
from .views import agregar_compra


app_name = 'compras'

urlpatterns = [
    path('agregar/', views.agregar_compra, name='agregar_compra'),
    path('ver/', views.ver_compras, name='ver_compras'),
    path('editar/<int:compra_id>/', views.editar_compra, name='editar_compra'),
    path('eliminar/<int:compra_id>/', views.eliminar_compra, name='eliminar_compra'),
    path('seleccionar_editar/', views.seleccionar_editar_compra, name='seleccionar_editar_compra'),
    path('seleccionar_eliminar/', views.seleccionar_eliminar_compra, name='seleccionar_eliminar_compra'),
]