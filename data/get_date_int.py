from datetime import timedelta, datetime
import time


def get_date_int(date: datetime) -> int:
    today = int(date.strftime("%Y%m%d"))
    current_time = int(time.strftime("%H", time.localtime()))
    # 如果是五点前，出刀算入上一天
    if current_time < 5:
        today = int((date - timedelta(days=1)).strftime("%Y%m%d"))
    return today
