from django.urls import path

from . import views

urlpatterns = [
    path("<pk>/", views.InventoryDetailView.as_view(), name="inventory-detail"),
]
