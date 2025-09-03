from django.shortcuts import get_object_or_404, render
from .models import Article, BlogInfo


def blog_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, "blog-details.html", {"article": article})


def blog(request):
    article = get_object_or_404(Article)
    blog_info = get_object_or_404(BlogInfo)
    return render(request, "blog.html", {
        "article": article,
        "blog_info": blog_info,
    })
