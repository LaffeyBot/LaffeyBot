from data.init_database import get_connection
import requests
import config
from data.model import *
from nonebot import get_bot
from pcr.plugins.auth_tools import get_auth_header


def add_record(qq: int, type_: str, damage: int = None):
    url = config.BACKEND_URL + '/v1/record/add_record'
    db.init_app(get_bot().server_app)
    headers = get_auth_header(qq)

    json = dict(type=type_, origin='QQ')
    if damage:
        json['damage'] = damage
    r = requests.post(url, json=json, headers=headers)
    print(r.text)
    return r.json()


# noinspection SqlWithoutWhere
def delete_all_records(group_id: int):
    c = get_connection()
    c.execute('DELETE FROM record WHERE group_id=%s', (group_id,))
    c.commit()
