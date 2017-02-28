from django.db import models


class Track(models.Model):
    user_id = models.IntegerField()


class HttpRequest(models.Model):
    track = models.ForeignKey(Track)
    status_code = models.IntegerField()
    JSON = models.TextField()
