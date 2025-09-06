from django.shortcuts import get_object_or_404, render
from .models import Product, ProductType
from django.core.paginator import Paginator


def product_detail(request, slug, page=1):
    product = get_object_or_404(Product, slug=slug)
    product_type = ProductType.objects.filter(is_active=True)
    paginator = Paginator(product_type, 6)
    page_obj = paginator.get_page(page)
    return render(request, "product-details.html", {"product": product,
                                                    "product_type": page_obj,
                                                    "default_meta_title": product.meta_title,
                                                    "default_meta_description": product.meta_description,
                                                    "canonical_url": product.canonical_url or request.build_absolute_uri(),
                                                    })


def product_type(request, slug):
    type = get_object_or_404(ProductType, slug=slug, is_active=True)
    return render(request, "product-type.html", {'type': type,
                                                 "default_meta_title": type.meta_title,
                                                 "default_meta_description": type.meta_description,
                                                 "canonical_url": type.canonical_url or request.build_absolute_uri(),
                                                 })
