from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=9), "JST")


@dataclass(frozen=True)
class CreatedAt:
    value: datetime

    @staticmethod
    def from_twikit_str(value: str) -> "CreatedAt":
        value = datetime.strptime(value, "%a %b %d %H:%M:%S %z %Y").astimezone(JST)
        return CreatedAt(value)

    def eq_or_before(self, datetime: datetime) -> bool:
        return self.value.timestamp() <= datetime.timestamp()

    def eq_or_after(self, datetime: datetime) -> bool:
        return self.value.timestamp() >= datetime.timestamp()
