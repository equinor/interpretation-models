import datetime
from models.metadata import SourceContext
import pytz


def id_generate(
    context: SourceContext, native_id: str
) -> str:
    return f"{context.database}:{context.project}:{native_id}"

def convert_date_to_utc(
    date: datetime.datetime, timezone: str | None = None
) -> datetime.datetime | None:
    if timezone is None:
        return date
    local_tz = pytz.timezone(timezone)
    local_dt = local_tz.localize(date) if date.tzinfo is None else date.astimezone(local_tz)
    return local_dt.astimezone(pytz.utc)
