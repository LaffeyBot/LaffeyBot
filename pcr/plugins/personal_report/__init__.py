from nonebot import on_command,CommandSession
from data.init_database import get_connection
import datetime


@on_command('show_rank',aliases=('个人排名',),only_to_me=False)
async def show_rank(session:CommandSession):
    print(session.event)
    group_id = session.event.group_id
    if session.event.message['card']:
        sender = session.event.message['card']
    else:
        sender = session.event.message['nickname']

    month = '%02d' % datetime.datetime.now().month
    day = '%02d' % datetime.datetime.now().day
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    pro_year = tomorrow.year
    pro_month = '%02d' % tomorrow.month
    pro_day = '%02d' % tomorrow.day
    begin_date = f'{datetime.datetime.now().year}-{month}-{day} 05:00:00'
    end_date = f'{pro_year}-{pro_month}-{pro_day} 05:00:00'
    date = datetime.datetime.today().strftime('%Y_%m_%d')
    c= get_connection()
    cursor = c.cursor()
    cursor.execute('select nickname, sdamage,last_modified from  (select nickname,sum(damage) as sdamage,last_modified from personal_record where group_id in (select id from `group` where group_chat_id=%s) and (last_modified>=%s and last_modified<=%s) group by nickname) as `pr*` order by sdamage desc;',
                   (group_id,begin_date, end_date))
    result = cursor.fetchall()
    name = []
    sdamage= []
    if result:
        for row in result:
            name.append(row[0])
            sdamage.append(row[1])
        try:
            rank = name.index(sender)
            await session.send(f'{sender}指挥官今天队内伤害排名是第{rank}',at_sender=True)
        except Exception as e:
            await session.send(f'{sender}指挥官的今天排名暂时查不到喵，请查看当前是否存在指挥官的记录：\n')
            for i,n in enumerate(name):
                message = '========\n'
                message+=f'{i+1}. {n}指挥官累计伤害是{sdamage[i]}\n'
            await session.send(message)






