from datetime import timedelta, datetime
import time
import pytz


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


def get_date_start_end(of_date: datetime) -> (datetime, datetime):
    start = of_date.replace(hour=5, minute=0, second=0, microsecond=0)
    end = start + timedelta(1)

    return start, end
