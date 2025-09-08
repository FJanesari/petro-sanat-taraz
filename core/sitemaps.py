from django.contrib.sitemaps import Sitemap
from .models import AboutUsPost
from product.models import Product, ProductType
from blog.models import Article


class StaticViewSitemap(Sitemap):

    def items(self):
        return ["home:home", "home:contact", "home:about"]

    def location(self, item):
        from django.urls import reverse
        return reverse(item)


class AboutUsPostSitemap(Sitemap):

    def items(self):
        return AboutUsPost.objects.filter(is_active=True)

    def lastmod(self, obj):
        if hasattr(obj.updated_at, "togregorian"):
            return obj.updated_at.togregorian()
        return obj.updated_at

    def location(self, obj):
        from django.urls import reverse
        return reverse("home:about_detail", args=[obj.slug])


class ProductSitemap(Sitemap):

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        if hasattr(obj.updated_at, "togregorian"):
            return obj.updated_at.togregorian()
        return obj.updated_at

    def location(self, obj):
        from django.urls import reverse
        return reverse("product:product_detail", args=[obj.slug])


class ProductTypeSitemap(Sitemap):

    def items(self):
        return ProductType.objects.filter(is_active=True)

    def lastmod(self, obj):
        if hasattr(obj.updated_at, "togregorian"):
            return obj.updated_at.togregorian()
        return obj.updated_at

    def location(self, obj):
        from django.urls import reverse
        return reverse("product:product_type", args=[obj.slug])


class ArticleSitemap(Sitemap):

    def items(self):
        return Article.objects.filter(is_active=True)

    def lastmod(self, obj):
        if hasattr(obj.updated_at, "togregorian"):
            return obj.updated_at.togregorian()
        return obj.updated_at

    def location(self, obj):
        from django.urls import reverse
        return reverse("blog:blog_detail", args=[obj.slug])
