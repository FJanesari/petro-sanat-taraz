from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("project/", views.project, name="project"),
    path("project/<slug:slug>/", views.project_detail, name="project_detail"),
]
