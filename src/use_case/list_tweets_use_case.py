from datetime import datetime

from common.domain.tweets import Tweets
from common.infrastructure.twikit_client import Twikit
from utils import dateutil


class ListTweetsUseCase:
    def __init__(self, twitter_client: Twikit) -> None:
        self._twitter_client = twitter_client

    def execute(
        self,
        user_screen_name: str,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> Tweets:
        tweets = self._twitter_client.get_tweets_by_screen_name(user_screen_name)
        return tweets.filter_range(start_datetime, end_datetime)


if __name__ == "__main__":
    # python -m src.use_case.list_tweets_use_case
    usecase = ListTweetsUseCase(twitter_client=Twikit.generate_instance())
    tweets = usecase.execute(
        user_screen_name="kobori_akira_pw",
        start_datetime=dateutil.jst_datetime(year=2024, month=6, day=9),
        end_datetime=dateutil.jst_datetime(year=2024, month=6, day=10),
    )
    print([tweet.embed_tweet_url for tweet in tweets])
