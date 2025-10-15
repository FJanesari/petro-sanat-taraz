from django.shortcuts import get_object_or_404
from product.models import Product
from .models import HomeInfo, FanFact, Setting, AboutUsInfo, ContactUsInfo
from blog.models import Article
from project.models import Project, ProjectInfo
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.http import HttpResponse


def home(request):
    products = Product.objects.all()
    banner = HomeInfo.objects.filter(is_active=True).first()
    fanfacts = FanFact.objects.filter(is_active=True)
    project_posts = Project.objects.filter(is_active=True)[:4]
    blog = Article.objects.filter(is_active=True)[:10]
    setting = Setting.objects.filter(is_active=True).first()
    return render(request, 'home/index.html', {
        "products": products,
        "banner": banner,
        "fanfacts": fanfacts,
        "project_posts": project_posts,
        "blog": blog,
        "setting": setting,
        "default_meta_title": banner.meta_title,
        "default_meta_description": banner.meta_description,
        "canonical_url": banner.canonical_url or request.build_absolute_uri(),
        "og_title": banner.og_title or banner.meta_title or banner.title,
        "og_description": banner.og_description or banner.meta_description,
        "og_image": banner.og_image.url if banner.og_image else None,
        "meta_robots": banner.meta_robots,
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

    return render(request, "contact/contact.html", {
        "contact_us": banner,
        "form": form,
        "default_meta_title": banner.meta_title,
        "default_meta_description": banner.meta_description,
        "canonical_url": banner.canonical_url or request.build_absolute_uri(),
        "og_title": banner.og_title or banner.meta_title or banner.title,
        "og_description": banner.og_description or banner.meta_description,
        "og_image": banner.og_image.url if banner.og_image else None,
        "meta_robots": banner.meta_robots,
    })


def about(request):
    banner = AboutUsInfo.objects.filter(is_active=True).first()

    return render(request, "about/about.html", {
        "about_us": banner,
        "default_meta_title": banner.meta_title,
        "default_meta_description": banner.meta_description,
        "meta_robots": banner.meta_robots,
        "canonical_url": banner.canonical_url or request.build_absolute_uri(),
        "og_title": banner.og_title or banner.meta_title or banner.title,
        "og_description": banner.og_description or banner.meta_description,
        "og_image": banner.og_image.url if banner.og_image else None,
    })


def project(request):
    banner = ProjectInfo.objects.filter(is_active=True).first()

    return render(request, "project.html", {
        "projects": banner,
        "default_meta_title": banner.meta_title,
        "default_meta_description": banner.meta_description,
    })


def project_detail(request, slug):
    banner = ProjectInfo.objects.filter(is_active=True).first()
    posts = Project.objects.filter(is_active=True)
    post = get_object_or_404(Project, is_active=True, slug=slug)

    return render(request, "project_details.html", {
        "projects": banner,
        "post": post,
        "posts": posts,
        "default_meta_title": banner.meta_title,
        "default_meta_description": banner.meta_description,
    })


def robots_txt(request):
    body = "\n".join([
        "User-agent: *",
        "Disallow:",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ])
    return HttpResponse(body, content_type="text/plain")
