from quart import request, jsonify, g
from functools import wraps
import jwt
import config
from data.model import *
from typing import Optional
import base64
import time
from nonebot import get_bot


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('auth')
        try:
            decode_jwt = jwt.decode(auth_header,
                                    config.SECRET_KEY,
                                    algorithms=['HS256'],
                                    audience=config.DOMAIN_NAME)
        except jwt.exceptions.InvalidTokenError:
            return jsonify({"msg": "Auth sign does not verify"}), 401
        db.init_app(get_bot().server_app)
        user: User = get_user_with(id_=decode_jwt.get("sub"))
        if user is None:
            return jsonify({"msg": "Can not find user data"}), 401
        if decode_jwt["iat"] < time.mktime(user.valid_since.timetuple()):
            return jsonify({"msg": "This session has been revoked"}), 401
        g.user = user
        return f(*args, **kwargs)

    return decorated_function


def current_user_is_admin() -> bool:
    user: User = g.user
    if user is None:
        return False
    return user.role >= 1


def current_user_is_owner() -> bool:
    user: User = g.user
    if user is None:
        return False
    return user.role >= 2


def get_user_with(username: str = None, email: str = None,
                  phone: str = None, id_: int = None) -> Optional[User]:
    if username is not None:
        return User.query.filter_by(username=username).first()
    elif email is not None:
        return User.query.filter_by(email=email).first()
    elif phone is not None:
        return User.query.filter_by(phone=phone).first()
    elif id_ is not None:
        return User.query.filter_by(id=id_).first()
    else:
        return None


def get_user_with_any(identifier: str) -> Optional[User]:
    user = User.query.filter_by(username=identifier).first()
    if user is None:
        user = User.query.filter_by(email=identifier).first()
    if user is None:
        user = User.query.filter_by(phone=identifier).first()
    return user


def sign(json_: dict) -> str:
    return jwt.encode(json_, config.SECRET_KEY, algorithm='HS256').decode()


def verify_sing(signed: str) -> dict:
    print(signed)
    return jwt.decode(signed, config.SECRET_KEY, algorithms=['HS256'])


def is_username_exist(username: str) -> bool:
    return get_user_with(username=username) is not None


def is_email_exist(email: str) -> bool:
    return get_user_with(email=email) is not None


def generate_user_dict(user: User, for_oneself: bool) -> dict:
    user_data = {
        "username": user.username,
        "id": user.id,
        "nickname": user.nickname,
        "role": user.role,
        "email": user.email
    }
    if user.group_id:
        user_data["group_id"] = user.group_id
    if user.qq:
        user_data["qq"] = user.qq
    return user_data
