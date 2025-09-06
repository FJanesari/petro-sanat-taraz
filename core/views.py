from django.shortcuts import render, get_object_or_404
from product.models import Product
from .models import HomeInfo, FanFact, AboutUsPost, Setting, AboutUsInfo, ContactUsInfo, ContactMessage
from blog.models import Article
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def home(request):
    products = Product.objects.all()
    banner = HomeInfo.objects.filter(is_active=True).first()
    fanfacts = FanFact.objects.filter(is_active=True)
    about_us_posts = AboutUsPost.objects.filter(is_active=True)[:4]
    blog = Article.objects.filter(is_active=True)[:4]
    setting = Setting.objects.filter(is_active=True).first()
    return render(request, 'home/index.html', {
        "products": products,
        "banner": banner,
        "fanfacts": fanfacts,
        "about_us_posts": about_us_posts,
        "blog": blog,
        "setting": setting,
    })


def contact(request):
    banner = ContactUsInfo.objects.filter(is_active=True).first()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "پیام شما با موفقیت ارسال شد ✅")
            return redirect("home:contact")  # ری‌دایرکت به همون صفحه
        else:
            messages.error(request, "لطفاً فرم را به درستی پر کنید ❌")
    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"contact_us": banner, "form": form})


def about(request):
    banner = AboutUsInfo.objects.filter(is_active=True).first()
    posts = AboutUsPost.objects.filter(is_active=True)

    # فرض: پست پیش‌فرض (اولین پست)
    default_post = posts.first()

    return render(request, "about/about.html", {
        "about_us": banner,
        "post": default_post,
        "posts": posts,
    })


def about_detail(request, slug):
    banner = AboutUsInfo.objects.filter(is_active=True).first()
    posts = AboutUsPost.objects.filter(is_active=True)
    post = get_object_or_404(AboutUsPost, is_active=True, slug=slug)

    return render(request, "about/about.html", {
        "about_us": banner,
        "post": post,
        "posts": posts,
    })
