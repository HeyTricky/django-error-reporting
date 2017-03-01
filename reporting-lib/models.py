from time import timezone

import simplejson as json
from django.db import models
from .utils import HTTP_STATUS_CODES


class Track(models.Model):
    time = models.DateTimeField(default=timezone.now)


class HttpRequest(models.Model):
    track = models.ForeignKey(Track)
    execution_time = models.TimeField()
    time = models.DateTimeField(default=timezone.now)
    # response information
    status_code = models.SmallIntegerField(choices=HTTP_STATUS_CODES, default=200)
    # content = models.TextField()

    # request information
    method = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    vars = models.TextField()
    is_secure = models.BooleanField(default=False)
    is_ajax = models.BooleanField(default=False)

    # user information
    ip = models.IPAddressField()
    user = models.CharField(max_length=255, blank=True, null=True)
    referer = models.URLField(max_length=255, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '[{0}] - {1} {2} {3}'.format(self.time, self.method, self.path, self.status_code)

    def save_request(self, request, response=None, commit=True):
        self.execution_time = (request.logging_end_time - request.logging_start_time)

        self.method = request.method
        self.path = request.path[:255]
        self.vars = json.dumps(request.REQUEST.__dict__)
        self.is_secure = request.is_secure()
        self.is_ajax = request.is_ajax()

        self.ip = request.META.get('REMOTE_ADDR', '')
        self.referer = request.META.get('HTTP_REFERER', '')[:255]
        self.user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]

        if response:
            self.status_code = response.status_code
            self.content = response.content

        if hasattr(request, 'user') and hasattr(request.user, 'is_authenticated'):
            if request.user.is_authenticated:  # ???
                self.user = request.user

        if commit:
            self.save()


class Sql(models.Model):
    http_request = models.ForeignKey(HttpRequest)
    query = models.TextField()


class Log(models.Model):
    http_request = models.ForeignKey(HttpRequest)
    message = models.CharField()
