import logging


class TypeSubRequest:
    def __init__(self):
        pass

    SQL = 'SQL'
    LOG = 'LOG'
    HTTP_REQUEST = 'HTTP_REQUEST'

    choices = (
        (SQL, 'Sql'),
        (LOG, 'Log'),
        (HTTP_REQUEST, 'Http Request')
    )


class OldFunctionToPatch:
    def __init__(self):
        pass

    debug = logging.debug
    info = logging.info
    error = logging.error
    critical = logging.critical
    exception = logging.exception


HTTP_STATUS_CODES = (

    # 1xx Infomational
    (100, 'Continue'),
    (101, 'Switching Protocols'),
    (102, 'Processing (WebDAV)'),

    # 2xx Success
    (200, 'OK'),
    (201, 'Created'),
    (202, 'Accepted'),
    (203, 'Non-Authoritative Information'),
    (204, 'No Content'),
    (205, 'Reset Content'),
    (206, 'Partial Content'),
    (207, 'Multi-Status (WebDAV)'),

    # 3xx Redirection
    (300, 'Multiple Choices'),
    (301, 'Moved Permanently'),
    (302, 'Found'),
    (303, 'See Other'),
    (304, 'Not Modified'),
    (305, 'Use Proxy'),
    (306, 'Switch Proxy'),
    (307, 'Temporary Redirect'),
    (308, 'Permanent Redirect'),

    # 4xx Client Error
    (400, 'Bad Request'),
    (401, 'Unauthorized'),
    (402, 'Payment Required'),
    (403, 'Forbidden'),
    (404, 'Not Found'),
    (405, 'Method Not Allowed'),
    (406, 'Not Acceptable'),
    (407, 'Proxy Authentication Required'),
    (408, 'Request Timeout'),
    (409, 'Conflict'),
    (410, 'Gone'),
    (411, 'Length Required'),
    (412, 'Precondition Failed'),
    (413, 'Payload Too Large'),
    (414, 'URI Too Long'),
    (415, 'Unsupported Media Type'),
    (416, 'Range Not Satisfiable'),
    (417, 'Expectation Failed'),
    (418, 'I\'m a teapot'),
    (421, 'Misdirected Request'),
    (422, 'Unprocessable Entity (WebDAV)'),
    (423, 'Locked (WebDAV)'),
    (424, 'Failed Dependency (WebDAV)'),
    (426, 'Upgrade Required'),
    (428, 'Precondition Required'),
    (429, 'Too Many Requests'),
    (431, 'Request Header Fields Too Large'),
    (451, 'Unavailable For Leagal Reasons'),

    # 5xx Server Error
    (500, 'Internal Server Error'),
    (501, 'Not Implemented'),
    (502, 'Bad Gateway'),
    (503, 'Service Unavailable'),
    (504, 'Gateway Timeout'),
    (505, 'HTTP Version Not Supported'),
    (506, 'Variant Also Negotiates'),
    (507, 'Insufficient Storage (WebDAV)'),
    (508, 'Loop Detected (WebDAV)'),
    (510, 'Not Extended'),
    (511, 'Network Authentication Required'),
)
