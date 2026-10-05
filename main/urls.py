from django.urls import path
from main.views import (
    create_achievement_ajax,
    show_main,
    show_experience,
    show_achievements,
    show_projects,
    create_project,
    get_projects_json,
    delete_project,
    update_project,
    register,
    login_user,
    logout_user,
    toggle_star,
    create_project_ajax,
    toggle_achievement_star,
    get_achievements_json
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("achievements/", show_achievements, name="show_achievements"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/update/", update_project, name="update_project"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("projects/<uuid:project_id>/star/",toggle_star,name="toggle_star",),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
    path("api/achievements/", get_achievements_json, name="get_achievements_json"),
    path("achievements/<uuid:achievement_id>/star/", toggle_achievement_star, name="toggle_achievement_star"),
    path("achievements/add-ajax/", create_achievement_ajax, name="create_achievement_ajax"),
]