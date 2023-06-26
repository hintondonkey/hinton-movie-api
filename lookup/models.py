
from django.conf import settings
from django.db import models
from hintonmovie.models import BaseCreateModel


class Category(BaseCreateModel):
    name = models.CharField(max_length=250)
    description = models.TextField(null=False, blank=False)
    image = models.CharField(max_length=250, null=True, blank=False)

    @property
    def total_stream_platform(self):
        num = 0
        try:
            num = self.stream_platform_caterogy.count()
        except Exception as e:
            num = 0
            print(e)
        return num


