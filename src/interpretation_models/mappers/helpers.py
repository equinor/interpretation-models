import datetime

from interpretation_models.models import SourceContext
import pytz


def localize_date(
    date: datetime.datetime, timezone: str | None = None
) -> datetime.datetime:
    """Attach the given timezone to a naive datetime (or convert an aware one)."""
    if timezone is None:
        return date
    local_tz = pytz.timezone(timezone)
    return local_tz.localize(date) if date.tzinfo is None else date.astimezone(local_tz)


def convert_date_to_utc(
    date: datetime.datetime, timezone: str | None = None
) -> datetime.datetime:
    if timezone is None:
        return date
    local_dt = localize_date(date, timezone)
    return local_dt.astimezone(pytz.utc)


def id_generate(
    context: SourceContext, native_id: str
) -> str:
    return f"{context.database}:{context.project}:{native_id}"
