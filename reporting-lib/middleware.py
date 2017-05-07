import time
from django.db import connections
from django.template import Template, Context
from models import HttpRequest, Track


class LoggingMiddleware(object):
    def process_request(self, request):
        if request.path == "/favicon.ico":
            return None

        request.logging_start_time = time.time()

    def process_response(self, request, response):
        if request.path == "/favicon.ico":
            return response

        track = Track()
        track.save()
        print '----------------'
        print track
        response.logging_end_time = time.time()
        response.logging_start_time = request.logging_start_time
        http_request = HttpRequest()
        http_request.save_request(track, request, response)
        print http_request
        print '----------------'

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
            print '------'
        """
        return response
