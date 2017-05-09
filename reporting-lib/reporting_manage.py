import simplejson as json
from django.utils import timezone


def start(request):
    request.session["new_track"] = json.dumps(timezone.now().strftime('%Y-%m-%dT%H:%M:%S'))


def stop(request):
    del request.session["is_reporting"]


def clear_session_new_track(request):
    del request.session["new_track"]


