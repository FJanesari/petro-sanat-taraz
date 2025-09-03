from django.shortcuts import get_object_or_404, render
from .models import Product, ProductType
from django.core.paginator import Paginator


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_type = ProductType.objects.filter(is_active=True)
    paginator = Paginator(product_type, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "product-details.html", {"product": product,
                                                    "product_type": page_obj,
                                                    })


def product_type(request):
    return render(request, "product-type.html", {"product_type": product_type})
