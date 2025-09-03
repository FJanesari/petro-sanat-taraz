from django.shortcuts import render, get_object_or_404
from product.models import Product
from .models import HomeInfo, FanFact, AboutUsPost


def home(request):
    products = Product.objects.all()
    banner = HomeInfo.objects.filter(is_active=True).first()
    fanfacts = FanFact.objects.filter(is_active=True)
    about_us_posts = AboutUsPost.objects.filter(is_active=True)[:4]
    return render(request, 'home/index.html', {
        "products": products,
        "banner": banner,
        "fanfacts": fanfacts,
        "about_us_posts": about_us_posts,
    })


def contact(request):
    return render(request, "contact/contact.html")


def about(request):
    return render(request, "about/about.html")


def about_detail(request, slug):
    post = get_object_or_404(AboutUsPost, slug=slug, is_active=True)
    return render(request, "about/about.html", {"post": post})
