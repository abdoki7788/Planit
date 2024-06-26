from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from . import filters
from . import forms
from jdatetime import date as jdate
from persian import convert_en_numbers as cen

# Create your views here.

class DashboardOverview(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        context = {
            "today_tasks_count": cen(user.tasks.filter(for_date=jdate.today(), is_done=False).count()),
            "reminders_count": cen(user.reminders.exclude(status="d").count()),
            "pins_count": cen(user.pins.count()),
            "overdue_tasks_count": cen(user.tasks.filter(for_date__lt=jdate.today(), is_done=False).count()),

            "pins": user.pins.filter(untill__gte=jdate.today(), is_pinned=True),
            "today": jdate.today(),

            "task_form": forms.TaskCreateForm(),
            "tasks": user.tasks.filter(for_date=jdate.today()),
            "today_reminders": user.reminders.filter(remind_date=jdate.today()).exclude(status="d")
        }
        return render(request, "dashboard/overview.html", context=context)

class DashboardTasksView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.TaskCreateForm()
        if not request.GET.get("is_done"):
            f = filters.TaskFilter(request.GET, queryset=request.user.tasks.exclude( Q(is_done=True) & ~Q(for_date=jdate.today())).order_by("-for_date"))
        else:
            f = filters.TaskFilter(request.GET, queryset=request.user.tasks.order_by("-for_date"))

        context = {
            "tasks": f.qs,
            "filter_data": f.data,
            "task_form": form,
            "today": jdate.today()
        }
        return render(request, "dashboard/tasks.html", context)

class DashboardRemindersView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.GET.get("status"):
            f = filters.ReminderFilter(request.GET, queryset=request.user.reminders.exclude(status="d"))
        else:
            f = filters.ReminderFilter(request.GET, queryset=request.user.reminders.all())
            print(f.__dict__)
        context = {
            "reminders": f.qs,
            "filter_data": f.data,
            "reminder_form": forms.ReminderForm,
            "today": jdate.today()
        }
        return render(request, "dashboard/reminders.html", context=context)

class DashboardNotesView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "notes": request.user.notes.all(),
            "note_form": forms.NoteForm,
            "today": jdate.today()
        }
        return render(request, "dashboard/notes.html", context=context)


class NoteAddView(LoginRequiredMixin, View):
    form_class = forms.NoteForm
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return render(request, "components/note.html", {"note": note})
        else:
            print(form.errors)


class NoteEditView(LoginRequiredMixin, View):
    form_class = forms.NoteForm
    def setup(self, request, id, *args, **kwargs):
        self.note = get_object_or_404(models.Note, id=id)
        return super().setup(request, *args, **kwargs)
    def get(self, request, id):
        form = self.form_class(instance=self.note)
        return render(request, "components/note-edit-form.html", {"note": self.note, "note_form": form})
    def post(self, request, id):
        form = self.form_class(instance=self.note, data=request.POST)
        if form.is_valid():
            form.save()
            return render(request, "components/note.html", {"note": self.note})
        else:
            print(form.errors)


class NoteDeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        note = get_object_or_404(models.Note, id=id)
        note.delete()
        return HttpResponse("")


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
        reminder_form = self.form_class(instance=self.reminder, data=request.POST)
        if reminder_form.is_valid():
            ins = reminder_form.save(commit=False)
            ins.status = "r"
            ins.save()
            return render(request, "components/reminder.html", {"reminder": self.reminder})
        else:
            print("error occured")


class ReminderAddView(LoginRequiredMixin, View):
    form_class = forms.ReminderForm
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            return render(request, "components/reminder.html", {"reminder": reminder})
        else:
            print(form.errors)




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


