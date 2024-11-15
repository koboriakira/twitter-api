from datetime import timedelta

from fastapi import APIRouter

from common.infrastructure.twikit_client import Twikit
from interface.fastapi_router.tweet.tweet_response import (
    TweetModelTranslator,
    TweetsResponse,
)
from use_case.list_tweets_use_case import ListTweetsUseCase
from utils.dateutil import jst_today_datetime

router = APIRouter()


@router.get("/{user_screen_name}/tweets/")
async def get_tweet(user_screen_name: str) -> TweetsResponse:
    """指定したユーザーの当日のツイートを取得します"""
    try:
        twitter_client = await Twikit.generate_instance()
        use_case = ListTweetsUseCase(twitter_client=twitter_client)
        tweets = await use_case.execute(
            user_screen_name=user_screen_name,
            start_datetime=jst_today_datetime() - timedelta(days=1),
            end_datetime=jst_today_datetime(),
        )
        tweet_models = [TweetModelTranslator.translate(tweet) for tweet in tweets]
        return TweetsResponse(data=tweet_models)
    except Exception as e:
        return TweetsResponse(status="ERROR", message=str(e))
