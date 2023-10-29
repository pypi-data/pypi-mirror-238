from datetime import datetime


def now():
    return datetime.now()


def format(dt: datetime = None, format: str = "%Y-%m-%dT%H:%M:%S.%f") -> str:
    if dt is None:
        dt = now()
    return dt.strftime(format)


def parse(dt_str: str, format: str = "%Y-%m-%dT%H:%M:%S.%f") -> datetime:
    return datetime.strptime(dt_str, format)


def format_duration(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"
