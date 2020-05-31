import time
import os
from pcr.plugins.ocr import recognize_text, image_to_position
import warnings
from data import damage
import nonebot
import config
from data.json.json_editor import JSONEditor
from pcr.plugins.alert_new_record import alert_new_record


@nonebot.scheduler.scheduled_job('interval', seconds=config.FETCH_INTERVAL)
async def _():
    if JSONEditor().get_fetch_status():
        await record_task()


async def record_task():
    screenshot_path = 'screenshots/screen.png'
    connect()
    refresh_data()
    screenshot(screenshot_path)
    result = recognize_text(screenshot_path)
    print(result)
    #  然后传回做数据处理
    new_records, did_kill = damage.add_record(result)
    # 然后调用NoneBot给群聊发信息汇报
    await alert_new_record(new_records, did_kill)


def refresh_data():
    images = ['back_button', 'gild_battle', 'expand_button']
    screenshot_path = 'screenshots/screen.png'
    for image in images:
        screenshot(screenshot_path)
        center = image_to_position(image)
        if center is not None:
            click(center[0], center[1])
            time.sleep(1)


def click(x, y):
    os.system('adb shell input tap %s %s' % (x, y))


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
