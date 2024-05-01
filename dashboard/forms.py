from django import forms
from . import models

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = models.TaskModel
        fields = ["name", "description", "for_date"]

class ReminderForm(forms.ModelForm):
    class Meta:
        model = models.Reminder
        fields = ["name", "description", "remind_date"]

class NoteForm(forms.ModelForm):
    class Meta:
        model = models.Note
        fields = ["title", "description"]
