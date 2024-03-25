from dataclasses import dataclass
from common.value.user_id import UserId
from common.value.url import Url


@dataclass
class User:
    user_id: UserId
    name: str
    screen_name: str
    url: Url
