import config
import hmac
import hashlib
import config
import requests


def password_for(qq: int):
    return hmac.new(config.SECRET_KEY.encode(), str(qq).encode(), digestmod=hashlib.sha256).hexdigest()


def get_auth_header(for_qq: int):
    password = password_for(for_qq)
    payload = dict(username='temp_qq_' + str(for_qq), password=password)
    login_url = config.BACKEND_URL + '/v1/auth/login'
    jwt = requests.post(url=login_url, json=payload).json()['jwt']
    return dict(auth=jwt)


def link_account_with(qq: int, account: str):
    header = get_auth_header(for_qq=qq)
    url = config.BACKEND_URL + '/v1/account/link_account'
    json = dict(username=account)
    r = requests.post(url=url, header=header, json=json)
    print(r.text)


if __name__ == '__main__':
    print(password_for(12123123))