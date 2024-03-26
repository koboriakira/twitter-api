import os
from pathlib import Path

from src.common.domain.tweet import Tweet
from src.utils.environment import Environment
from src.utils.s3_client import S3Client
from twikit import Client

from common.infrastructure.twikit_converter import TwikitConverter
from common.value.tweet_id import TweetId

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

    def my(
        self,
    ):
        return self._client.get_user_by_screen_name(os.getenv("TWITTER_USER_NAME"))

    def get_user_by_screen_name(self, screen_name):
        return self._client.get_user_by_screen_name(screen_name)


if __name__ == "__main__":
    # python -m src.common.infrastructure.twikit

    twikit = Twikit.generate_instance()

    tweet = twikit.find_tweet_by_id(TweetId("1772269440396333105"))
    print(tweet)
    print(tweet.url)
