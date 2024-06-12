from fastapi import APIRouter

from common.infrastructure.twikit_client import Twikit
from common.value.tweet_id import TweetId
from interface.fastapi_router.tweet.tweet_response import (
    TweetModelTranslator,
    TweetResponse,
)
from use_case.find_tweet_use_case import FindTweetUseCase

router = APIRouter()


@router.get("/{tweet_id}")
def get_tweet(tweet_id: str) -> TweetResponse:
    twitter_client = Twikit.generate_instance()
    use_case = FindTweetUseCase(twitter_client=twitter_client)
    tweet = use_case.execute(tweet_id=TweetId(tweet_id))
    return TweetModelTranslator.translate(tweet)
