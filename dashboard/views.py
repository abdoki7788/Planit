from django.core.exceptions import PermissionDenied
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from . import forms
from jdatetime import date as jdate
from persian import convert_en_numbers as cen

# Create your views here.

class DashboardOverview(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        context = {
            "today_tasks_count": cen(user.tasks.filter(for_date=jdate.today(), is_done=False).count()),
            "reminders_count": cen(user.reminders.count()),
            "pins_count": cen(user.pins.count()),
            "overdue_tasks_count": cen(user.tasks.filter(for_date__lt=jdate.today(), is_done=False).count()),

            "pins": user.pins.filter(untill__gte=jdate.today(), is_pinned=True),
            "today": jdate.today(),

            "task_form": forms.TaskCreateForm(),
            "tasks": user.tasks.filter(for_date=jdate.today()),
            "today_reminders": user.reminders.filter(remind_date=jdate.today(), status="a")
        }
        return render(request, "dashboard/overview.html", context=context)

class DashboardTasksView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.TaskCreateForm()
        context = {
            "tasks": request.user.tasks.filter(is_done=False).order_by_date(),
            "task_form": form,
            "today": jdate.today()
        }
        return render(request, "dashboard/tasks.html", context)

class DashboardRemindersView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "reminders": request.user.reminders.exclude(status="d"),
            "reminder_form": forms.ReminderForm,
            "today": jdate.today()
        }
        return render(request, "dashboard/reminders.html", context=context)

class PinRemoveView(LoginRequiredMixin, View):
    def get(self, request, id):
        pin = get_object_or_404(models.Pin, id=id)
        pin.is_pinned = False
        pin.save()
        return redirect("dashboard:overview")



class ReminderDeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        reminder = get_object_or_404(models.Reminder, id=id)
        reminder.status = "d"
        reminder.save()
        return HttpResponse("")

class ReminderRedeclareView(LoginRequiredMixin, View):
    form_class = forms.ReminderForm
    def setup(self, request, id, *args, **kwargs):
        self.reminder = get_object_or_404(models.Reminder, id=id)
        return super().setup(request, *args, **kwargs)
    def get(self, request, id):
        form = self.form_class(instance=self.reminder)
        return render(request, "components/reminder-redeclare-form.html", {"reminder": self.reminder, "reminder_form": form})
    def post(self, request, id):
        form = self.form_class(instance=self.reminder, data=request.POST)
        if form.is_valid():
            if form.cleaned_data["remind_date"] != self.reminder.remind_date:
                form.cleaned_data["status"] = "r"
            form.save()
            return render(request, "components/reminder.html", {"reminder": self.reminder})




class TaskAddView(LoginRequiredMixin, View):
    form_class = forms.TaskCreateForm
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return render(request, "components/task.html", {"task": task})
        else:
            print(form.errors)

class TaskDeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        task = get_object_or_404(models.TaskModel, id=id)
        task.delete()
        return HttpResponse("")

class TaskEditView(LoginRequiredMixin, View):
    form_class = forms.TaskCreateForm
    def setup(self, request, id, *args, **kwargs):
        self.task = get_object_or_404(models.TaskModel, id=id)
        return super().setup(request, *args, **kwargs)
    def get(self, request, id):
        form = self.form_class(instance=self.task)
        return render(request, "components/task-edit-form.html", {"task": self.task, "task_form": form})
    def post(self, request, id):
        form = self.form_class(instance=self.task, data=request.POST)
        if form.is_valid():
            form.save()
            return render(request, "components/task.html", {"task": self.task})
        else:
            print(form.errors)

class TaskDoneView(LoginRequiredMixin, View):
    def setup(self, request, id, *args, **kwargs):
        self.task = get_object_or_404(models.TaskModel, id=id)
        return super().setup(request, *args, **kwargs)

    def post(self, request, id):
        self.task.is_done = not self.task.is_done
        self.task.save()
        return render(request, "components/task.html", {"task": self.task})
