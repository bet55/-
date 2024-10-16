from rest_framework import serializers

from lists.models import Film, Genre


class FilmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Film
        fields = ['kp_id', 'name', 'poster', 'premiere', 'description', 'duration', 'rating_kp', 'is_archive']


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'watch_counter']
