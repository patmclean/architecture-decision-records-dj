# Generated by Django 4.2 on 2023-04-12 15:30

import architecture_decision_records.decisions.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("decisions", "0002_status_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="Decision",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(null=True, unique=True)),
                ("stakeholder", models.CharField(max_length=255)),
                ("title", models.CharField(max_length=255)),
                ("context", models.TextField()),
                ("decision_description", models.TextField(blank=True)),
                ("consequence", models.TextField(blank=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "status",
                    models.ForeignKey(
                        default=architecture_decision_records.decisions.models.Status.get_status,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="decisions.status",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "verbose_name": "Decision Record",
                "ordering": ["-id"],
            },
        ),
    ]
