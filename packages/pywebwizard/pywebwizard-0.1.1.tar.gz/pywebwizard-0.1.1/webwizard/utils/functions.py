from .exceptions import FieldError
import re


def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def required_fields(fields: list):
    def wrapper(f):
        def wrapped(*args, **kwargs):
            _action = args[1]
            for _field in fields:
                if _field not in _action.keys():
                    raise FieldError(f"'{_field}' not defined in config for {_action.get('action')}")
            return f(*args, **kwargs)
        return wrapped
    return wrapper
