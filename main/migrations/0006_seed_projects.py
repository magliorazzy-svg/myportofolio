import sys

from django.db import migrations

# title, description, tech_stack, project_url, project_image_url
SEED = [
    (
        "Personal Portfolio Website",
        "A personal portfolio built with Django, HTML5, and CSS3, with a Stranger "
        "Things-inspired design and MVT-driven Experience, Achievement, and Project "
        "sections.",
        "Django, Python, HTML5, CSS3, PostgreSQL",
        "https://github.com/magliorazzy-svg/myportofolio",
        "",
    ),
]


def seed_projects(apps, schema_editor):
    # Don't seed during the test suite - the tests expect a clean table.
    if "test" in sys.argv:
        return

    Project = apps.get_model("main", "Project")
    if Project.objects.exists():
        return

    for title, description, tech_stack, project_url, project_image_url in SEED:
        Project.objects.create(
            title=title,
            description=description,
            tech_stack=tech_stack,
            project_url=project_url,
            project_image_url=project_image_url or None,
        )


def unseed_projects(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    Project.objects.filter(title__in=[row[0] for row in SEED]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_project"),
    ]

    operations = [
        migrations.RunPython(seed_projects, unseed_projects),
    ]
