from django.db import models
import pendulum
from lists.models import Film


class Postcard(models.Model):
    meeting_date = models.DateTimeField()
    movies = models.ManyToManyField(Film)
    created_at = models.DateTimeField(default=pendulum.now('Asia/Yekaterinburg'))