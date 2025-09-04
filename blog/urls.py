from django.urls import path
from . import views

app_name = "blog"


urlpatterns = [
    path('blog/', views.blog, name='blog'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    path("<slug:slug>/page/<int:page>/", views.blog_detail, name="blog_detail_page"),
]
