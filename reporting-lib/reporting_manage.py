import simplejson as json
from django.utils import timezone
from models import Track


def start(request):
    request.first_request = True
    track = Track()
    track.save()
    print track
    request.session["is_reporting"] = track.id


def stop(request):
    del request.session["is_reporting"]


def generate_report():
    pass
