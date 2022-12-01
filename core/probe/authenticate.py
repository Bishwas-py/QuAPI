import functools


def authenticate(func):
    def wrapper(*args, **kw):
        request = args[0]
        if request.authorization:
            return func(*args, **kw)
        return "Unauthorized Request", "401 Unauthorized"

    return wrapper
