from django.shortcuts import get_object_or_404, render
from .models import Project, ProjectInfo
from django.core.paginator import Paginator


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    query = request.GET.get("q")
    if query:

        recent_posts = Project.objects.filter(title__icontains=query).exclude(id=project.id)[:3]
    else:

        recent_posts = Project.objects.exclude(id=project.id).order_by("-created_at")[:3]
    return render(request, "project_details.html", {"project": project,
                                                    "recent_posts": recent_posts,
                                                    "query": query,
                                                    "default_meta_title": project.meta_title,
                                                    "default_meta_description": project.meta_description,
                                                    "og_title": project.og_title or project.meta_title or project.title,
                                                    "og_description": project.og_description or project.meta_description,
                                                    "og_image": project.og_image.url if project.og_image else None,
                                                    "meta_robots": project.meta_robots,
                                                    "canonical_url": project.canonical_url or request.build_absolute_uri(),
                                                    })


def project(request, page=1):
    project = Project.objects.filter(is_active=True)
    project_info = get_object_or_404(ProjectInfo)
    paginator = Paginator(project, 9)
    page_obj = paginator.get_page(page)
    return render(request, "project.html", {
        "project": page_obj,
        "project_info": project_info,
        "default_meta_title": project_info.meta_title,
        "default_meta_description": project_info.meta_description,
        "og_title": project_info.og_title or project_info.meta_title or project_info.title,
        "og_description": project_info.og_description or project_info.meta_description,
        "og_image": project_info.og_image.url if project_info.og_image else None,
        "meta_robots": project_info.meta_robots,
        "canonical_url": project_info.canonical_url or request.build_absolute_uri(),
    })
