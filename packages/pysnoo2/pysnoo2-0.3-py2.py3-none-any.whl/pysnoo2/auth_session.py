"""PySnoo2 OAuth Session."""

import json
import logging

from typing import (Callable, Any)

from oauthlib.oauth2 import LegacyApplicationClient

from .const import (OAUTH_CLIENT_ID,
                    OAUTH_TOKEN_REFRESH_ENDPOINT,
                    OAUTH_LOGIN_ENDPOINT,
                    BASE_HEADERS)
from .oauth2_session import OAuth2Session

from typing import (
    Union,
)

from yarl import URL
StrOrURL = Union[str, URL]

_LOGGER = logging.getLogger(__name__)


class SnooAuthSession(OAuth2Session):
    """Snoo-specific OAuth2 Session Object"""

    def __init__(
            self,
            username,
            password,
            token: dict = None,
            token_updater: Callable[[dict], None] = None) -> None:
        """Construct a new OAuth 2 client session."""

        # From Const
        super().__init__(
            client=LegacyApplicationClient(client_id=OAUTH_CLIENT_ID),
            auto_refresh_url=OAUTH_TOKEN_REFRESH_ENDPOINT,
            auto_refresh_kwargs=None,
            scope=None,
            redirect_uri=None,
            token=token,
            state=None,
            token_updater=token_updater,
            headers=BASE_HEADERS)
        
        self.username = username
        self.password = password
        
    async def get(self, url: StrOrURL, *, allow_redirects: bool=True, **kwargs: Any):
        """Perform HTTP GET request."""
        response = await super().get(url, allow_redirects=allow_redirects, **kwargs)
        
        if response.status in {401, 403}:
            _LOGGER.debug('Received 401/403 from response, attempting to re-auth')
            await self._reAuth()
            response = await super().get(url, allow_redirects=allow_redirects, **kwargs)
        self._logResponse(response)
        return response
    
    async def post(self, url: StrOrURL, *, data: Any=None, **kwargs: Any):
        """Perform HTTP POST request."""
        response = await super().post(url, data=data, **kwargs)
        
        if response.status in {401, 403}:
            _LOGGER.debug('Received 401/403 from response, attempting to re-auth')
            await self._reAuth()
            response = await super().post(url, data=data, **kwargs)
        self._logResponse(response)
        return response
    
    async def patch(self, url: StrOrURL,
              *, data: Any=None, **kwargs: Any):
        """Perform HTTP GET request."""
        response = await super().patch(url, data=data, **kwargs)
        
        if response.status in {401, 403}:
            _LOGGER.debug('Received 401/403 from response, attempting to re-auth')
            await self._reAuth()
            response = await super().post(url, data=data, **kwargs)
        self._logResponse(response)
        return response
    
    async def _reAuth(self):
        _LOGGER.debug('Getting new access token for reauth')
        new_token = await self.fetch_token()
        self.token_updater(new_token)

    def _logResponse(self, response):
        if response.status != 200:
            _LOGGER.warn("Response failed with status %s", response.status)

    async def fetch_token(self):  # pylint: disable=arguments-differ
        # Note, Snoo OAuth API is not 100% RFC 6749 compliant. (Wrong Content-Type)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
        }
        return await super().fetch_token(OAUTH_LOGIN_ENDPOINT, code=None, authorization_response=None,
                                         body='', auth=None, username=self.username, password=self.password, method='POST',
                                         timeout=None, headers=headers, verify_ssl=True,
                                         post_payload_modifier=json.dumps)
