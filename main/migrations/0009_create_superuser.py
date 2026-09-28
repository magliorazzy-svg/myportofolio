import os

from django.contrib.auth import get_user_model
from django.db import migrations


def create_superuser(apps, schema_editor):
    username = os.getenv("DJANGO_SUPERUSER_USERNAME")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
    email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")

    # Skip entirely if the env vars are not set (e.g. on a fresh checkout
    # where nobody has configured them yet, or during the test suite).
    if not username or not password:
        return

    User = get_user_model()
    if User.objects.filter(username=username).exists():
        return

    User.objects.create_superuser(username=username, email=email, password=password)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0008_create_editor_group"),
    ]

    operations = [
        migrations.RunPython(create_superuser, noop),
    ]
