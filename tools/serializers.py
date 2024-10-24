from rest_framework import serializers

from lists.models import AppUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppUser
        fields = ['username', 'first_name', 'last_name', 'avatar']
