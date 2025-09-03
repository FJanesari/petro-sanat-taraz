from django.shortcuts import get_object_or_404, render
from .models import Article


def blog_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, "", {"article": article})
