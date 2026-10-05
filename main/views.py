from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.http import HttpResponse, JsonResponse 
from main.forms import ProjectForm, AchievementForm
from main.models import Experience, Achievement, Project
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required 
from django.core.exceptions import PermissionDenied       
import datetime
from django.views.decorators.http import require_POST


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'No active login session / Cookie not found')
    context = {
        "name": "Maglio Razzy Effendy",
        "npm": "2506553616",
        "study_program": "S1 Ilmu Komputer KKI",
        "bio": (
            "A Computer Science student at Universitas Indonesia interested "
            "in software development and education."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Maglio Razzy Effendy",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_achievements(request):
    context = {
        "name": "Maglio Razzy Effendy",
        "achievement_list": Achievement.objects.all(),
    }
    return render(request, "achievements.html", context)

def get_achievements_json(request):
    title_query = request.GET.get("title", "").strip()
    achievements = Achievement.objects.prefetch_related("starred_by").order_by("-year")

    if title_query:
        achievements = achievements.filter(title__icontains=title_query)

    data = []
    for achievement in achievements:
        starred_users = achievement.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        data.append({
            "pk": str(achievement.id),
            "fields": {
                "title": achievement.title,
                "event": achievement.event,
                "category": achievement.get_category_display(),
                "description": achievement.description,
                "year": achievement.year,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": ", ".join(u.username for u in starred_users),
            },
        })
    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def toggle_achievement_star(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)

    if request.method == "POST":
        if request.user in achievement.starred_by.all():
            achievement.starred_by.remove(request.user)
        else:
            achievement.starred_by.add(request.user)

    return redirect("main:show_achievements")

@require_POST
def create_achievement_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse({"message": "Only the portfolio owner can add achievements."}, status=403)

    form = AchievementForm(request.POST)
    if form.is_valid():
        achievement = form.save()
        return JsonResponse({"message": "Achievement added successfully.", "pk": str(achievement.id)}, status=201)

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@login_required(login_url="/login")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")
    context = {"name": "Maglio Razzy Effendy", "form": form}
    return render(request, "projects_form.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Manually build the JSON data so we can add the Star logic
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "project_image_url": project.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)


def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Burhan",
        "title_query": title_query,
        "form": ProjectForm(),

    }
    return render(request, "projects.html", context)


@login_required(login_url="/login")   
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")
    return redirect("main:show_projects")

@login_required(login_url="/login") 
def update_project(request, project_id):
    is_editor = request.user.groups.filter(name="Editor").exists()
    if not (request.user.is_superuser or is_editor):
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_projects")
    context = {"name": "Maglio Razzy Effendy", "form": form}
    return render(request, "projects_form.html", context)

#-------TUTORIAL 4-------
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("main:login")

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# No is_superuser check: any logged-in account may give a star
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # If this account has already starred it, remove the star.
        # If not, add one.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")


@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add projects."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Project added successfully.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

