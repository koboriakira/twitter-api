from datetime import timedelta

from fastapi import APIRouter

from common.infrastructure.twikit_client import Twikit
from interface.fastapi_router.tweet.tweet_response import (
    TweetModelTranslator,
    TweetResponse,
)
from use_case.list_tweets_use_case import ListTweetsUseCase
from utils.dateutil import jst_today_datetime

router = APIRouter()


@router.get("/{user_screen_name}/tweets/")
def get_tweet(user_screen_name: str) -> list[TweetResponse]:
    """指定したユーザーの当日のツイートを取得します"""
    twitter_client = Twikit.generate_instance()
    use_case = ListTweetsUseCase(twitter_client=twitter_client)
    tweets = use_case.execute(
        user_screen_name=user_screen_name,
        start_datetime=jst_today_datetime() - timedelta(days=1),
        end_datetime=jst_today_datetime(),
    )
    return [TweetModelTranslator.translate(tweet) for tweet in tweets]
