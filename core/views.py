from django.shortcuts import render
from product.models import Product
from .models import HomeInfo


def home(request):
    products = Product.objects.all()
    banner = HomeInfo.objects.filter(is_active=True).first()
    return render(request, 'home/index.html', {"products": products, "banner": banner})


def contact(request):
    return render(request, "contact/contact.html")


def about(request):
    return render(request, "about/about.html")
