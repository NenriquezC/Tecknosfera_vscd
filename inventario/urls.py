from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.inicio, name='inicio'),  # ← Este nombre es el que usas en tu template
    path('inventario/', views.inventario, name='inventario'),
    path('producto/agregar/', views.agregar_producto, name='agregar_producto'),
    path('producto/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),

]
