from dataclasses import dataclass

from common.value.url import Url
from common.value.user_id import UserId


@dataclass
class User:
    user_id: UserId
    name: str
    screen_name: str
    url: Url
