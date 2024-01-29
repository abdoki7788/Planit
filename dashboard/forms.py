from django import forms
from . import models

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = models.TaskModel
        fields = ["name", "description", "for_date"]
