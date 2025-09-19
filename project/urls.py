from django.urls import path
from . import views

app_name = "project"


urlpatterns = [
    path('', views.project, name='project'),
    path('page/<int:page>/', views.project, name='project_page'),
    path('<slug:slug>/', views.project_detail, name='project_detail'),
]
