from nonebot import on_command, CommandSession, permission as perm
import config
import os
import json
import nonebot
import random as r
from nonebot.command.argfilter import extractors, validators
from nonebot import on_natural_language, NLPSession, IntentCommand


@on_command('change_character', aliases=('更换声源', '换声', '修改声源', '选择声源'), only_to_me=False, permission=perm.SUPERUSER)
async def change_character(session: CommandSession):
    group_id = session.event.group_id
    file_name = r'C:\Users\david\PycharmProjects\PCRBot\pcr\plugins\record_send\recording.json'
    # print(os.path.isfile(file_name))
    if not os.path.isfile(file_name):
        print('-')
        default_data = json.dumps({'record': [{'group_id': group_id, 'character': 'Laffey'}]})
        with open(file_name, 'w', encoding='utf8') as f:
            f.write(default_data)
            print('3')
    with open(file_name, 'r') as f:
        data = json.load(f)
        print('2')
    if data:
        flag = False
        for i in data['record']:
            if i['group_id'] == session.event.group_id:
                if 'new_name' not in session.state:
                    prompt = '指挥官，现在有如下声源可以供选择的喵：\n'
                    index = 1
                    for cname in config.RECORD_ORIGIN:
                        prompt += str(index) + '. ' + cname + '\n'
                        index += 1
                    prompt += '当前声源是' + i['character'] + '酱为指挥官服务喵~\n' + '请在30s内做出选择喵！'
                    await session.send(prompt)
                    session.get('new_name', arg_filters=[extractors.extract_text])
                new_name = session.state['new_name']
                is_exist = False
                for i1 in config.RECORD_ORIGIN.items():
                    for j in i1[1]:
                        if new_name in j:
                            new_name = i1[0]
                            is_exist = True
                            break
                flag = True

                if is_exist:
                    i['character'] = new_name
                    with open(file_name, 'w', encoding='utf8') as f:
                        json.dump(data, f)
                    await session.send('修改成功了喵~')

                else:
                    await session.send('修改的名称不存在喵，请重试命令~')
                    return
                break
        if not flag:
            current_data = {'group_id': group_id, 'character': 'Laffey'}
            # data['record'].append(current_data)
            await session.send(f'指挥官，现在有如下声源可以供选择的喵：\n')
            index = 1
            for cname in config.RECORD_ORIGIN:
                await session.send(f'{index}. {cname}\n')
                index += 1
            await session.send('当前声源是' + current_data['character'] + '酱为指挥官服务喵~\n'
                                                                     '请在30s内做出选择喵！')
            new_name = session.get('new_name',arg_filters=[extractors.extract_text])
            print(new_name)
            is_exist = False
            for i2 in config.RECORD_ORIGIN.items():
                for j in i2[1]:
                    if new_name in j:
                        new_name = i2[0]
                        is_exist = True
                        break
            if is_exist:
                current_data['character'] = new_name
                data['record'].append(current_data)
                with open(file_name, 'w', encoding='utf8') as f:
                    json.dump(data, f)
                await session.send('修改成功了喵~')
            else:
                await session.send('修改的名称不存在喵，请重试命令~')
                return
    else:
        await session.send('出故障了喵QAQ，请重试命令')


@on_command('send_record',aliases=('发语音'), only_to_me=False)
async def send_record(session:CommandSession):
    if session.event.group_id in config.PRIMARY_GROUP_ID:
        file = r'C:\Users\david\PycharmProjects\PCRBot\pcr\plugins\record_send\recording.json'
        if not os.path.isfile(file):
            await session.send('请指挥官先执行一遍[选择声源]命令喵~')
            return
        with open(file,'r') as f:
            data = json.load(f)
        if data:
            for record in data['record']:
                if record['group_id'] == session.event.group_id:
                    dir_name = record['character']+'_voice'
                    bot = nonebot.get_bot()
                    try:
                        rls = os.listdir(f'C:\\Users\\david\\Documents\\酷Q_Pro\\data\\record\\{dir_name}')
                    except:
                        await session.send('指挥官要找的语音资源暂时不存在的喵~请尝试使用[更换声源]命令进行操作喵')
                    record_file = os.path.join(f'\{dir_name}',
                                               rls[r.randint(0, len(rls) - 1)])

                    await bot.send_group_msg(group_id=session.event.group_id,
                                       message=f'[CQ:record,file={record_file}]')


@on_natural_language(keywords={'语音'})
async def _(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(95.0, 'send_record')