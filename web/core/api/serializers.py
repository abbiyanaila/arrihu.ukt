from rest_framework import serializers
from core import models as core_models


class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.FCMDevice
        fields = ['registration_id', 'device_id']
