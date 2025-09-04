from django.urls import path
from . import views

app_name = "product"


urlpatterns = [
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path("<slug:slug>/page/<int:page>/", views.product_detail, name="product_detail_page"),
    path('product-type/<slug:slug>/', views.product_type, name='product_type'),
]
