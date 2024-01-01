from django.urls import path
from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.DashboardOverview.as_view(), name="overview")
]
