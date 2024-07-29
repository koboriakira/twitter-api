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
        # 日付を July 28, 2024 のように表現
        date = self.created_at.value.strftime("%B %d, %Y")
        text = f"""<blockquote class="twitter-tweet">
<p lang="en" dir="ltr">{self.text}</p>&mdash; {self.user.name} (@{self.user.screen_name})
 <a href="https://twitter.com/kobori_akira_pw/status/1817404940853338530?ref_src=twsrc%5Etfw">{date}</a>
</blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
"""
        return text.replace("\n", "")
