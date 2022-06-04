import datetime


def format_elapsed_time(duration: float, include_days: bool = True) -> str:
    """Format elapsed time to number of days/hours etc"""
    sec = datetime.timedelta(seconds=duration)
    d = datetime.datetime(1, 1, 1) + sec
    return ('%dd %dh %dm %ds' % (d.day - 1, d.hour, d.minute, d.second)) if include_days else (
            '%dh %dm %ds' % (d.hour, d.minute, d.second))
