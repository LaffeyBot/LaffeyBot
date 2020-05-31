from datetime import datetime
import os
from pcr.plugins.ocr import recognize_text
import warnings
from data import damage, init
import nonebot
import my_config as config


@nonebot.scheduler.scheduled_job('interval', seconds=10)
async def _():
    await record_task()


async def record_task():
    screenshot_path = 'screenshots/screen.png'
    connect()
    screenshot(screenshot_path)
    result = recognize_text(screenshot_path)
    print(result)
    #  然后传回做数据处理
    new_records = damage.add_record(result)
    # 然后调用NoneBot给群聊发信息汇报
    await alert_new_record(new_records)


async def alert_new_record(new_records: list):
    if len(new_records) == 0:
        return
    message = '添加了新的记录\n'
    for record in new_records:
        message += '- ' + record[0] + '对' + record[1] + '造成了 ' + str(record[2]) + ' 点伤害\n'
    print(message)
    print(config.GROUP_ID)
    await nonebot.get_bot().send_group_msg(group_id=config.GROUP_ID, message=message)


def connect():
    try:
        os.system('adb connect 127.0.0.1:7555')
    except:
        warnings.warn("无法连接到模拟器，请检查模拟器是否正常运作。")


def screenshot(relative_path: str):
    path = os.path.abspath('.') + '/' + relative_path
    os.system('adb shell screencap /data/screen.png')
    os.system('adb pull /data/screen.png %s' % path)


# if __name__ == '__main__':
    # if not os.path.isfile('main.db'):
    #     init.init_database()
