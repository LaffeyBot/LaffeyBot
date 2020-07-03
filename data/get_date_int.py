from datetime import timedelta, datetime
import time


def get_date_int(date: datetime, with_hour: bool = False) -> int:
    format_str = "%Y%m%d"
    if with_hour:
        format_str = "%Y%m%d%H"
    today = int(date.strftime(format_str))
    current_time = int(time.strftime("%H", time.localtime()))
    # 如果是五点前，出刀算入上一天
    if current_time < 5 and not with_hour:
        today = int((date - timedelta(days=1)).strftime("%Y%m%d"))
    return today
