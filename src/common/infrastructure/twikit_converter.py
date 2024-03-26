from common.domain.tweet import Tweet
from common.domain.user import User
from common.value.created_at import CreatedAt
from common.value.media import Media
from common.value.medium import Medium
from common.value.tweet_id import TweetId
from common.value.url import Url
from common.value.user_id import UserId


class TwikitConverter:
    @staticmethod
    def convert_tweet(tweet) -> Tweet:
        all_params = {
            "id": tweet.id,
            "created_at": tweet.created_at,
            "text": tweet.text,
            # "favorite_count": tweet.favorite_count,
            "media": tweet.media,
            "user": tweet.user,
            # "replies": tweet.replies,
            # "reply_to": tweet.reply_to,
            # "lang": tweet.lang,
            # "is_quote_status": tweet.is_quote_status,
            # "possibly_sensitive": tweet.possibly_sensitive,
            # "possibly_sensitive_editable": tweet.possibly_sensitive_editable,
            # "quote_count": tweet.quote_count,
            # "reply_count": tweet.reply_count,
            # "favorited": tweet.favorited,
            # "view_count": tweet.view_count,
            # "retweet_count": tweet.retweet_count,
            # "editable_until_msecs": tweet.editable_until_msecs,
            # "is_translatable": tweet.is_translatable,
            # "is_edit_eligible": tweet.is_edit_eligible,
            # "edits_remaining": tweet.edits_remaining,
            # "state": tweet.state,
        }
        tweet_id = TweetId(value=all_params["id"])
        media = TwikitConverter.convert_media(all_params["media"])
        text = all_params["text"]
        created_at = CreatedAt.from_twikit_str(value=all_params["created_at"])
        user = TwikitConverter.convert_user(all_params["user"])
        return Tweet(
            tweet_id=tweet_id,
            media=media,
            text=text,
            created_at=created_at,
            user=user,
        )

    @staticmethod
    def convert_user(user) -> Media:
        return User(
            user_id=UserId(value=user.id),
            name=user.name,
            screen_name=user.screen_name,
            url=Url(value=user.url),
        )

    @staticmethod
    def convert_media(media) -> Media | None:
        if media is None:
            return None
        return Media(values=[TwikitConverter.convert_medium(m) for m in media])

    @staticmethod
    def convert_medium(medium) -> Medium:
        return Medium(
            media_url_https=medium["media_url_https"],
            display_url=medium["display_url"],
            expanded_url=medium["expanded_url"],
            ext_alt_text=medium.get("ext_alt_text", ""),
        )
