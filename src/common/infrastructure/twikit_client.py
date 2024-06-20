import os
from pathlib import Path

from twikit import Client, User

from common.domain.tweet import Tweet
from common.domain.tweets import Tweets
from common.infrastructure.twikit_converter import TwikitConverter
from common.value.tweet_id import TweetId
from utils.environment import Environment
from utils.s3_client import S3Client

TMP_DIR = "/tmp"  # noqa: S108
COOKIE_FILE_PATH = f"{TMP_DIR}/twikit_cookies.json"


class Twikit:
    def __init__(self, client: Client) -> None:
        self._client = client

    @staticmethod
    def generate_instance() -> "Twikit":
        client = Client("ja")

        if Environment.is_production():
            s3_client = S3Client()
            s3_client.download(COOKIE_FILE_PATH)

        if Path(COOKIE_FILE_PATH).exists():
            client.load_cookies(COOKIE_FILE_PATH)
        else:
            client.login(
                auth_info_1=os.getenv("TWITTER_USER_NAME"),
                auth_info_2=os.getenv("TWITTER_EMAIL_ADDRESS"),
                password=os.getenv("TWITTER_PASSWORD"),
            )
            client.save_cookies(COOKIE_FILE_PATH)
            if Environment.is_production():
                s3_client = S3Client()
                s3_client.upload(COOKIE_FILE_PATH)
        return Twikit(client)

    def find_tweet_by_id(self, tweet_id: TweetId) -> Tweet:
        tweet = self._client.get_tweet_by_id(tweet_id.value)
        return TwikitConverter.convert_tweet(tweet)

    def get_tweets_by_screen_name(self, screen_name: str) -> Tweets:
        """指定したユーザーのツイートを取得します"""
        user = self._client.get_user_by_screen_name(screen_name)
        user_tweets = user.get_tweets("Tweets")
        user_tweet_ids = [TweetId(tweet.id) for tweet in user_tweets]
        return Tweets([self.find_tweet_by_id(tweet_id) for tweet_id in user_tweet_ids])

    def my(self) -> User:
        return self._client.get_user_by_screen_name(os.getenv("TWITTER_USER_NAME"))


if __name__ == "__main__":
    # python -m src.common.infrastructure.twikit

    twikit = Twikit.generate_instance()

    tweet = twikit.find_tweet_by_id(TweetId("1772269440396333105"))
    print(tweet)
    print(tweet.url)
