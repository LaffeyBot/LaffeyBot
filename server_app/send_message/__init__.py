import nonebot
from quart import request, jsonify, g
from server_app.auth_tools import login_required
from data.model import *

bot = nonebot.get_bot()  # 在此之前必须已经 init


@bot.server_app.route('/send_message', methods=['POST'])
@login_required
async def send_message():
    json = request.get_json(force=True)
    message = json.get('message', None)
    id_ = json.get('id', None)
    type_ = json.get('type', None)

    if not (message or id_ or type_):
        return jsonify({'Missing parameters'})

    user: User = g.user
    group: Group = user.group
    if type_ == 'group':
        if group.group_chat_id != user.group_id:
            return jsonify({'You can only send message to your group.'}), 403
        await nonebot.get_bot().send_group_msg(group_id=int(id_), message=message)
    elif type_ == 'private':
        if not group.users.filter_by(qq=int(id_)).first():
            return jsonify({'You can only send message to your group members.'}), 403
        await nonebot.get_bot().send_private_msg(user_id=int(id_), message=message)