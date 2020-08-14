from nonebot import on_command, CommandSession, permission as perm
import config
import os
import json
import nonebot
import random as r
from nonebot.command.argfilter import extractors, validators
from nonebot import on_natural_language, NLPSession, IntentCommand
from hoshino.util import load_image_as_cqimage


@on_command('change_character', aliases=('更换声源', '换声', '修改声源', '选择声源'), only_to_me=False)
async def change_character(session: CommandSession):
    group_id = session.event.group_id
    file_name = os.path.join(os.path.dirname(__file__), 'recording.json').replace('\\', '/')
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
            if 'new_name' not in session.state:
                message = '指挥官，现在有如下声源可以供选择的喵：\n'
                index = 1
                for cname in config.RECORD_ORIGIN:
                    message += f'{index}. {cname}\n'
                    index += 1
                message += '当前声源是' + current_data['character'] + '酱为指挥官服务喵~\n' + '请在30s内做出选择喵！'
                await session.send(message)
                session.get('new_name', arg_filters=[extractors.extract_text])
            new_name = session.state['new_name']
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


@on_command('send_record', aliases=('发语音'), only_to_me=False)
async def send_record(session: CommandSession):
    print('1')
    file = os.path.join(os.path.dirname(__file__), 'recording.json').replace('\\', '/')
    if not os.path.isfile(file):
        await session.send('请指挥官先执行一遍[选择声源]命令喵~')
        return
    with open(file, 'r') as f:
        data = json.load(f)
    print('2')
    print(data)
    if data:
        is_find_group = False
        for record in data['record']:

            if record['group_id'] == session.event.group_id:
                is_find_group = True
                dir_name = record['character'] + '_voice'
                bot = nonebot.get_bot()
                try:
                    rls = os.listdir(os.path.join(config.CQ_SOURCE_PATH, 'record', dir_name))
                except:
                    await session.send('指挥官要找的语音资源暂时不存在的喵~请尝试使用[更换声源]命令进行操作喵')
                record_file = os.path.join(f'\{dir_name}',
                                           rls[r.randint(0, len(rls) - 1)])
                print(session.event.group_id)

                await bot.send_group_msg(group_id=session.event.group_id,
                                         message=f'[CQ:record,file={record_file}]')
        if not is_find_group:
            print('3')
            await session.send('指挥官,请使用[更换声源]命令对该群语音状态初始化喵~')
    else:
        print('4')
        await session.send('指挥官,请使用[更换声源]命令对该群语音状态初始化喵~')


@on_natural_language(keywords={'语音'}, only_to_me=False)
async def _(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(95.0, 'send_record')


@on_command('qielu', aliases=('切噜', 'qielu'), only_to_me=False)
async def qielu(session: CommandSession):
    print(session.event)
    sender_id = session.event['sender']['user_id']
    print(sender_id)
    image_dir = os.path.join('images/qielu')
    print(os.listdir(image_dir))
    print(r.randint(0, len(os.listdir(image_dir)) - 1))
    file = os.listdir(image_dir)[r.randint(0, len(os.listdir(image_dir)) - 1)]
    file_path = 'images/qielu/' + file
    cqimage = load_image_as_cqimage(file_path)
    message = f'[CQ:at,qq={sender_id}]切噜噜~♫~(=^･ω･^)ﾉ\n' + cqimage
    await session.send(message)
    await session.send('[CQ:record,file=切噜~.mp3]')


@on_natural_language(keywords={"切噜", "qielu"}, only_to_me=False)
async def _(session: NLPSession):
    return IntentCommand(90.0, 'qielu')


if __name__ == '__main__':
    print(os.path.join(os.path.dirname(__file__), 'recording.json').replace('\\', '/'))
    print(os.path.join(config.CQ_SOURCE_PATH, 'record', '123.mp3'))
