from common.infrastructure.twikit_converter import TwikitConverter
from twikit import Client
import os
from pathlib import Path
from common.value.tweet_id import TweetId

COOKIE_FILE_DIR = "/tmp/twikit"
Path(COOKIE_FILE_DIR).mkdir(parents=True, exist_ok=True)

COOKIE_FILE_PATH = f"{COOKIE_FILE_DIR}/cookies.json"


class Twikit:

    def __init__(self, client: Client):
        self._client = client

    @staticmethod
    def generate_instance() -> "Twikit":
        client = Client("ja")
        if os.path.exists(COOKIE_FILE_PATH):
            client.load_cookies(COOKIE_FILE_PATH)
        else:
            client.login(
                auth_info_1=os.getenv("TWITTER_USER_NAME"),
                auth_info_2=os.getenv("TWITTER_EMAIL_ADDRESS"),
                password=os.getenv("TWITTER_PASSWORD"),
            )
            client.save_cookies(COOKIE_FILE_PATH)
        return Twikit(client)

    def find_tweet_by_id(self, tweet_id: TweetId):
        tweet = self._client.get_tweet_by_id(tweet_id.value)
        user_id = tweet.user.id
        user = self._client.get_user_by_id(user_id)
        return TwikitConverter.convert_tweet(tweet)

    def my(
        self,
    ):
        return self._client.get_user_by_screen_name(os.getenv("TWITTER_USER_NAME"))

    def get_user_by_screen_name(self, screen_name):
        return self._client.get_user_by_screen_name(screen_name)


if __name__ == "__main__":
    # python -m src.common.infrastructure.twikit
    import json

    twikit = Twikit.generate_instance()

    tweet = twikit.find_tweet_by_id(TweetId("1772269440396333105"))
    print(tweet)
    print(tweet.url)
