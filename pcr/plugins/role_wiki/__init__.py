import nonebot
from aiocqhttp.event import Event
from .wiki_data_capture import Wiki
import re
import os, json
import config
import csv
from nonebot import CommandSession
from pcr.plugins.priconne._pcr_data import CHARA_NAME
from hoshino import  util

bot = nonebot.get_bot()


@bot.on_message()
async def send_gif(cq_event: Event):
    # 获取信息
    group_id = cq_event.group_id
    message = cq_event.message
    rex = re.match('(.*?).gif', str(message))

    if rex:
        role_name = util.normalize_str(rex.group(1))
        # 查找是否是对应的别名
        filtered = filter(lambda char_list: role_name in char_list,
                          list(CHARA_NAME.values()))
        result = next(filtered, None)
        if result:
            role_name = result[0].replace('(', '（').replace(')', '）')
        else:
            return

        if os.path.exists('pcr/plugins/role_wiki/roles.json'):
            with open('pcr/plugins/role_wiki/roles.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            names = data['role_name']
            if role_name in names:
                fold_path = os.path.join(config.CQ_SOURCE_PATH, 'images', f'{role_name}动画')
                if os.path.exists(fold_path):
                    for root,dirs,files in os.walk(fold_path):
                        for file_name in files:
                            # msg = f'{file_name}如下：\n'
                            msg = f'[CQ:image,file={role_name}动画/{file_name}]'
                            await bot.send_msg(group_id=group_id,message=msg,auto_escape=False)

        else:
            await bot.send_msg(group_id=group_id, message='初始化记录中，请稍后再试')
            w = Wiki()
            w.get_role_gifs()
            await bot.send_msg(group_id=group_id,message='初始化完成>_<')
    else:
        return


@bot.on_message()
async def send_gif(cq_event: Event):
    # 获取信息
    group_id = cq_event.group_id
    message = cq_event.message
    print(message)
    print(str(message))
    rex = re.match('(.*?)技能', str(message))
    if rex:
        role_name = rex.group(1)
        with open(r'pcr/plugins/role_wiki/nickname.csv', 'r', encoding='utf-8') as f:
            f_csv = csv.reader(f)
            is_find = False
            for row in f_csv:
                if role_name in row:
                    role_name = row[2]
                    is_find = True
                    break
            print(is_find)
            if not is_find:
                return
        w = Wiki()
        results = w.get_role_skills(role_name)
        msg = ''
        for skill in results:
            msg += '==========\n'
            msg += skill['title']+skill['sub_title']
            msg += '[CQ:image,file={}]'.format(skill['image_url'])
            msg += skill['skill']
        await bot.send_msg(group_id=group_id, message=msg)


def name_does_match(chara_name_list: list, name: str):
    return name in chara_name_list


if __name__ == '__main__':
    with open('./nickname.csv', 'r', encoding='utf-8') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            print(row)
    for i in os.walk(r'E:\pcrbot\pcr\plugins\role_wiki'):
        print(i)


