from http import HTTPMethod

import requests

from scrapify_ig import types


__all__ = [
    "UserMixin",
]


class UserMixin(object):
    """
    Used to process Instagram users

    @DynamicAttrs
    """

    def get_user_info(
            self,
            username_or_id_or_url: str,
            include_about: bool = False,
            url_embed_safe: bool = False
    ) -> types.User:
        """ Get user profile information. Includes contact details (email, phone, etc.), if present.

            :param username_or_id_or_url - user identifier.
            :param include_about - include user about information. See types.UserAbout class.
            Include 'About this account' information: country and date_joined (in about field).
            :param url_embed_safe - If you need to embed images/videos on your website,
            set to 'True' to evade CORS restrictions.
        """
        response: requests.Response = self.api_request(
            url="/info",
            method=HTTPMethod.GET,
            params={
                "username_or_id_or_url": username_or_id_or_url,
                "include_about": include_about,
                "url_embed_safe": url_embed_safe
            }
        )
        return types.User(**response.json()["data"])

    def get_followers_chunk(
            self,
            username_or_id_or_url: str,
            amount: int = 50,
            pagination_token: str = None
    ) -> types.FollowersChunk:
        """
        Get user followers. Up to 1000 at a time.
        This endpoint is paginated. Use the token from the previous request to retrieve the continuation of the list.
        Leave empty in the first request.
        """
        response: requests.Response = self.api_request(
            url="/followers",
            method=HTTPMethod.GET,
            params={
                "username_or_id_or_url": username_or_id_or_url,
                "amount": amount,
                "pagination_token": pagination_token
            }
        )
        return types.FollowersChunk(
            **response.json(),
            client=self,
            amount=amount,
            user_identifier=username_or_id_or_url
        )

    def get_user_medias_chunk(
            self,
            username_or_id_or_url: str,
            pagination_token: str = None,
            url_embed_safe: bool = False
    ) -> types.MediaPostsChunk:
        """
        Get user posts. 12 posts at a time.
        This endpoint is paginated. Use the token from the previous request to retrieve the continuation of the list.
        Leave empty in the first request.

        :param username_or_id_or_url - user identifier.
        :param pagination_token - Use the value from the previous request to retrieve the continuation of the list.
        Leave empty in the first request.
        :param url_embed_safe - If you need to embed images/videos on your website,
        set to 'True' to evade CORS restrictions.
        """
        response: requests.Response = self.api_request(
            url="/posts",
            method=HTTPMethod.GET,
            params={
                "username_or_id_or_url": username_or_id_or_url,
                "pagination_token": pagination_token,
                "url_embed_safe": url_embed_safe
            }
        )
        return types.MediaPostsChunk(
            **response.json(),
            client=self,
            user_identifier=username_or_id_or_url
        )

    def get_similar_accounts(self, username_or_id_or_url: str) -> types.SimilarAccounts:
        """ Find similar Instagram accounts """
        response: requests.Response = self.api_request(
            url="/similar_accounts",
            method=HTTPMethod.GET,
            params={
                "username_or_id_or_url": username_or_id_or_url
            }
        )
        return types.SimilarAccounts(**response.json()["data"])
