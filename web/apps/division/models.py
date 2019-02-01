from django.db import models

from core.models import TimeStampedModel
# Create your models here.


class Division(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'division'


class Level(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100, blank=True)
    division = models.ForeignKey(Division, related_name='levels')

    def __str__(self):
        return '{} -- {}'.format(self.division.name, self.name)

    class Meta:
        db_table = 'level'
