from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.sitemaps import StaticViewSitemap, AboutUsPostSitemap, ProductSitemap, ProductTypeSitemap,\
    ArticleSitemap, ProjectSitemap, ProjectDetailSitemap
from core.views import robots_txt
from django.contrib.sitemaps import views as sitemap_views

sitemaps = {
    "static": StaticViewSitemap,
    "about_posts": AboutUsPostSitemap,
    "products": ProductSitemap,
    "product_types": ProductTypeSitemap,
    "articles": ArticleSitemap,
    "projects": ProjectSitemap,
    "project_details": ProjectDetailSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('fa/product/', include("product.urls", namespace='product')),
    path('fa/project/', include("project.urls", namespace="project")),
    path("fa/", include("core.urls", namespace="home")),
    path('fa/', include("blog.urls", namespace='blog')),
    path("sitemap.xml", sitemap_views.index, {"sitemaps": sitemaps}),
    path("sitemap-<section>.xml", sitemap_views.sitemap, {"sitemaps": sitemaps},
         name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
]

if settings.DEBUG:  # فقط در حالت توسعه
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
