from rest_framework import serializers
from django.db import models

from lists.models import Film, Genre, AppUser, Sticker


class FilmSerializer(serializers.ModelSerializer):
    premiere = serializers.DateTimeField(format="%d/%m/%Y")

    class Meta:
        model = Film
        fields = ['kp_id',
                  'name',
                  'poster',
                  'premiere',
                  'description',
                  'duration',
                  'rating_kp',
                  'is_archive',
                  ]


class FilmSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['kp_id',
                  'poster',
                  ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        notes = instance.sticker_set.all()
        representation['notes'] = StickerSerializer(notes, many=True).data
        return representation


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  ]


class StickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = '__all__'
