import nonebot
from quart import request, jsonify, g
from server_app.auth_tools import login_required
from data.model import *
import json

bot = nonebot.get_bot()  # 在此之前必须已经 init


class Message:

    def __init__(self, message: str, id: int, type: str) -> None:
        self.type_ = type
        self.message = message
        self.id_ = id


@bot.server_app.route('/send_message', methods=['POST'])
@login_required
async def send_message():
    data = await request.get_data()
    data = data.decode("UTF-8")
    json_dict: dict = json.loads(data)
    message = json_dict.get('message')
    id_ = json_dict.get('id')
    type_ = json_dict.get('type')

    if not (message or id_ or type_):
        return jsonify({'msg': 'Missing parameters'})

    user: User = g.user
    group: Group = user.group
    if type_ == 'group':
        if group.group_chat_id != group.group_chat_id:
            return jsonify({'msg': 'You can only send message to your group.'}), 403
        await nonebot.get_bot().send_group_msg(group_id=int(id_), message=message)
    elif type_ == 'private':
        if not group.users.filter_by(qq=int(id_)).first():
            return jsonify({'msg': 'You can only send message to your group members.'}), 403
        await nonebot.get_bot().send_private_msg(user_id=int(id_), message=message)
    return ''
