from django.contrib.auth.models import User
from django.db import models

QUESTION_MARK_URL = 'https://banner2.cleanpng.com/20180715/yag/aavjmwzok.webp'


# Create your models here.
class AppUser(User):
    pass


class Actor(models.Model):
    _actor_manager = models.Manager()
    kp_id = models.IntegerField()
    name = models.CharField(max_length=50)
    photo = models.URLField(default=QUESTION_MARK_URL)


class Director(models.Model):
    _direcotr_manager = models.Manager()
    kp_id = models.IntegerField()
    name = models.CharField(max_length=50)
    photo = models.URLField(default=QUESTION_MARK_URL)


class Writer(models.Model):
    _writer_manager = models.Manager()
    kp_id = models.IntegerField()
    name = models.CharField(max_length=50)
    photo = models.URLField(default=QUESTION_MARK_URL)


class Genre(models.Model):
    _genre_manager = models.Manager()
    name = models.CharField(max_length=50)
    watch_counter = models.IntegerField(default=0)


class Film(models.Model):
    _film_manager = models.Manager()
    kp_id = models.IntegerField()
    name = models.CharField(max_length=50)
    countries = models.JSONField(null=True)
    genres = models.ManyToManyField(Genre)
    directors = models.ManyToManyField(Director)
    actors = models.ManyToManyField(Actor)
    writers = models.ManyToManyField(Writer)
    budget = models.IntegerField(default=0)
    fees = models.IntegerField(default=0)
    premiere = models.DateTimeField(null=True)
    description = models.TextField(default='...', null=True)
    short_description = models.TextField(default='...', null=True)
    slogan = models.TextField(default='...', null=True)
    duration = models.IntegerField(default=0)
    poster = models.URLField(default=QUESTION_MARK_URL)
    rating_kp = models.DecimalField(default=0.0, decimal_places=3, max_digits=4)
    rating_imdb = models.DecimalField(default=0.0, decimal_places=3, max_digits=4)
    votes_kp = models.IntegerField(default=0)
    votes_imdb = models.IntegerField(default=0)
    watch_date = models.DateTimeField(null=True)
    is_archive = models.BooleanField(default=False)


class Sticker(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()

