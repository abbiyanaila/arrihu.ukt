"""
Class for Generic Models
"""
from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Make this class abstract
        """
        abstract = True


class Setting(TimeStampedModel):
    property = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return '%s : %s' % (self.property, self.value)

    class Meta:
        db_table = 'setting'
        