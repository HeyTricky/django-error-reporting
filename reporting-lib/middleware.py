import time
from django.db import connections
from django.template import Template, Context
from models import HttpRequest


class LoggingMiddleware(object):
    def process_request(self, request):
        if request.path == "/favicon.ico":
            return None

        request.logging_start_time = time.time()

    def process_response(self, request, response):
        if request.path == "/favicon.ico":
            return response

        request.logging_end_time = time.time()
        HttpRequest.save_request(request, response)

        """for connection_name in connections:
            connection = connections[connection_name]
            if connection.queries:
                time = sum([float(q['time']) for q in connection.queries])
                header = Template("{{name}}: {{count}} quer{{count|pluralize:\"y,ies\"}} in {{time}} seconds")
                print header.render(Context({
                    'name': connection_name,
                    'sqllog': connection.queries,
                    'count': len(connection.queries),
                    'time': time
                }))
                t = Template(
                    "{% for sql in sqllog %}"
                        "[{{forloop.counter}}] {{sql.time}}s: {{sql.sql|safe}}"
                        "{% if not forloop.last %}\n\n"
                        "{% endif %}"
                    "{% endfor %}")
                print t.render(Context({'sqllog': connection.queries}))"""

        return response
