# Generated by Django 5.0.1 on 2024-01-28 06:30

import datetime
import django.db.models.deletion
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="projectmodel",
            name="last_activity",
            field=django_jalali.db.models.jDateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name="TaskModel",
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
                ("description", models.TextField(blank=True, null=True)),
                ("status", models.CharField(default="در انتظار", max_length=64)),
                (
                    "date_added",
                    django_jalali.db.models.jDateTimeField(
                        default=datetime.datetime(2024, 1, 28, 10, 0, 16, 793852)
                    ),
                ),
                ("for_date", django_jalali.db.models.jDateField(blank=True, null=True)),
                ("is_done", models.BooleanField(default=False)),
                (
                    "for_project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="dashboard.projectmodel",
                    ),
                ),
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
