import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_seed_experiences'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('event', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('academic', 'Academic'), ('non-academic', 'Non-Academic')], default='non-academic', max_length=20)),
                ('description', models.TextField()),
                ('year', models.IntegerField()),
            ],
        ),
    ]
