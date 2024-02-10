from django.core.exceptions import PermissionDenied
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from . import forms
from jdatetime import date as jdate
import persian

# Create your views here.

class DashboardOverview(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "today_tasks_count": persian.convert_en_numbers(request.user.tasks.filter(for_date=jdate.today(), is_done=False).count()),
            "reminders_count": persian.convert_en_numbers(request.user.reminders.count()),
            "pins_count": persian.convert_en_numbers(request.user.pins.count()),
            "overdue_tasks_count": persian.convert_en_numbers(request.user.tasks.filter(for_date__lt=jdate.today(), is_done=False).count()),

            "pins": request.user.pins.filter(untill__gte=jdate.today(), is_pinned=True),
            "today": jdate.today(),
            "task_form": forms.TaskCreateForm(),

            "tasks": request.user.tasks.filter(for_date=jdate.today())
        }
        return render(request, "dashboard/overview.html", context=context)

class PinRemoveView(LoginRequiredMixin, View):
    def get(self, request, id):
        pin = get_object_or_404(models.Pin, id=id)
        pin.is_pinned = False
        pin.save()
        return redirect("dashboard:overview")

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
