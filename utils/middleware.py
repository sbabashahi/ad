import jwt
from flask import g, request
from functools import wraps

from user.models import User
from utils import exceptions, responses


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            user = handle_jwt_decode(request)
        except exceptions.CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()
        g.user = user
        return f(*args, **kwargs)
    return decorated_function


def handle_jwt_decode(req):
    auth = req.headers.get('Authorization', None)
    if auth is None or auth == '':
        raise exceptions.CustomException(detail='You have no Authorization')
    if auth.startswith('JWT '):
        token = auth.split()
        if len(token) == 1:
            raise exceptions.CustomException(detail='Invalid Authorization header. No credentials provided.')
        if len(token) > 2:
            raise exceptions.CustomException(detail='Invalid Authorization header. should not contain spaces.')
        try:
            user_id = jwt.decode(token[1], options={"verify_signature": False})['sub']
        except jwt.exceptions.PyJWTError as e:
            raise exceptions.CustomException(detail='Token not verified.')
        user = User.query.get(user_id)
        if user:
            try:
                jwt.decode(token[1], user.secret, algorithms='HS256')
            except jwt.exceptions.PyJWKError as e:
                raise exceptions.CustomException(detail='Token not verified.')
            return user
        else:
            raise exceptions.CustomException(detail='Invalid token.')
    else:
        raise exceptions.CustomException(detail='Invalid Authorization header.')
