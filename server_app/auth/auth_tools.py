from quart import request, jsonify, g
from functools import wraps
import jwt
from data.init_database import db_connection_required
from data.user import User
from typing import Optional
import config


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
            return jsonify({"msg": "Auth sign does not verify"}), 400
        user: dict = get_user_with_uid(decode_jwt.get("sub"))
        if user is None:
            return jsonify({"msg": "Can not find user data"}), 403
        if decode_jwt["iat"] < user["valid_since"].timestamp():  # 若是這個jwt已被撤銷
            return jsonify({"msg": "This session has been revoked"}), 403
        g.user = user
        return f(*args, **kwargs)

    return decorated_function


@db_connection_required
def current_user_is_admin():
    return 'admin' in g.user['group']


@db_connection_required
def get_user_with_uid(uid: str) -> dict:
    return g.db.users.find_one({"_id": ObjectId(uid)})


def sign(json_: dict) -> str:
    return jwt.encode(json_, current_app.secret_key, algorithm='HS256').decode()


def verify_sing(signed: str) -> dict:
    print(signed)
    return jwt.decode(signed, current_app.secret_key, algorithms=['HS256'])


@db_connection_required
def is_username_exist(qq_id: str, group_id: str) -> bool:
    result: int = g.db.cursor().execute('SELECT * FROM player_list '
                                        'WHERE group_id=%s AND qq_id=%s', (group_id, qq_id))
    return result != 0


@db_connection_required
def get_user_with_username(qq_id: str, group_id: int) -> Optional[User]:
    cursor = g.db.cursor()
    cursor.execute('SELECT (group_id, qq_id, qq_name, role, password, player_name, id) FROM '
                   'player_list WHERE qq_id=%s AND group_id=%s', (qq_id, group_id))
    record = cursor.fetchone()
    if record is None:
        return None
    else:
        return User(record)
