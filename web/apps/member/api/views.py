from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from ..models import Profile
from .serializers import ProfileSerializer


class ProfileObjectAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, username):
        obj = Profile.objects.filter(user__username=username).first()
        if obj:
            serializer = ProfileSerializer(obj)

            data = {
                'user_id': obj.user.id,
                'username': obj.user.username,
                'profile': serializer.data,
                'physic': {
                    'body_height': obj.physic.body_height,
                    'body_weight': obj.physic.body_weight,
                    'arm_span': obj.physic.arm_span,
                    'full_draw': obj.physic.full_draw,
                    'over_draw': obj.physic.over_draw,
                    'blood_group': obj.physic.blood_group,
                    'hospital_history': obj.physic.hospital_history,
                },
                'division': obj.level.division.name,
                'level': obj.level.name,
                'organization': obj.organization.name,
            }
            response = {
                'error': False,
                'message': 'User dengan No. Registrasi {} Ditemukan'.format(username),
                'data': data
            }
        else:
            response = {
                'error': False,
                'message': 'User dengan No. Registrasi {} Tidak Ditemukan'.format(username),
                'data': None
            }
        return Response(response, status=status.HTTP_200_OK)
