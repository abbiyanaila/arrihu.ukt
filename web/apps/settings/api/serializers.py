from django.contrib.auth import authenticate
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer,
    jwt_payload_handler,
    jwt_encode_handler,
)


class JWTLoginSerializer(JSONWebTokenSerializer):
    def validate(self, kwargs):

        credentials = {
            'username': kwargs.get('username'),
            'password': kwargs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(request=self.context['request'], **credentials)
            if user:
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                return Response({
                    'message': 'User Found!',
                    'data': {
                        'token': token
                    }
                },  status=status.HTTP_200_OK)
            else:
                Response({
                    'message': 'User Not Found!',
                    'data': None
                },  status=status.HTTP_200_OK)
        else:
            raise serializers.ValidationError(
                'Credential must containt Username and Password')
