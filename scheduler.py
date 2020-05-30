from datetime import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from pcr.plugins.ocr import recognize_text
import warnings


def record_task():
    screenshot_path = 'screenshots/screen.png'
    connect()
    screenshot(screenshot_path)
    result = recognize_text(screenshot_path)
    print(result)
    # TODO: 然后传回做数据处理
    # TODO: 然后调用NoneBot给群聊发信息汇报


def connect():
    try:
        os.system('adb connect 127.0.0.1:7555')
    except:
        warnings.warn("无法连接到模拟器，请检查模拟器是否正常运作。")


def screenshot(relative_path: str):
    path = os.path.abspath('.') + '/' + relative_path
    os.system('adb shell screencap /data/screen.png')
    os.system('adb pull /data/screen.png %s' % path)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(record_task, 'interval', seconds=10)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
