from django.shortcuts import render
from product.models import Product


def home(request):
    products = Product.objects.all()
    return render(request, 'home/index.html', {"products": products})
