import asyncio
from datetime import datetime

from common.domain.tweets import Tweets
from common.infrastructure.twikit_client import Twikit
from utils import dateutil


class ListTweetsUseCase:
    def __init__(self, twitter_client: Twikit) -> None:
        self._twitter_client = twitter_client

    async def execute(
        self,
        user_screen_name: str,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> Tweets:
        tweets = await self._twitter_client.get_tweets_by_screen_name(user_screen_name)
        return tweets.filter_range(start_datetime, end_datetime)


async def main():
    twitter_client = await Twikit.generate_instance()
    usecase = ListTweetsUseCase(twitter_client=twitter_client)
    start_str = datetime(2024, 11, 15, 11, 0, 0, 0, tzinfo=dateutil.JST).isoformat()
    end_str = datetime(2024, 11, 15, 12, 0, 0, 0, tzinfo=dateutil.JST).isoformat()
    print(start_str, end_str)
    tweets = await usecase.execute(
        user_screen_name="kobori_akira_pw",
        start_datetime=datetime.fromisoformat(start_str),
        end_datetime=datetime.fromisoformat(end_str),
    )
    print([tweet for tweet in tweets])


if __name__ == "__main__":
    # python -m src.use_case.list_tweets_use_case
    asyncio.run(main())
