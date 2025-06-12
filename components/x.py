import sys
from urllib.parse import urlparse


class Object(object):
    def __init__(self):
        self.d = {}

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    pass


def rt_assert(cond, hint_on_failure=None):
    if not cond:
        if hint_on_failure is None:
            hint_on_failure = "(no message)"
        raise RuntimeError(hint_on_failure)


def parse_url(schema):  # url -> host, port
    parsed = urlparse(f"//{schema}")  # 补全为 URL 格式
    hostname = parsed.hostname
    port = parsed.port
    if port is None:
        port = 22
    username = parsed.username
    if username is None:
        username = "root"
    return hostname, port, username


def p(*args, **kwargs):
    kwargs["file"] = sys.stdout
    print(*args, **kwargs)


def pe(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)
