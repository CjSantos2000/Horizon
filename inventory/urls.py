from django.urls import path

from . import views

urlpatterns = [
    path("<pk>/", views.InventoryDetailView.as_view(), name="inventory-detail"),
    path("<pk>/add/", views.AddProductView.as_view(), name="add-product"),
    path(
        "<pk>/update/<product_id>/",
        views.UpdateProductView.as_view(),
        name="update-product",
    ),
    path(
        "<pk>/delete/<product_id>/",
        views.DeleteProductView.as_view(),
        name="delete-product",
    ),
]
