import config
import hmac
import hashlib


def password_for(qq: int):
    return hmac.new(config.SECRET_KEY.encode(), str(qq).encode(), digestmod=hashlib.sha256).hexdigest()


if __name__ == '__main__':
    print(password_for(12123123))