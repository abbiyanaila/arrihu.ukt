from rest_framework import serializers
from apps.member.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user', 'level', 'physic', 'organization']
