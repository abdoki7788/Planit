from django.db import models
from django.contrib.auth import get_user_model
from colorfield.fields import ColorField
from django_jalali.db.models import jDateField, jDateTimeField
from jdatetime import date as jdate

User = get_user_model()

# Create your models here.


class ProjectModel(models.Model):
    COLOR_PALETTE = [
        (
            "#FFFFFF",
            "white",
        ),
        (
            "#000000",
            "black",
        ),
        (
            "#666666",
            "gray"
        )
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=64)
    color = ColorField(format="rgb", samples=COLOR_PALETTE)
    status = models.CharField(max_length=64)
    last_activity = jDateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه ها"


class TaskModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(default="در انتظار", max_length=64)
    date_added = jDateTimeField(auto_now_add=True)
    for_date = jDateField(default=jdate.today())
    is_done = models.BooleanField(default=False)
    for_project = models.ForeignKey(ProjectModel, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return f"{self.user} ==> {self.name}"

    class Meta:
        verbose_name = "کار"
        verbose_name_plural = "کارها"


class Reminder(models.Model):
    STATUS_CHOICES = (
        ("a", "Awaiting"),
        ("d", "Done"),
        ("r", "ReDeclared")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reminders")
    date_added = jDateTimeField(auto_now_add=True)
    remind_date = jDateField(default=jdate.today())
    name = models.CharField(max_length=64)
    description = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="a")

    def __str__(self):
        return f"{self.user} ==> {self.name} : {self.status}"
    
    class Meta:
        verbose_name = "یادآور"
        verbose_name_plural = "یادآورها"

class Pin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pins")
    date_added = jDateTimeField(auto_now_add=True)
    untill = jDateField(null=True, blank=True)
    is_pinned = models.BooleanField()
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return f"{self.user} ==> {self.name}"
    
    class Meta:
        verbose_name = "سنجاق"
        verbose_name_plural = "سنجاق ها "
