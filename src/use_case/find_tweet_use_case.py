from common.infrastructure.twikit_client import Twikit
from common.domain.tweet import Tweet
from common.value.tweet_id import TweetId


class FindTweetUseCase:

    def __init__(self, twitter_client: Twikit):
        self._twitter_client = twitter_client

    def execute(self, tweet_id: TweetId) -> Tweet:
        return self._twitter_client.find_tweet_by_id(tweet_id)
