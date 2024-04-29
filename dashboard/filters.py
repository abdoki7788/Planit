import django_filters
import jdatetime

from dashboard.models import Reminder, TaskModel

class ReminderFilter(django_filters.FilterSet):
    remind_date = django_filters.CharFilter(method="remind_date_filter")
    class Meta:
        model = Reminder
        fields = ["status", "remind_date"]
    def remind_date_filter(self, queryset, name, value):
        if value == "today":
            value = jdatetime.date.today()
        return queryset.filter(**{
            name: value,
        })


class TaskFilter(django_filters.FilterSet):
    for_date = django_filters.CharFilter(method="for_date_filter")
    class Meta:
        model = TaskModel
        fields = {
            "for_date",
            "is_done"
        }

    def for_date_filter(self, queryset, name, value):
        today = jdatetime.date.today()
        if value == "today":
            value = today
        elif value == "past":
            value = today
            name = "for_date__lt"
        elif value == "upcoming":
            value = today
            name = "for_date__gt"
        return queryset.filter(**{
            name: value,
        })
