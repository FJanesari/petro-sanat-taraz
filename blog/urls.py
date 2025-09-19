from django.urls import path
from . import views

app_name = "blog"


urlpatterns = [
    path('blog/', views.blog, name='blog'),
    path('blog/page/<int:page>/', views.blog, name='blog_page'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
]
