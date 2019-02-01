from django.db import models

from apps.member.models import Level, Profile
from core.models import TimeStampedModel

# Create your models here.


class LevellingInfo(TimeStampedModel):
    location = models.CharField(max_length=255)
    accuracy_weight = models.FloatField(default=0.0)
    speed_weight = models.FloatField(default=0.0)
    technique_weight = models.FloatField(default=0.0)
    knowledge_weight = models.FloatField(default=0.0)
    physic_weight = models.FloatField(default=0.0)
    mental_weight = models.FloatField(default=0.0)
    division = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    pass_score = models.FloatField(max_length=100)
    profile = models.ManyToManyField(
        Profile, through='Levelling', related_name='lev_info')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'LevellingInfo - %s : %s' % (self.location, self.created)

    class Meta:
        db_table = 'levelling_info'


class Levelling(TimeStampedModel):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='levellings')
    lev_info = models.ForeignKey(
        LevellingInfo, on_delete=models.CASCADE, related_name='levellings')
    accuracy_point = models.FloatField(default=0.0)
    speed_point = models.FloatField(default=0.0)
    technique_point = models.FloatField(default=0.0)
    knowledge_point = models.FloatField(default=0.0)
    physic_point = models.FloatField(default=0.0)
    mental_point = models.FloatField(default=0.0)

    def __str__(self):
        return 'Levelling - %s : %s' % (self.created)

    class Meta:
        db_table = 'levelling'


class AssesmentWeight(models.Model):
    accuracy = models.FloatField(default=0.0)
    speed = models.FloatField(default=0.0)
    technique = models.FloatField(default=0.0)
    knowledge = models.FloatField(default=0.0)
    physic = models.FloatField(default=0.0)
    mental = models.FloatField(default=0.0)
    level = models.OneToOneField(Level, on_delete=models.CASCADE)

    def __str__(self):
        return '{} : ({}, {}, {}, {}, {}, {})'.format(
            self.level.name,
            self.accuracy,
            self.speed,
            self.technique,
            self.knowledge,
            self.physic,
            self.mental
        )

    class Meta:
        db_table = 'assesment_weight'
