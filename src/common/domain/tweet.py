from dataclasses import dataclass

from common.domain.user import User
from common.value.created_at import CreatedAt
from common.value.media import Media
from common.value.tweet_id import TweetId


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

    @property
    def embed_tweet_url(self) -> str:
        return f"https://publish.twitter.com/?query={self.url}&widget=Tweet"

    @property
    def embed_tweet_html(self) -> str:
        """埋め込みツイートのリンクを取得。実際につくるのは大変すぎた"""
        expanded_url = (
            f"https://twitter.com/{self.user.screen_name}/status/{self.tweet_id.value}"
        )
        return f"https://publish.twitter.com/?query={expanded_url}&widget=Tweet"
