from django.contrib import admin
from . import models

# Register your models here.


class BusinessAdmin(admin.ModelAdmin):
    list_display = ("name", "total_amount", "initial_amount", "status")


class BusinessContributionAdmin(admin.ModelAdmin):
    list_display = ("name", "business", "user", "amount", "percentage")


class TransactionLogAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "description", "type", "amount", "business")


class TransactionFileAdmin(admin.ModelAdmin):
    list_display = ("transaction_log", "file_type", "file_name")


admin.site.register(models.Business, BusinessAdmin)
admin.site.register(models.BusinessContribution, BusinessContributionAdmin)
admin.site.register(models.TransactionLog, TransactionLogAdmin)

admin.site.register(models.TransactionFile)
