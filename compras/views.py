from django.http import HttpResponse
from .models import Compra
from django.shortcuts import render


# Create your views here.
def index(request):
    # productos = Producto.objects.all()
    return HttpResponse("esta es la view de compras y compras productos") 