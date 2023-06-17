
from django.conf import settings
from django.db import models


class BaseCreateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Category(BaseCreateModel):
    name = models.CharField(max_length=250)
    description = models.TextField(null=False, blank=False)
    image = models.CharField(max_length=250, null=True, blank=False)