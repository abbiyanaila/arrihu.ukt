import os
import time
import shutil

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver

from versatileimagefield.fields import VersatileImageField

from core.models import TimeStampedModel
from apps.organization.models import Organization
from apps.division.models import Division, Level

from config.base import BASE_DIR
# Create your models here.


def profile_picture(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{}.{}".format(instance.user.username, ext)
    return os.path.join('user/{}/profile'.format(instance.id), filename)

# def profile_qrcode(instance, filename):
#     ext = filename.split('.')[-1]
#     filename = "profile_{}_qrcode.{}".format(instance.id, ext)
#     return os.path.join('user/{}/qrcode'.format(instance.id), filename)


class Physic(models.Model):
    body_weight = models.CharField(max_length=5)
    body_height = models.CharField(max_length=5)
    arm_span = models.CharField(max_length=5)
    full_draw = models.CharField(max_length=5)
    over_draw = models.CharField(max_length=5)
    hospital_history = models.TextField()
    blood_group = models.CharField(max_length=5)

    def __str__(self):
        return self.body_weight

    class Meta:
        db_table = 'physic'


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
    gender = models.CharField(max_length=25)
    born_place = models.CharField(max_length=100)
    born_date = models.DateField(auto_now=False, auto_now_add=False)
    religion = models.CharField(
        max_length=100, default='Islam', blank=True, null=False)
    identity_number = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    level = models.ForeignKey(Level, related_name='profiles')
    physic = models.OneToOneField(Physic, on_delete=models.CASCADE)
    picture = VersatileImageField(
        upload_to=profile_picture)
    # qrcode = VersatileImageField(
    #     upload_to=profile_qrcode)
    organization = models.ForeignKey(Organization, related_name='profiles')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'profile'


@receiver(models.signals.post_delete, sender=Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    os.remove(instance.picture.path)
    instance.picture.delete_all_created_images()


@receiver(models.signals.pre_save, sender=Profile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_picture = Profile.objects.get(pk=instance.pk).picture
        # old_qrcode = Profile.objects.get(pk=instance.pk).qrcode
    except Profile.DoesNotExist:
        return False

    new_picture = instance.picture
    if not old_picture == new_picture:
        if old_picture:
            if os.path.isfile(old_picture.path):
                os.remove(old_picture.path)

    # new_qrcode = instance.qrcode
    # if not old_qrcode == new_qrcode:
    #     if old_qrcode:
    #         if os.path.isfile(old_qrcode.path):
    #             os.remove(old_qrcode.path)
