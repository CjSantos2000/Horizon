from django.urls import path

from . import views

urlpatterns = [
    path("", views.HorizonDashboardView.as_view(), name="dashboard"),
]
