from datetime import date, datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), "JST")


def jst_now() -> datetime:
    return datetime.now(JST)


def jst_today_datetime() -> datetime:
    return jst_now().replace(hour=0, minute=0, second=0, microsecond=0)


def jst_today() -> date:
    return jst_now().date()


def jst_yesterday() -> date:
    return jst_today() - timedelta(days=1)


def jst_date(days: int = 0) -> datetime:
    """今日を基準に、指定した日数前後の日時を取得します。正の値で未来、負の値で過去の日時を取得します。"""
    return jst_today_datetime() + timedelta(days=days)


def jst_datetime(  # noqa: PLR0913
    year: int = 0,
    month: int = 0,
    day: int = 0,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
) -> datetime:
    """指定した日時を取得します。指定しない場合は、現在の日時を取得します。"""
    return jst_now().replace(year=year, month=month, day=day, hour=hour, minute=minute, second=second)


def convert_to_date_or_datetime(value: str | None, cls: type | None = None) -> date | datetime | None:
    if value is None:
        return None
    length_date = 10  # "YYYY-MM-DD"
    value_error_msg = f"Invalid class: {cls}"
    if len(value) == length_date:
        tmp_date = date.fromisoformat(value)
        if cls is None or cls == date:
            return tmp_date
        if cls == datetime:
            return datetime(tmp_date.year, tmp_date.month, tmp_date.day, tzinfo=JST)
        raise ValueError(value_error_msg)
    tmp_datetime = datetime.fromisoformat(value)
    if cls is None or cls == datetime:
        return tmp_datetime
    if cls == date:
        return tmp_datetime.date()
    raise ValueError(value_error_msg)
