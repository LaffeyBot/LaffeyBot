import re
import time
from collections import defaultdict

import hoshino
from hoshino import Service
from hoshino.typing import *
from hoshino.util import FreqLimiter, concat_pic, pic2b64

from .. import chara

sv_help = '''
[怎么拆] 接防守队角色名 查询竞技场解法喵
[点赞] 接作业id 评价解法喵
[点踩] 接作业id 评价解法喵
'''.strip()
sv = Service('pcr-arena', help_=sv_help, bundle='pcr查询', use_priv=True)

from . import arena

lmt = FreqLimiter(5)

aliases = ('怎么拆', '怎么解', '怎么打', '如何拆', '如何解', '如何打', '怎麼拆', '怎麼解', '怎麼打', 'jjc查询', 'jjc查詢')
aliases_b = tuple('b' + a for a in aliases) + tuple('B' + a for a in aliases)
aliases_tw = tuple('台' + a for a in aliases)
aliases_jp = tuple('日' + a for a in aliases)


@sv.on_prefix(aliases)
async def arena_query(bot, ev):
    await _arena_query(bot, ev, region=1)


@sv.on_prefix(aliases_b)
async def arena_query_b(bot, ev):
    await _arena_query(bot, ev, region=2)


@sv.on_prefix(aliases_tw)
async def arena_query_tw(bot, ev):
    await _arena_query(bot, ev, region=3)


@sv.on_prefix(aliases_jp)
async def arena_query_jp(bot, ev):
    await _arena_query(bot, ev, region=4)


async def _arena_query(bot, ev: CQEvent, region: int):
    arena.refresh_quick_key_dic()
    uid = ev.user_id

    if not lmt.check(uid):
        await bot.finish(ev, '查询过于频繁了，休息一下吧喵！', at_sender=True)
    lmt.start_cd(uid)

    # 处理输入数据
    defen = ev.message.extract_plain_text()
    defen = re.sub(r'[?？，,_]', '', defen)
    defen, unknown = chara.roster.parse_team(defen)

    if unknown:
        _, name, score = chara.guess_id(unknown)
        if score < 70 and not defen:
            return  # 忽略无关对话
        msg = f'无法识别"{unknown}"' if score < 70 else f'无法识别"{unknown}" {score}%是不是{name}呢喵？'
        await bot.finish(ev, msg)
    if not defen:
        await bot.finish(ev, '格式"怎么拆[空格]防守队伍"', at_sender=True)
    if len(defen) > 5:
        await bot.finish(ev, '队伍不能多于5名角色喵', at_sender=True)
    if len(defen) != len(set(defen)):
        await bot.finish(ev, '队伍中有重复角色喵', at_sender=True)
    if any(chara.is_npc(i) for i in defen):
        await bot.finish(ev, '队伍中有未实装角色喵', at_sender=True)
    # if 1004 in defen:
    #     await bot.send(ev, '\n⚠️您正在查询普通版炸弹人\n※万圣版可用万圣炸弹人/瓜炸等别称', at_sender=True)

    # 执行查询
    sv.logger.info('Doing query...')
    res = await arena.do_query(defen, uid, region)
    sv.logger.info('Got response!')

    # 处理查询结果
    if res is None:
        await bot.finish(ev, '查询失败了喵...', at_sender=True)
    if not len(res):
        await bot.finish(ev, '没有查询到解法喵...', at_sender=True)
    res = res[:min(6, len(res))]  # 限制显示数量，截断结果

    # 发送回复
    if hoshino.config.USE_CQPRO:
        sv.logger.info('Arena generating picture...')
        atk_team = [chara.gen_team_pic(entry['atk']) for entry in res]
        atk_team = concat_pic(atk_team)
        atk_team = pic2b64(atk_team)
        atk_team = str(MessageSegment.image(atk_team))
        sv.logger.info('Arena picture ready!')
    else:
        atk_team = '\n'.join(map(lambda entry: ' '.join(
            map(lambda x: f"{x.name}{x.star if x.star else ''}{'专' if x.equip else ''}", entry['atk'])), res))

    details = [" ".join([
        f"赞{e['up']}+{e['my_up']}" if e['my_up'] else f"赞{e['up']}",
        f"踩{e['down']}+{e['my_down']}" if e['my_down'] else f"踩{e['down']}",
        e['qkey'],
        "你赞过" if e['user_like'] > 0 else "你踩过" if e['user_like'] < 0 else ""
    ]) for e in res]

    defen = [chara.fromid(x).name for x in defen]
    defen = f"防守方【{' '.join(defen)}】"
    at = str(MessageSegment.at(ev.user_id))

    msg = [
        defen,
        f'已为指挥官{at}查询到以下进攻方案喵：',
        str(atk_team),
        f'作业评价：',
        *details,
        '※发送"点赞/点踩"可进行评价'
    ]
    if region == 1:
        msg.append('※使用"b怎么拆"或"台怎么拆"可按服过滤喵')
    msg.append('Support by pcrdfans_com')

    sv.logger.debug('Arena sending result...')
    await bot.send(ev, '\n'.join(msg))
    sv.logger.debug('Arena result sent!')


@sv.on_prefix('点赞')
async def arena_like(bot, ev):
    await _arena_feedback(bot, ev, 1)


@sv.on_prefix('点踩')
async def arena_dislike(bot, ev):
    await _arena_feedback(bot, ev, -1)


rex_qkey = re.compile(r'^[0-9a-zA-Z]{5}$')


async def _arena_feedback(bot, ev: CQEvent, action: int):
    action_tip = '赞' if action > 0 else '踩'
    qkey = ev.message.extract_plain_text().strip()
    if not qkey:
        await bot.finish(ev, f'发送"点{action_tip}+作业id"，如"点{action_tip}ABCDE"', at_sender=True)
    if not rex_qkey.match(qkey):
        await bot.finish(ev, f'找不到{action_tip}这个作业喵...', at_sender=True)
    try:
        await arena.do_like(qkey, ev.user_id, action)
    except KeyError:
        await bot.finish(ev, '无法找到作业喵...', at_sender=True)
    await bot.send(ev, '感谢反馈喵~', at_sender=True)
