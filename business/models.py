import uuid
from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel


class Business(BaseModel):
    class Status(models.TextChoices):
        ACTIVE = "Active", "active"
        INACTIVE = "Inactive", "inactive"

    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="owners")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        choices=Status.choices, max_length=10, default=Status.ACTIVE
    )
    data = models.JSONField()

    def __str__(self):
        return f"{self.name} - {self.total_amount}"


class BusinessContribution(BaseModel):
    name = models.CharField(max_length=255)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    percentage = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class TransactionLog(BaseModel):
    class TransactionType(models.TextChoices):
        INCOME = "Income", "income"
        EXPENSE = "Expense", "expense"

    transaction_id = models.CharField(max_length=255, default=uuid.uuid4)
    description = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]


class TransactionFile(BaseModel):
    transaction_log = models.ForeignKey(
        TransactionLog, on_delete=models.SET_NULL, null=True, blank=True
    )
    file = models.FileField(upload_to="transaction_files/")
    file_type = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.transaction_log} - {self.file_name}"
