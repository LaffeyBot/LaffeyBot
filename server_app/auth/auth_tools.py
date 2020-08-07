from quart import request, current_app, jsonify, g
from functools import wraps
import jwt
from data.init_database import db_connection_required
import config
from data.model import *
from typing import Optional


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('auth')
        try:
            decode_jwt = jwt.decode(auth_header,
                                    current_app.secret_key,
                                    algorithms=['HS256'],
                                    audience=config.DOMAIN_NAME)
        except jwt.exceptions.InvalidTokenError:
            return jsonify({"msg": "Auth sign does not verify", "code": 301}), 400
        user: Users = get_user_with(id_=decode_jwt.get("sub"))
        if user is None:
            return jsonify({"msg": "Can not find user data"}), 403
        if decode_jwt["iat"] < user.valid_since.timestamp():
            return jsonify({"msg": "This session has been revoked", "code": 302}), 403
        g.user = user
        return f(*args, **kwargs)

    return decorated_function


def current_user_is_admin() -> bool:
    user: Users = g.user
    if user is None:
        return False
    return user.role >= 1


def current_user_is_owner() -> bool:
    user: Users = g.user
    if user is None:
        return False
    return user.role >= 2


def get_user_with(username: str = None, email: str = None,
                  phone: str = None, id_: int = None) -> Optional[Users]:
    if username is not None:
        return Users.query.filter_by(username=username).first
    elif email is not None:
        return Users.query.filter_by(email=email).first
    elif phone is not None:
        return Users.query.filter_by(phone=phone).first
    elif id_ is not None:
        return Users.query.filter_by(id=id_).first
    else:
        return None


def sign(json_: dict) -> str:
    return jwt.encode(json_, config.SECRET_KEY, algorithm='HS256').decode()


def verify_sing(signed: str) -> dict:
    print(signed)
    return jwt.decode(signed, config.SECRET_KEY, algorithms=['HS256'])


def is_username_exist(username: str) -> bool:
    return get_user_with(username=username) is not None
