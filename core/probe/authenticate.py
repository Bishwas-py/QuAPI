import functools

from core.entities.user import User


def authenticate(func):
    def wrapper(*args, **kw):
        request = args[0]
        if request.authorization:
            return func(*args, **kw)
        return "Unauthorized Request", "401 Unauthorized"

    return wrapper


def make_jwt(user: User):
    username = user.username
    email = user.email

    return f"{username}:{email}"
