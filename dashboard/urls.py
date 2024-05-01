from django.urls import path
from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.DashboardOverview.as_view(), name="overview"),
    path("pins/<int:id>/delete/", views.PinRemoveView.as_view(), name="pin-delete"),

    path("reminders/", views.DashboardRemindersView.as_view(), name="reminders-list"),
    path("reminders/add/", views.ReminderAddView.as_view(), name="reminder-add"),
    path("reminders/<int:id>/delete/", views.ReminderDeleteView.as_view(), name="reminder-remove"),
    path("reminders/<int:id>/redeclare/", views.ReminderRedeclareView.as_view(), name="reminder-redeclare"),

    path("notes/", views.DashboardNotesView.as_view(), name="notes-list"),
    path("notes/add/", views.NoteAddView.as_view(), name="note-add"),
    path("notes/<int:id>/", views.NoteEditView.as_view(), name="note-edit"),
    path("notes/<int:id>/delete/", views.NoteDeleteView.as_view(), name="note-delete"),

    path("tasks/", views.DashboardTasksView.as_view(), name="tasks-list"),
    path("tasks/add/", views.TaskAddView.as_view(), name="task-add"),
    path("tasks/<int:id>/", views.TaskEditView.as_view(), name="task-edit"),
    path("tasks/<int:id>/done/", views.TaskDoneView.as_view(), name="task-done"),
    path("tasks/<int:id>/delete/", views.TaskDeleteView.as_view(), name="task-delete")
]
