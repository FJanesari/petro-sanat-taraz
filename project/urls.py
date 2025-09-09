from django.urls import path
from . import views

app_name = "project"


urlpatterns = [
    path('', views.project, name='project'),
    path('<slug:slug>/', views.project_detail, name='project_detail'),
    path("<slug:slug>/page/<int:page>/", views.project_detail, name="project_detail_page"),
]
