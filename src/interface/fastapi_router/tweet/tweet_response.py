from interface.fastapi_router.base_response import BaseResponse
from common.domain.tweet import Tweet
from pydantic import BaseModel, Field
from datetime import datetime


class UserModel(BaseModel):
    id: str
    name: str
    screen_name: str


class MediumModel(BaseModel):
    url: str
    alt_text: str


class TweetModel(BaseModel):
    id: str
    text: str
    url: str
    created_at: datetime
    user: UserModel
    media: list[MediumModel] | None = Field(default=None)


class TweetResponse(BaseResponse):
    data: TweetModel


class TweetModelTranslator:
    @staticmethod
    def translate(tweet: Tweet) -> TweetResponse:
        user_model = UserModel(
            id=tweet.user.user_id.value,
            name=tweet.user.name,
            screen_name=tweet.user.screen_name,
        )
        medium_list = tweet.media.values if tweet.media is not None else []
        media = [
            MediumModel(url=m.media_url_https, alt_text=m.ext_alt_text)
            for m in medium_list
        ]
        tweet_model = TweetModel(
            id=tweet.tweet_id.value,
            text=tweet.text,
            url=tweet.url,
            created_at=tweet.created_at.value,
            user=user_model,
            media=media if len(media) > 0 else None,
        )
        return TweetResponse(data=tweet_model)
