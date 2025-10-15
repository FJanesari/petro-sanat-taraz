from django.shortcuts import get_object_or_404, render
from .models import Article, BlogInfo
from django.core.paginator import Paginator


def blog_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    query = request.GET.get("q")
    if query:

        recent_posts = Article.objects.filter(title__icontains=query).exclude(id=article.id)[:3]
    else:

        recent_posts = Article.objects.exclude(id=article.id).order_by("-created_at")[:3]
    return render(request, "blog-details.html", {"article": article,
                                                 "recent_posts": recent_posts,
                                                 "query": query,
                                                 "default_meta_title": article.meta_title,
                                                 "default_meta_description": article.meta_description,
                                                 "og_title": article.og_title or article.meta_title or article.title,
                                                 "og_description": article.og_description or article.meta_description,
                                                 "og_image": article.og_image.url if article.og_image else None,
                                                 "meta_robots": article.meta_robots,
                                                 "canonical_url": article.canonical_url or request.build_absolute_uri(),
                                                 })


# def blog_list(request):
#     query = request.GET.get("q", "")
#     posts = Article.objects.all().order_by("-created_at")
#
#     if query:
#         posts = posts.filter(title__icontains=query)
#
#     return render(request, "blog.html", {
#         "posts": posts,
#         "query": query,
#     })


def blog(request, page=1):
    article = Article.objects.filter(is_active=True)
    blog_info = get_object_or_404(BlogInfo)
    paginator = Paginator(article, 9)
    page_obj = paginator.get_page(page)
    return render(request, "blog.html", {
        "article": page_obj,
        "blog_info": blog_info,
        "default_meta_title": blog_info.meta_title,
        "default_meta_description": blog_info.meta_description,
        "og_title": blog_info.og_title or blog_info.meta_title or blog_info.title,
        "og_description": blog_info.og_description or blog_info.meta_description,
        "og_image": blog_info.og_image.url if blog_info.og_image else None,
        "meta_robots": blog_info.meta_robots,
        "canonical_url": blog_info.canonical_url or request.build_absolute_uri(),
    })
