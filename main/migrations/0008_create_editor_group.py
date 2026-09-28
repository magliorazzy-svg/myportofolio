from django.contrib.auth.models import Group
from django.db import migrations

def create_editor_group(apps,schema_editor):
    Group.objects.get_or_create(name="Editor")

def remove_editor_group(apps, schema_editor):
    Group.objects.filter(name="Editor").delete()

class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_project_starred_by"),    
    ]

    operations =  [
        migrations.RunPython(create_editor_group, remove_editor_group),
    ]