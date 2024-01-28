from django.contrib import admin
from .models import ProjectModel, TaskModel, Reminder, Pin

# Register your models here.

admin.site.register(TaskModel)
admin.site.register(ProjectModel)
admin.site.register(Reminder)
admin.site.register(Pin)
