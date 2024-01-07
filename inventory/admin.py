from django.contrib import admin
from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "business",
        "name",
        "description",
        "price",
        "quantity",
        "warning_quantity",
    )
    list_filter = ("business",)
    search_fields = ("name",)


@admin.register(models.ProductHistory)
class ProductHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "business", "description", "type", "date_added")
    list_filter = ("business", "type")
    search_fields = ("description",)
