import sys
from datetime import datetime, timezone

from django.db import migrations

# title, description, category, ended_at (None = still ongoing)
SEED = [
    (
        "Vice Person In Charge",
        "Represented Liaison Officer as Vice Person In Charge in Open House Fasilkom UI 2026.",
        "volunteer",
        None,
    ),
    (
        "Academics Department Staff",
        "Managed academics resources within BEM Fasilkom UI 2026.",
        "volunteer",
        None,
    ),
    (
        "Staff of Liaison Officer",
        "Guided guest speakers and external partners for Open House Fasilkom UI 2025.",
        "volunteer",
        datetime(2025, 11, 30, tzinfo=timezone.utc),
    ),
    (
        "Event Organizer Committee",
        "Handled logistics and run-of-show coordination for SOSPRO Fasilkom UI 2025.",
        "volunteer",
        datetime(2025, 9, 30, tzinfo=timezone.utc),
    ),
    (
        "Head of Artist Division",
        "Led artist outreach, booking, and hospitality for Coalesce 2024.",
        "volunteer",
        datetime(2024, 12, 15, tzinfo=timezone.utc),
    ),
    (
        "Member of Security Committee",
        "Managed venue security and crowd flow for Alpus INC 9.",
        "volunteer",
        datetime(2023, 8, 20, tzinfo=timezone.utc),
    ),
]


def seed_experiences(apps, schema_editor):
    if "test" in sys.argv:
        return

    Experience = apps.get_model("main", "Experience")
    if Experience.objects.exists():
        return

    for title, description, category, ended_at in SEED:
        Experience.objects.create(
            title=title,
            description=description,
            category=category,
            ended_at=ended_at,
        )


def unseed_experiences(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")
    Experience.objects.filter(title__in=[row[0] for row in SEED]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_experiences, unseed_experiences),
    ]
