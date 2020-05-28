from datetime import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from pykeyboard import PyKeyboard
import win32api
import win32con
import keyboard


def record_task():
    # win32api.keybd_event(0x12, 0, 0, 0)  # alt键位码是17
    # win32api.keybd_event(0x51, 0, 0, 0)  # Q键位码是81
    # win32api.keybd_event(0x12, 0, win32con.KEYEVENTF_KEYUP, 0)
    # win32api.keybd_event(0x51, 0, win32con.KEYEVENTF_KEYUP, 0)
    keyboard.press_and_release('alt+q')
    print('Tapped')


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(record_task, 'interval', seconds=5)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
