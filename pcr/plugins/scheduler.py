from datetime import datetime
import os
from pcr.plugins.ocr import recognize_text
import warnings
from data import damage
import nonebot
from pcr.plugins.alert_new_record import alert_new_record


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
    new_records, did_kill = damage.add_record(result)
    # 然后调用NoneBot给群聊发信息汇报
    await alert_new_record(new_records, did_kill)


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
