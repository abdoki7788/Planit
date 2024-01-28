# Generated by Django 5.0.1 on 2024-01-28 06:07

import colorfield.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ProjectModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                (
                    "color",
                    colorfield.fields.ColorField(
                        default="rgb(255, 255, 255)",
                        image_field=None,
                        max_length=25,
                        samples=[
                            ("#FFFFFF", "white"),
                            ("#000000", "black"),
                            ("#666666", "gray"),
                        ],
                    ),
                ),
                ("status", models.CharField(max_length=64)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
