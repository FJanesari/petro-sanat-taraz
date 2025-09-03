from .models import Setting
from product.models import Product


def global_context(request):
    setting = Setting.objects.first()
    products = Product.objects.all()

    return {
        "setting": setting,
        "products": products,
    }
