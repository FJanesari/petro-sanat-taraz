from django.shortcuts import render
from product.models import Product
from .models import HomeInfo, FanFact


def home(request):
    products = Product.objects.all()
    banner = HomeInfo.objects.filter(is_active=True).first()
    fanfacts = FanFact.objects.filter(is_active=True)
    return render(request, 'home/index.html', {"products": products, "banner": banner, "fanfacts": fanfacts})


def contact(request):
    return render(request, "contact/contact.html")


def about(request):
    return render(request, "about/about.html")
