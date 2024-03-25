from dataclasses import dataclass


@dataclass(frozen=True)
class Url:
    value: str
