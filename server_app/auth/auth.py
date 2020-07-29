from quart import Blueprint, request, jsonify, g
import jwt
import datetime
from .auth_tools import is_username_exist, verify_sing, get_user_with_username, sign
import bcrypt
import config
from data.init_database import db_connection_required
from data.user import User

auth_blueprint = Blueprint(
    "auth",
    __name__,
    url_prefix='/auth'
)


@auth_blueprint.route('/sign_up', methods=['POST'])
@db_connection_required
def sign_up():
    if not config.REGISTER_ENABLED:
        return jsonify({"msg": "Register is not enabled."}), 400
    try:
        qq_id = request.form["qq_id"]  # 要求3字以上好了
        password = request.form["password"]  # 要求8字以上好了
        group_id = request.form['group_id']
    except KeyError:
        return jsonify({"msg": "Missing parameter"}), 400
    if len(password) < 8:
        return jsonify({"msg": "Password is too short"}), 400
    if is_username_exist(qq_id=qq_id, group_id=group_id):
        return jsonify({"msg": "User Exist"}), 400
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    g.db.cursor().execute('UPDATE player_list SET password=%s WHERE qq_id=%s AND group_id=%s',
                          (hashed_password, qq_id, group_id))
    g.db.commit()
    return jsonify({
        "msg": "Success!"
    }), 200


@auth_blueprint.route('/login', methods=['POST'])
def login():
    try:
        username = request.form["qq_id"]
        password: str = request.form["password"]
    except KeyError:
        return jsonify({"msg": "Username or Password is incorrect"}), 403
    if is_username_exist(username) is False:
        return jsonify({"msg": "User does not exist"}), 403
    user: User = get_user_with_username(username)
    if user is None:
        return jsonify({"mag": "Username or Password is incorrect"}), 403
    hash_pwd: str = user.password
    if not bcrypt.checkpw(password.encode(), hash_pwd.encode()):
        return jsonify({"mag": "Username or Password is incorrect"}), 403
    user_id: str = str(user["_id"])
    token = {
        "sub": user_id,
        "iss": config.DOMAIN_NAME,
        "aud": config.FRONTEND_DOMAIN_NAME,
        "iat": int(datetime.datetime.now().timestamp()),
        "remember": True,
        "type": "login_credential",
        "level": "master_password"
    }
    signed = sign(token)
    return jsonify({
        "msg": "successful",
        "jwt": signed
    }), 200


@auth_blueprint.route('/forget_pwd')
def forget_pwd():
    pass
