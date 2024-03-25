from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9), "JST")


@dataclass(frozen=True)
class CreatedAt:
    value: datetime

    @staticmethod
    def from_twikit_str(value: str) -> "CreatedAt":
        value = datetime.strptime(value, "%a %b %d %H:%M:%S %z %Y").astimezone(JST)
        return CreatedAt(value)
