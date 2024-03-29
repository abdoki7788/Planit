# Generated by Django 5.0.1 on 2024-01-28 06:53

import datetime
import django.db.models.deletion
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "dashboard",
            "0003_alter_projectmodel_options_alter_taskmodel_options_and_more",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Reminder",
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
                (
                    "date_added",
                    django_jalali.db.models.jDateTimeField(auto_now_add=True),
                ),
                (
                    "remind_date",
                    django_jalali.db.models.jDateField(
                        default=datetime.date(2024, 1, 28)
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                ("description", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[("a", "Awaiting"), ("d", "Done"), ("r", "ReDeclared")],
                        max_length=1,
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
