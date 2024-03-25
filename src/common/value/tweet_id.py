from dataclasses import dataclass


@dataclass(frozen=True)
class TweetId:
    value: str
