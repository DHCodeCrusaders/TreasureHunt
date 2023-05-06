import functools

import jwt
from flask import g, request

from app.utils.utils import build_response


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("token")
        if not token:
            response = build_response(message="Token is missing")
            return response, 401

        try:
            g.login_details = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        except jwt.InvalidTokenError:
            response = build_response(message="Token is invalid")
            return response, 401

        return func(*args, **kwargs)

    return wrapper
