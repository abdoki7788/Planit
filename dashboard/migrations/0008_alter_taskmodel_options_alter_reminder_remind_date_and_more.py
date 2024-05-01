# Generated by Django 5.0.1 on 2024-04-30 04:18

import datetime
import django.db.models.deletion
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_alter_pin_options_alter_pin_is_pinned_alter_pin_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskmodel',
            options={'ordering': ('-for_date',), 'verbose_name': 'کار', 'verbose_name_plural': 'کارها'},
        ),
        migrations.AlterField(
            model_name='reminder',
            name='remind_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 4, 30)),
        ),
        migrations.AlterField(
            model_name='taskmodel',
            name='for_date',
            field=django_jalali.db.models.jDateField(blank=True, default=datetime.date(2024, 4, 30), null=True),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
