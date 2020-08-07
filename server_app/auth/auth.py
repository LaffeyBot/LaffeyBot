from quart import Blueprint, request, jsonify, g
import jwt
import datetime
from .auth_tools import is_username_exist, get_user_with, sign
import bcrypt
import config
from data.model import *

auth_blueprint = Blueprint(
    "auth_v1",
    __name__,
    url_prefix='/v1/auth'
)


@auth_blueprint.route('/sign_up', methods=['POST'])
def sign_up():
    if not config.REGISTER_ENABLED:
        return jsonify({"msg": "Register is not enabled."}), 400
    try:
        username = request.form["username"]  # 要求3字以上
        password = request.form["password"]  # 要求8字以上
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        nickname = request.form.get('nickname', username)
    except KeyError:
        return jsonify({"msg": "Missing parameter", "code": 101}), 400
    if len(username) < 3 or len(password) < 8:
        return jsonify({"msg": "Username or password is too short",
                        "code": 102}), 400
    if is_username_exist(username):
        return jsonify({"msg": "User Exists", "code": 103}), 403
    new_user: Users = Users(group_id=-1,
                            username=username,
                            password=bcrypt.hashpw(password, bcrypt.gensalt()),
                            nickname=nickname,
                            created_at=datetime.datetime.now(),
                            role=0,
                            email=email,
                            email_verified=False,
                            phone=phone,
                            phone_verified=False,
                            valid_since=datetime.datetime.now()
                            )
    db.session.add(new_user)
    return jsonify({
        "msg": "Successful!",
        "id": str(new_user.id),
    }), 200


@auth_blueprint.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username', None)
        email = request.form.get('email', None)
        phone = request.form.get('phone', None)
        password: str = request.form["password"]
    except KeyError:
        return jsonify({"mag": "Username or Password is missing", "code": 201}), 403
    user: Users = get_user_with(username=username)
    if user is None:
        user = get_user_with(email=email)
    if user is None:
        user = get_user_with(phone=phone)
    if user is None:
        return jsonify({"mag": "User does not exist", "code": 202}), 403
    hash_pwd: str = user.password
    if not bcrypt.checkpw(password.encode(), hash_pwd.encode()):
        return jsonify({"msg": "Username or Password is incorrect", "code": 203}), 403
    user_id: int = user.id
    token = {
        "sub": user_id,
        "iss": config.DOMAIN_NAME,
        "aud": config.FRONTEND_DOMAIN_NAME,
        "iat": int(datetime.datetime.now().timestamp()),
        "remember": True,
        "type": "login_credential"
    }
    signed = sign(token)
    return jsonify({
        "msg": "successful",
        "jwt": signed
    }), 200


@auth_blueprint.route('/forget_pwd')
def forget_pwd():
    pass
