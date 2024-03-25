from dataclasses import dataclass
from common.value.created_at import CreatedAt
from common.value.media import Media
from common.value.tweet_id import TweetId
from common.value.user_id import UserId
from common.domain.user import User


@dataclass
class Tweet:
    tweet_id: TweetId
    text: str
    created_at: CreatedAt
    user: User
    media: Media | None = None

    @property
    def url(self) -> str:
        return (
            f"https://twitter.com/{self.user.screen_name}/status/{self.tweet_id.value}"
        )
