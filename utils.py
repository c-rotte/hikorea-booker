import time


def get_today_ymd() -> str:
    return time.strftime("%Y%m%d")


def get_ymd_in_one_year() -> str:
    return time.strftime("%Y%m%d", time.localtime(time.time() + 31536000))
