from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path("fa/", include("core.urls", namespace="home")),
    path('fa/', include("blog.urls", namespace='blog')),
    path('fa/product/', include("product.urls", namespace='product')),
]

if settings.DEBUG:  # فقط در حالت توسعه
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
