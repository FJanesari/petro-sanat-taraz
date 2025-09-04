from django.shortcuts import get_object_or_404, render
from .models import Article, BlogInfo
from django.core.paginator import Paginator


def blog_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, "blog-details.html", {"article": article})


def blog(request, page=1):
    article = Article.objects.filter(is_active=True)
    blog_info = get_object_or_404(BlogInfo)
    paginator = Paginator(article, 6)
    page_obj = paginator.get_page(page)
    return render(request, "blog.html", {
        "article": page_obj,
        "blog_info": blog_info,
    })
