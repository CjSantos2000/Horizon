import uuid
from django.db import models

# Create your models here.


class BaseModel(models.Model):
    slug = models.CharField(
        default=uuid.uuid4,
        max_length=40,
        editable=False,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
