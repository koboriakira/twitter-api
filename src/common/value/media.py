from dataclasses import dataclass
from common.value.medium import Medium


@dataclass(frozen=True)
class Media:
    values: list[Medium]
