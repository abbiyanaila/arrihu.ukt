from django.db import models
from core.models import TimeStampedModel
# Create your models here.


class Organization(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'organization'