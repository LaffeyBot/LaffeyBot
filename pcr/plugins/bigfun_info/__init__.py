from nonebot import CommandSession, on_command
from nonebot import on_natural_language, NLPSession, IntentCommand
from jieba import posseg
import re
from .team_homework_spider import TeamHomework
from data import init_database

from pcr.plugins.priconne.chara import Chara, gen_team_pic

from hoshino.util import pic2b64


from nonebot.command.argfilter import extractors
from nonebot import MessageSegment
import nonebot

NICKNAME = {'拉菲', '拉菲酱', 'Laffey', 'laffey'}


@on_command('team_homework', aliases=('会战作业', '公会战作业', '工会战作业'), only_to_me=False)
async def team_homework(session: CommandSession):
    target_boss = session.get('target_boss', prompt='请指挥官给出目标boss')
    print(target_boss)
    print(type(target_boss))
    try:
        boss_position = int(target_boss)
    except:
        boss_position = int(re.search(r'([1-5]+)王', target_boss).group(1))
    if boss_position > 5 or boss_position < 1:
        await session.send('请给出boss的位置信息，最多是5', at_sender=True)
        return
    homework_ids = await get_message(boss_position, session)
    c = init_database.get_connection()
    cursor = c.cursor()
    for hid in homework_ids:
        result = cursor.execute(f'select homework_id from team_homework where homework_id={hid}')
        if not result:
            try:
                print(1)
                cursor.execute(
                    f'insert into team_homework (homework_id,id) values ({hid},DEFAULT )'
                )
                print(f'insert into team_homework (homework_id,id) values ({hid},DEFAULT )')
                c.commit()
            except Exception as e:
                print(e)
                c.rollback()
    c.close()


@on_command('get_details', aliases=('查询作业详情', '查询轴', '查看细节', '作业详情', '查看作业详情'), only_to_me=False)
async def get_details(session: CommandSession):
    hid = session.get('hid', prompt='请给出要查看详情的作业id喵~')
    try:
        hid = int(hid)
    except:
        await session.send('作业的id都是数字喵QAQ')
    c = init_database.get_connection()
    cursor = c.cursor()
    result = cursor.execute(
        f'select homework_id from team_homework where homework_id={hid}'
    )
    if result:
        t = TeamHomework()
        data = t.get_details(hid)
        work = data['data']['work']
        video_url = data['data']['video_src']
        remark = data['data']['remark']
        if work or video_url:
            if work:
                if remark:
                    await session.send(work + '\n' + '==========\n' + '温馨提示：' + remark)
                else:
                    await session.send(work)
            if video_url:
                await session.send('参考操作视频地址' + video_url)
        else:
            await session.send('这个作业暂时没有给出任何有价值的详情信息，有可能是烟雾弹，请指挥官谨慎选择喵~')

    else:
        await session.send('指挥官要查询的作业走丢了喵qaq')


async def get_message(boss_position, session: CommandSession):
    params = {
        'target': 'get-gzlj-team-war-work-list/a',
        'type': 2,
        'battle_id': 3,
        'boss_position': boss_position,
        'order': 1,
        'page': 1
    }
    t = TeamHomework('https://www.bigfun.cn/api/feweb', params=params)
    data_dict = t.parse()
    homework_list = data_dict['data']
    message = f'以下是拉菲为指挥官查到的{boss_position}王的作业，请选择合适的使用:\n'
    count = 0
    homework_ids = []
    for homework in homework_list:
        if count <= 5:
            message += '==========\n'
            message += '【作业编号{0}】 {1}\n'.format(homework['id'], homework['title'])
            message += '该轴预期的伤害为{0} 适用{1}周目 收到的点赞数{2}\n'.format(homework['expect_injury'], homework['boss_cycle'],
                                                                homework['like_count'])
            team_pic = draw_pic(homework['role_list'])
            atk_team = str(MessageSegment.image(team_pic))
            message += atk_team
            message += '\n'
            message += '作者为：{}\n'.format(homework['user']['player_name'])
            homework_ids.append(homework['id'])
            count += 1
    message += '指挥官可以通过【查询作业详情】+作业编号查看具体信息'
    await session.send(message, at_sender=True)
    return homework_ids


def draw_pic(team):
    # 1.star是角色星级数，weapon是是否有专武(0无，1有）
    chars = list()
    for image in team:
        chara = Chara(int(image['id']), image['stars'], image['weapons'], url=image['avatar'], is_bigfun=True)
        chars.append(chara)
    team_pic = gen_team_pic(team)
    team_pic_b64 = pic2b64(team_pic)
    return team_pic_b64


@team_homework.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['target_boss'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('格式：【会战作业 xxx】')

    session.state[session.current_key] = stripped_arg


@get_details.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['hid'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('格式：【作业详情 xxx】')

    session.state[session.current_key] = stripped_arg


@on_natural_language(keywords={'会战作业'}, only_to_me=False)
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg = session.msg_text.strip()
    # 对消息进行分词和词性标注
    words = posseg.lcut(stripped_msg)

    target_boss = None
    # 遍历 posseg.lcut 返回的列表
    for word in words:
        # 每个元素是一个 pair 对象，包含 word 和 flag 两个属性，分别表示词和词性
        if word.flag == 'm':
            # ns 词性表示地名
            target_boss = word.word

    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'team_homework', current_arg=target_boss or '')
