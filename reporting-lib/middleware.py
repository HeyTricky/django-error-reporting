import time
from django.db import connections
from django.template import Template, Context
from models import HttpRequest, Track
from datetime import datetime
import pytz
from reporting_manage import clear_session_new_track


class LoggingMiddleware(object):
    def process_request(self, request):

        if "new_track" in request.session:
            if not request.session["new_track"] == Track.objects.last().get_time_str() and Track.objects.last() \
                    or not Track.objects:
                track = Track()
                track_datetime = datetime.strptime(request.session["new_track"], '"%Y-%m-%dT%H:%M:%S"').replace(
                    tzinfo=pytz.utc)
                track.save_with_time(track_datetime)
                print track
                request.session["is_reporting"] = "true"

        if "is_reporting" in request.session:

            if request.path == "/favicon.ico":
                return None

            request.logging_start_time = time.time()

    def process_response(self, request, response):

        if Track.objects.last() and "new_track" in request.session:
            if request.session["new_track"] == Track.objects.last().get_time_str():
                clear_session_new_track(request)

        if "is_reporting" in request.session:

            if request.path == "/favicon.ico":
                return response

            response.logging_end_time = time.time()
            response.logging_start_time = request.logging_start_time
            http_request = HttpRequest()
            track = Track.objects.last()
            http_request.save_request(track, request, response)
            print http_request

            """
            for connection_name in connections:
                connection = connections[connection_name]
                if connection.queries:
                    con_time = sum([float(q['time']) for q in connection.queries])
                    header = Template("{{name}}: {{count}} quer{{count|pluralize:\"y,ies\"}} in {{time}} seconds")
                    print header.render(Context({
                        'name': connection_name,
                        'sqllog': connection.queries,
                        'count': len(connection.queries),
                        'time': con_time
                    }))
                    t = Template(
                        "{% for sql in sqllog %}"
                        "[{{forloop.counter}}] {{sql.time}}s: {{sql.sql|safe}}"
                        "{% if not forloop.last %}\n\n"
                        "{% endif %}"
                        "{% endfor %}")
                    print t.render(Context({'sqllog': connection.queries}))
                print '------'"""
        return response
