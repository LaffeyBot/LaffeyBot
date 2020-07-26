import nonebot
from quart import request, jsonify
from data.json.json_editor import JSONEditor
from data.damage import add_record

bot = nonebot.get_bot()  # 在此之前必须已经 init


@bot.server_app.route('/fetch_status', methods=['GET'])
async def fetch_status():
    group_id = request.args.get('group_id', None)

    if not group_id:
        return jsonify({'error': 'Missing parameters. Required parameters: '
                                 'group_id'})
    return str(JSONEditor(group_id).get_fetch_status())
