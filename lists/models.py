from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class AppUser(User):
    pass


class Actor(models.Model):
    kp_id = models.IntegerField()
    name = models.CharField(max_length=50)
    photo = models.URLField()


class Director(models.Model):
    kp_id = models.IntegerField()
    name = models.CharField(max_length=50)
    photo = models.URLField()


class Writer(models.Model):
    kp_id = models.IntegerField()
    name = models.CharField(max_length=50)
    photo = models.URLField()


class Genre(models.Model):
    name = models.CharField(max_length=50)
    watch_counter = models.IntegerField(default=0)


class Film(models.Model):
    kp_id = models.IntegerField()
    name = models.CharField(max_length=50)
    countries = models.JSONField()
    genres = models.ManyToManyField(Genre)
    directors = models.ManyToManyField(Director)
    actors = models.ManyToManyField(Actor)
    writers = models.ManyToManyField(Writer)
    budget = models.IntegerField()
    fees = models.IntegerField()
    premiere = models.DateTimeField()
    description = models.TextField()
    short_description = models.TextField()
    slogan = models.TextField()
    duration = models.IntegerField()
    poster = models.URLField()
    rating_kp = models.DecimalField(decimal_places=3, max_digits=4)
    rating_imdb = models.DecimalField(decimal_places=3, max_digits=4)
    votes_kp = models.IntegerField()
    votes_imdb = models.IntegerField()
    watch_date = models.DateTimeField()


class Sticker(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
