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
    paginator = Paginator(article, 6)
    page_obj = paginator.get_page(page)
    return render(request, "blog.html", {
        "article": page_obj,
        "blog_info": blog_info,
        "default_meta_title": blog_info.meta_title,
        "default_meta_description": blog_info.meta_description,
        "meta_robots": blog_info.meta_robots,
    })
