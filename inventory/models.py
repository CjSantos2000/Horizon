from django.db import models
from core.models import BaseModel
from business.models import Business

# Create your models here.


class Product(BaseModel):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    warning_quantity = models.IntegerField()

    def __str__(self):
        return self.name


class ProductHistory(BaseModel):
    class Types(models.TextChoices):
        ADD = "ADD"
        REMOVE = "REMOVE"
        UPDATE = "UPDATE"

    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=100)
    date_added = models.DateField()

    def __str__(self):
        return self.product.name + self.created_at.strftime("%d-%m-%Y %H:%M:%S")
