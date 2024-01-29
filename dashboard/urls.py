from django.urls import path
from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.DashboardOverview.as_view(), name="overview"),
    path("pins/<int:id>/", views.PinRemoveView.as_view(), name="pin-remove"),
    path("tasks/add/", views.TaskAddView.as_view(), name="task-add"),
]
