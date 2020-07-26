import nonebot
from quart import request, jsonify
from server_app.validate_api_key import validate_api_key
from data.init_database import get_connection
import datetime
from data.get_date_int import get_date_int

bot = nonebot.get_bot()  # 在此之前必须已经 init


@bot.server_app.route('/add_rank', methods=['GET'])
async def add_rank():
    api_key = request.args.get('api_key', None)
    group_id = request.args.get('group_id', None)
    rank = request.args.get('rank', None)

    if not group_id or not api_key or not rank:
        return jsonify({'error': 'Missing parameters. Required parameters: '
                                 'api_key, group_id, rank'})

    if not validate_api_key(api_key, group_id):
        return jsonify({'error': 'Your API key is not valid.'})

    c = get_connection()
    cursor = c.cursor()
    cursor.execute('SELECT date, rank FROM rank_record '
                   'ORDER BY date DESC LIMIT 1')
    previous_rank = cursor.fetchone()
    if previous_rank is not None \
            and (previous_rank[1] - 50) / rank > 5 or (previous_rank[1] + 50) / rank < 0.2:
        # This data is not right
        return

    date = datetime.datetime.now()
    date_int: int = get_date_int(date, with_hour=True)

    cursor.execute('DELETE FROM rank_record WHERE group_id=%s AND date=%s',
                   (group_id, date))
    cursor.execute('INSERT INTO rank_record (date, rank)'
                   'VALUES (%s, %s)', (date_int, rank))
    c.commit()
    return 'Success!'
