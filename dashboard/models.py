from django.db import models
from django.db.models import Case, Value, When
from django.contrib.auth import get_user_model
from colorfield.fields import ColorField
from django_jalali.db.models import jDateField, jDateTimeField
from jdatetime import date as jdate

User = get_user_model()

# Create your models here.

class TaskQuerySet(models.QuerySet):
    date_order = Case(
        When(for_date=jdate.today(), then=Value(1)),
        When(for_date__lt=jdate.today(), then=Value(2)),
        When(for_date__gt=jdate.today(), then=Value(3)),
    )
    def order_by_date(self):
        return self.alias(date_order=self.date_order).order_by("date_order", "for_date", "date_added")


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
    for_date = jDateField(blank=True, null=True,default=jdate.today())
    is_done = models.BooleanField(default=False)
    for_project = models.ForeignKey(ProjectModel, on_delete=models.DO_NOTHING, null=True, blank=True)

    objects = TaskQuerySet.as_manager()

    def __str__(self):
        return f"{self.user} ==> {self.name}"

    def is_overdue(self):
        return jdate.today() > self.for_date

    def is_for_today(self):
        return jdate.today() == self.for_date

    class Meta:
        verbose_name = "کار"
        verbose_name_plural = "کارها"
        ordering = ("-for_date",)


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
    is_pinned = models.BooleanField(default=True)
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return f"{self.user} ==> {self.name}"
    
    class Meta:
        verbose_name = "سنجاق"
        verbose_name_plural = "سنجاق ها "


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    date_added = jDateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)
    description = models.TextField()
