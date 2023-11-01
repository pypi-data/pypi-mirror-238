import uuid
from urllib.parse import parse_qs, urlparse

from destipy.utils.error import InvalidStateException

from .utils.http_method import HTTPMethod
from .utils.requester import Requester


class OAuth:
    """This class handles all the OAuth requests to the Bungie.net API.
    """
    def __init__(self, client_id, client_secret, requester, redirect_url, logger):
        self.logger = logger
        self.client_id = client_id
        self.client_secret = client_secret
        self.requester: Requester = requester
        self.active_states = []
        self.redirect_url = redirect_url
        self.TOKEN_URL = "https://www.bungie.net/platform/app/oauth/token/"
        self.OAUTH_URL = "https://www.bungie.net/en/OAuth/"

    async def gen_auth_link(self) -> str:
        """Generates an authentication link for the user to use to authenticate with Bungie.net

        Returns:
            str: The authentication link
        """
        self.logger.info("Generating auth link...")
        state = uuid.uuid4().hex
        self.active_states.append(state)
        url = "{}authorize?client_id={}&response_type=code&state={}&redirect_uri={}".format(
            self.OAUTH_URL, self.client_id, state, self.redirect_url)
        return url

    async def fetch_token_from_url(self, url: str) -> dict:
        """Fetches an authentication token from the Bungie.net API using the url for simplicity

        Args:
            url (str): The url the user is redirected to after authenticating with Bungie.net

        Raises:
            Exception: Error fetching token. Reason: response

        Returns:
            dict: The authentication token
        """
        parts = urlparse(url)
        query_dict = parse_qs(parts.query)
        url = self.TOKEN_URL
        return await self.fetch_token(query_dict["code"][0], query_dict["state"][0])

    async def fetch_token(self, code: str, state: str) -> dict:
        """Fetches an authentication token from the Bungie.net API given the user's authentication code

        Args:
            code (str): The user's authentication code
            state (str): The state of the authentication

        Raises:
            Exception: Error fetching token. Reason: response

        Returns:
            dict: The authentication token
        """
        url = self.TOKEN_URL
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "code": code,
        }
        try:
            if state in self.active_states:
                self.logger.debug("State is valid, fetching token...")
                return await self.requester.request(HTTPMethod.POST, url, data=payload,
                                                    oauth=True, client_id=self.client_id,
                                                    client_secret=self.client_secret)
            else:
                raise InvalidStateException("State is invalid")
        except Exception as ex:
            self.logger.exception(f"Error fetching token. Reason: {ex}")

    async def refresh_token(self, token: dict) -> dict:
        """Refreshes an authentication token

        Args:
            token (dict): The authentication token to refresh

        Raises:
            Exception: Error refreshing token. Reason: response

        Returns:
            dict: The refreshed authentication token
        """
        data = {
            "grant_type": "refresh_token",
            "refresh_token": token["refresh_token"],
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "Content-Type": "application/x-www-form-urlencoded",
        }
        try:
            membership_id = token["membership_id"]
            self.logger.info(f"Refreshing token for {membership_id}...")
            return await self.requester.request(HTTPMethod.POST, self.TOKEN_URL, data=data, refresh=True)
        except Exception as ex:
            self.logger.exception(f"Error refreshing token. Reason: {ex}")
