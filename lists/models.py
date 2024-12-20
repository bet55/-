import pendulum
from django.contrib.auth.models import User
from django.db import models

from lists import validators

QUESTION_MARK_URL = 'https://banner2.cleanpng.com/20180715/yag/aavjmwzok.webp'


# Create your models here.
class AppUser(User):
    avatar = models.URLField(default=QUESTION_MARK_URL)


class Actor(models.Model):
    mgr = models.Manager()
    kp_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    photo = models.URLField(default=QUESTION_MARK_URL)


class Director(models.Model):
    mgr = models.Manager()
    kp_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    photo = models.URLField(default=QUESTION_MARK_URL)


class Writer(models.Model):
    mgr = models.Manager()
    kp_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    photo = models.URLField(default=QUESTION_MARK_URL)


class FilmGenreRelations(models.Model):
    film = models.ForeignKey('Film', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    # Заработало без этой моделе. Я ничего не понял.
    # https://stackoverflow.com/questions/64462130/how-to-change-the-primary-key-of-manytomany-table-in-django
    # https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.ManyToManyField.through


class Genre(models.Model):
    mgr = models.Manager()
    name = models.CharField(max_length=50, primary_key=True)
    watch_counter = models.IntegerField(default=0)


class Film(models.Model):
    # class CustomJSONField(models.JSONField):
    #
    #     def get_prep_value(self, value):
    #         import json
    #         if value is None:
    #             return value
    #         # Почему не работает????????????????????????
    #         return json.dumps(value, ensure_ascii=False)

    mgr = models.Manager()
    kp_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, validators=[validators.validate_name])
    countries = models.JSONField(default=list(('unknown',)))
    genres = models.ManyToManyField(Genre)
    # genres = models.ManyToManyField(Genre, through=FilmGenreRelations)
    directors = models.ManyToManyField(Director)
    actors = models.ManyToManyField(Actor)
    writers = models.ManyToManyField(Writer)
    budget = models.IntegerField(default=0)
    fees = models.IntegerField(default=0)
    premiere = models.DateTimeField(default='1900-01-24T09:27:20.807Z')
    description = models.TextField(default='...')
    short_description = models.TextField(default='...')
    slogan = models.TextField(default='...')
    duration = models.IntegerField(default=0)
    poster = models.URLField(default=QUESTION_MARK_URL)
    rating_kp = models.DecimalField(default=0.0, decimal_places=3, max_digits=4)
    rating_imdb = models.DecimalField(default=0.0, decimal_places=3, max_digits=4)
    votes_kp = models.IntegerField(default=0)
    votes_imdb = models.IntegerField(default=0)
    watch_date = models.DateTimeField(null=True)
    is_archive = models.BooleanField(default=False)

    class Meta:
        ordering = ['-rating_kp']


class Sticker(models.Model):
    mgr = models.Manager()
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    text = models.TextField(default='И сказать нечего...')
    rating = models.IntegerField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'film'], name='user_film_key'),
        ]
