from rest_framework import serializers

from lists.models import Film, Genre, AppUser


class FilmSerializer(serializers.HyperlinkedModelSerializer):
#TODO: serialize foreign tables

    premiere = serializers.DateTimeField(format="%d/%m/%Y")

    class Meta:
        model = Film
        fields = ['kp_id', 'name', 'poster', 'premiere', 'description', 'duration', 'rating_kp', 'is_archive']


class FilmSmallSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Film
        fields = ['kp_id', 'poster']


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
