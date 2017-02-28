from django.db import connections
from django.template import Template, Context

class LoggingMiddleware(object):

    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR', '') or request.META.get('HTTP_X_FORWARDED_FOR', '')
        print ('%s %s %s' % (request.user, request.path, ip))


    def process_response(self, request, response):
        for connection_name in connections:
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
                print t.render(Context({'sqllog': connection.queries}))
        ip = request.META.get('REMOTE_ADDR', '') or request.META.get('HTTP_X_FORWARDED_FOR', '')
        print('resp %s %s %s %s' % (request.user, request.path, ip, response.status_code))
        return response
