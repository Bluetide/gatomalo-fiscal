from functools import wraps
from flask import Blueprint, request, abort, Response
from os import environ


def check_auth(username, password):
    return username == environ.get('ADMIN_USERNAME') and password == environ.get('ADMIN_PASSWORD')


def authenticate():
    return Response('Porfavor ingresar credenciales', 401, {'WWW-Authenticate': 'Basic realm=""'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
