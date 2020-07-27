import nonebot
from quart import request, jsonify
from server_app.validate_api_key import validate_api_key
from data.damage import add_record
from pcr.plugins.manage_record.alert_new_record import alert_new_record

bot = nonebot.get_bot()  # 在此之前必须已经 init


@bot.server_app.route('/add_attack_record', methods=['GET'])
async def add_attack_record():
    api_key = request.args.get('api_key', None)
    group_id = request.args.get('group_id', None)
    damage = request.args.get('damage', None)
    username = request.args.get('username', None)
    target = request.args.get('target', '')
    force = False

    if not group_id or not api_key or not damage or not username:
        return jsonify({'error': 'Missing parameters. Required parameters: '
                                 'api_key, group_id, damage, username'})

    if not validate_api_key(api_key, group_id):
        return jsonify({'error': 'Your API key is not valid.'})

    new_record = [[username, target, int(damage)]]
    added_record, did_kill = add_record(new_record, group_id, force=force)
    await alert_new_record(added_record, did_kill, group_id=group_id)
    return 'Success!'
