from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from core import models as core_models
from . import serializers


class FCMDeviceCreateView(generics.CreateAPIView):
    model = core_models.FCMDevice
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = serializers.FCMDeviceSerializer

    def perform_create(self, serializer):
        device = core_models.FCMDevice.objects.filter(
            registration_id=serializer.validated_data['registration_id']).first()
        if device:
            instance = device
        else:
            instance = serializer.save()
        return Response(data={
            'error': False,
            'message': 'Data has been saved!',
            'data': {
                'id': instance.pk,
                'registration_id': instance.registration_id
            }
        }, status=status.HTTP_201_CREATED)


class FCMDeviceListView(generics.ListAPIView):
    model = core_models.FCMDevice
    queryset = core_models.FCMDevice.objects.values('id', 'registration_id')
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = serializers.FCMDeviceSerializer

    def list(self, request):
        data = {
            'error': False,
            'message': 'Fetch All Data',
            'data': self.get_queryset()
        }
        return Response(data=data, status=status.HTTP_200_OK)
