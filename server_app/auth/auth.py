from quart import Blueprint, request, jsonify, g
import jwt
import datetime
from server_app.auth_tools import is_username_exist, get_user_with, sign
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
    """
    @api {post} /v1/auth/sign_up 注册
    @apiVersion 1.0.0
    @apiName sign_up
    @apiGroup Users
    @apiParam {String}  username   (必须)    用户名（3字以上）
    @apiParam {String}  password   (必须)    密码（8字以上）
    @apiParam {String}  email      (可选)    邮箱
    @apiParam {String}  phone      (可选)    手机号
    @apiParamExample {json} Request-Example:
        {
            username: "someuser",
            password: "12345678",
            email: "a@ddavid.net",
            phone: "13312341234"
        }

    @apiSuccess (回参) {String} msg  为"Successful!"
    @apiSuccess (回参) {String} id   用户id
    @apiSuccessExample {json} 成功样例
        HTTP/1.1 200 OK
        {
            "msg": "Successful!",
            "id": 12345
        }

    @apiErrorExample {json} 用户名或密码过短
        HTTP/1.1 400 Bad Request
        {
            "msg": "Username or password is too short",
            "code": 102
        }

    @apiErrorExample {json} 用户名已存在
        HTTP/1.1 403 Forbidden
        {"msg": "User Exists", "code": 103}

    """
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
        "id": new_user.id,
    }), 200


@auth_blueprint.route('/login', methods=['POST'])
def login():
    """
    @api {post} /v1/auth/login 登录
    @apiVersion 1.0.0
    @apiName login
    @apiGroup Users
    @apiParam {String}  username   (可选)    用户名
    @apiParam {String}  email      (可选)    邮箱
    @apiParam {String}  phone      (可选)    手机号
    @apiParam {String}  password   (必须)    密码
    @apiParamExample {json} Request-Example:
        {
            username: "someuser",
            password: "12345678"
        }

    @apiSuccess (回参) {String} msg  为"Successful!"
    @apiSuccess (回参) {String} jwt  jwt token，应当放入auth header
    @apiSuccessExample {json} 成功样例
        { "msg": "Successful!",
         "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
         }

    @apiErrorExample {json} 未提供用户名或密码
        HTTP/1.1 403 Forbidden
        {"msg": "Username or Password is missing", "code": 201}

    @apiErrorExample {json} 用户不存在
        HTTP/1.1 403 Forbidden
        {"msg": "User does not exist", "code": 202}

    @apiErrorExample {json} 密码或用户名错误
        HTTP/1.1 403 Forbidden
        {"msg": "Username or Password is incorrect", "code": 203}

    """
    try:
        username = request.form.get('username', None)
        email = request.form.get('email', None)
        phone = request.form.get('phone', None)
        password: str = request.form["password"]
    except KeyError:
        return jsonify({"msg": "Username or Password is missing", "code": 201}), 403
    user: Users = get_user_with(username=username)
    if user is None:
        user = get_user_with(email=email)
    if user is None:
        user = get_user_with(phone=phone)
    if user is None:
        return jsonify({"msg": "User does not exist", "code": 202}), 403
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
