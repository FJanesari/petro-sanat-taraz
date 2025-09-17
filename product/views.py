from django.shortcuts import get_object_or_404, render
from .models import Product, ProductType
from django.core.paginator import Paginator


def product_detail(request, slug, page=1):
    product = get_object_or_404(Product, slug=slug)

    # فقط نوع‌های مربوط به همین محصول
    product_types = product.types.filter(is_active=True)

    paginator = Paginator(product_types, 6)
    page_obj = paginator.get_page(page)

    return render(request, "product-details.html", {
        "product": product,
        "product_type": page_obj,  # page_obj برای pagination
        "default_meta_title": product.meta_title,
        "default_meta_description": product.meta_description,
        "og_title": product.og_title or product.meta_title or product.title,
        "og_description": product.og_description or product.meta_description,
        "og_image": product.og_image.url if product.og_image else None,
        "meta_robots": product.meta_robots,
        "canonical_url": product.canonical_url or request.build_absolute_uri(),
    })


def product_type(request, slug):
    type = get_object_or_404(ProductType, slug=slug, is_active=True)
    return render(request, "product-type.html", {'type': type,
                                                 "default_meta_title": type.meta_title,
                                                 "default_meta_description": type.meta_description,
                                                 "og_title": type.og_title or type.meta_title or type.title,
                                                 "og_description": type.og_description or type.meta_description,
                                                 "og_image": type.og_image.url if type.og_image else None,
                                                 "meta_robots": type.meta_robots,
                                                 "canonical_url": type.canonical_url or request.build_absolute_uri(),
                                                 })
