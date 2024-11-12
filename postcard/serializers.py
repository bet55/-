from rest_framework import serializers

from lists.serializers import FilmSerializer
from postcard.models import Postcard


class PostcardSerializer(serializers.ModelSerializer):
    movies = FilmSerializer

    class Meta:
        model = Postcard
        fields = '__all__'

    def create(self, validated_data):
        postcard = Postcard(
            meeting_date=validated_data['meeting_date'],
        )
        postcard.save()
        postcard.movies.set(validated_data['movies'])
        return postcard

    def update(self, instance, validated_data):
        instance.meeting_date = validated_data['meeting_date']
        instance.save()
        instance.movies.set(validated_data['movies'])
        return instance
