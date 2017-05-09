from django.utils import timezone

import simplejson as json
from django.db import models
from .utils import HTTP_STATUS_CODES
from datetime import datetime


class Track(models.Model):
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '[{0}] Track #{1}'.format(self.time, self.id)

    def get_time_str(self):
        return json.dumps(self.time.strftime('%Y-%m-%dT%H:%M:%S'))

    def save_with_time(self, time, commit=True):
        self.time = time
        if commit:
            self.save()


class HttpRequest(models.Model):
    track = models.ForeignKey(Track)
    execution_time = models.TextField()
    time = models.DateTimeField(default=timezone.now, db_index=True)

    # response information
    status_code = models.SmallIntegerField(choices=HTTP_STATUS_CODES, default=200)
    # content = models.TextField()

    # request information
    method = models.CharField(max_length=7, default='GET')
    path = models.CharField(max_length=255)
    vars = models.TextField(default="No vars")
    is_secure = models.BooleanField(default=False)
    is_ajax = models.BooleanField(default=False)

    # user information
    ip = models.GenericIPAddressField()
    user = models.CharField(max_length=255, blank=True, null=True)
    referer = models.URLField(max_length=255, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '[{0}] - {1} {2} {3} {4}'.format(self.time, self.method, self.path, self.status_code, self.user)

    def save_request(self, track, request, response=None, commit=True):
        self.execution_time = str(response.logging_end_time - response.logging_start_time) + "s"
        self.track = track
        self.method = request.method
        self.path = request.path[:255]
        if request.GET:
            self.vars = json.dumps(request.GET)
        elif request.POST:
            self.vars = json.dumps(request.POST)
        self.is_secure = request.is_secure
        self.is_ajax = request.is_ajax

        self.ip = request.META.get('REMOTE_ADDR', '')
        self.referer = request.META.get('HTTP_REFERER', '')[:255]
        self.user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]

        if response:
            self.status_code = response.status_code
            self.content = response.content

        if hasattr(request, 'user') and hasattr(request.user, 'is_authenticated'):
            if request.user.is_authenticated:
                self.user = request.user

        if commit:
            self.save()


class Sql(models.Model):
    http_request = models.ForeignKey(HttpRequest)
    query = models.TextField()


class Log(models.Model):
    http_request = models.ForeignKey(HttpRequest)
    message = models.CharField(max_length=255)
