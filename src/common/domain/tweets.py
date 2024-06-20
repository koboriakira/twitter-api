from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime

from common.domain.tweet import Tweet


@dataclass
class Tweets:
    values: list[Tweet]

    def filter_range(self, start_datetime: datetime | None, end_datetime: datetime | None) -> "Tweets":
        """指定した期間内のツイートのみを取得します"""
        values = self.values
        if start_datetime is not None:
            values = [tweet for tweet in values if tweet.created_at.eq_or_after(start_datetime)]
        if end_datetime is not None:
            values = [tweet for tweet in values if tweet.created_at.eq_or_before(end_datetime)]
        return Tweets(values)

    def __iter__(self) -> Iterator[Tweet]:
        return iter(self.values)
