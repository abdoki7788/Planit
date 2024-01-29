from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from jdatetime import date as jdate
import persian

# Create your views here.

class DashboardOverview(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "today_tasks_count": persian.convert_en_numbers(request.user.tasks.filter(for_date=jdate.today()).count()),
            "reminders_count": persian.convert_en_numbers(request.user.reminders.count()),
            "pins_count": persian.convert_en_numbers(request.user.pins.count()),
            "overdue_tasks_count": persian.convert_en_numbers(request.user.tasks.filter(for_date__lt=jdate.today()).count()),

            "pins": request.user.pins.filter(untill__gte=jdate.today(), is_pinned=True),
            "today": jdate.today()
        }
        return render(request, "dashboard/overview.html", context=context)

class PinRemoveView(LoginRequiredMixin, View):
    def get(self, request, id):
        pin = get_object_or_404(models.Pin, id=id)
        pin.is_pinned = False
        pin.save()
        return redirect("dashboard:overview")
