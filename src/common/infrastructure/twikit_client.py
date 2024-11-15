import asyncio
import os
import time
from logging import Logger, getLogger
from pathlib import Path

from fake_useragent import UserAgent
from twikit import Client
from twikit.user import User

from common.domain.tweet import Tweet
from common.domain.tweets import Tweets
from common.infrastructure.twikit_converter import TwikitConverter
from common.value.tweet_id import TweetId
from utils.environment import Environment
from utils.s3_client import S3Client

TMP_DIR = "/tmp"  # noqa: S108
COOKIE_FILE_PATH = f"{TMP_DIR}/twikit_cookies.json"

UA = UserAgent(os="macos")

class Twikit:
    def __init__(self, client: Client, logger: Logger|None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    @staticmethod
    async def generate_instance() -> "Twikit":
        client = Client(language="en-US", user_agent=UA.safari)

        if Environment.is_production():
            s3_client = S3Client()
            s3_client.download(COOKIE_FILE_PATH)

        if Path(COOKIE_FILE_PATH).exists():
            client.load_cookies(COOKIE_FILE_PATH)
            return Twikit(client)

        count = 0
        while count < 3:
            try:
                await client.login(
                    auth_info_1=os.environ["TWITTER_USER_NAME"],
                    auth_info_2=os.getenv("TWITTER_EMAIL_ADDRESS"),
                    password=os.environ["TWITTER_PASSWORD"],
                )
                client.save_cookies(COOKIE_FILE_PATH)
                if Environment.is_production():
                    s3_client = S3Client()
                    s3_client.upload(COOKIE_FILE_PATH)
                return Twikit(client)
            except Exception as e:
                count += 1
                print(f"Failed to login: {e}")
                continue
        raise Exception("Failed to login")

    async def find_tweet_by_id(self, tweet_id: TweetId) -> Tweet:
        time.sleep(1)
        tweet = await self._client.get_tweet_by_id(tweet_id.value)
        return TwikitConverter.convert_tweet(tweet)

    async def get_tweets_by_screen_name(self, screen_name: str) -> Tweets:
        """指定したユーザーのツイートを取得します"""
        time.sleep(1)
        user = await self._client.get_user_by_screen_name(screen_name)
        time.sleep(1)
        user_tweets = await user.get_tweets("Tweets")
        user_tweet_ids = [TweetId(tweet.id) for tweet in user_tweets]
        return Tweets([await self.find_tweet_by_id(tweet_id) for tweet_id in user_tweet_ids])

    async def my(self) -> User:
        time.sleep(1)
        return await self._client.get_user_by_screen_name(os.environ["TWITTER_USER_NAME"])

async def main():
    twikit = await Twikit.generate_instance()
    result = await twikit.get_tweets_by_screen_name("kobori_akira_pw")
    print(result)

if __name__ == "__main__":
    # python -m src.common.infrastructure.twikit_client
    asyncio.run(main())
