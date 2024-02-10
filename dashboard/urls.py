from django.urls import path
from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.DashboardOverview.as_view(), name="overview"),
    path("pins/<int:id>/", views.PinRemoveView.as_view(), name="pin-remove"),
    path("tasks/add/", views.TaskAddView.as_view(), name="task-add"),
    path("tasks/<int:id>/", views.TaskEditView.as_view(), name="task-edit"),
    path("tasks/<int:id>/done/", views.TaskDoneView.as_view(), name="task-done"),
    path("tasks/<int:id>/delete/", views.TaskDeleteView.as_view(), name="task-delete")
]
