import sys

from django.db import migrations

# title, event, category, description, year
SEED = [
    (
        "Gold Medalist of Math Competition",
        "ONSB (Olimpiade Nasional Sains dan Bahasa)",
        "academic",
        "Won the gold medal in the mathematics category.",
        2025,
    ),
    (
        "Gold Medalist of Biology Competition",
        "ISMO",
        "academic",
        "Won the gold medal in the biology category.",
        2024,
    ),
    (
        "2x Winner",
        "Al-Azhar Travelling Research Product and Design Competition",
        "non-academic",
        "Won the competition two years in a row.",
        2024,
    ),
]


def seed_achievements(apps, schema_editor):
    if "test" in sys.argv:
        return

    Achievement = apps.get_model("main", "Achievement")
    if Achievement.objects.exists():
        return

    for title, event, category, description, year in SEED:
        Achievement.objects.create(
            title=title,
            event=event,
            category=category,
            description=description,
            year=year,
        )


def unseed_achievements(apps, schema_editor):
    Achievement = apps.get_model("main", "Achievement")
    Achievement.objects.filter(title__in=[row[0] for row in SEED]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_achievement"),
    ]

    operations = [
        migrations.RunPython(seed_achievements, unseed_achievements),
    ]
