from django.contrib import admin
from . import models

# Register your models here.


admin.site.register(models.Business)
admin.site.register(models.BusinessContribution)
admin.site.register(models.TransactionLog)
admin.site.register(models.TransactionFile)
