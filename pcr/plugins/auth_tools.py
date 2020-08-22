import config
import hmac
import hashlib
import config
from data.model import *
from nonebot import get_bot
import datetime
import config
import jwt


def password_for(qq: int):
    return hmac.new(config.SECRET_KEY.encode(), str(qq).encode(), digestmod=hashlib.sha256).hexdigest()


def get_auth_header(for_qq: int):
    db.init_app(get_bot().server_app)
    user: User = User.query.filter_by(qq=for_qq).first()
    token = {
        "sub": user.id,
        "iss": config.FRONTEND_DOMAIN_NAME,
        "aud": config.DOMAIN_NAME,
        "iat": int(datetime.datetime.now().timestamp()),
        "remember": True,
        "type": "login_credential"
    }
    signed = sign(token)

    return dict(auth=signed)


def sign(json_: dict) -> str:
    return jwt.encode(json_, config.SECRET_KEY, algorithm='HS256').decode()


if __name__ == '__main__':
    print(password_for(12123123))