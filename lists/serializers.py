from rest_framework import serializers

from lists.models import Film, Genre


class FilmSerializer(serializers.HyperlinkedModelSerializer):
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
