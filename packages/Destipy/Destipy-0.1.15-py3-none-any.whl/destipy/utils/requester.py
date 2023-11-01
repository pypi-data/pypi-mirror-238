import asyncio
import base64
import http
import logging
import time
from typing import Optional

import aiohttp
from destipy.utils.error import DestipyRunTimeError, DestipyHTTPError

from destipy.utils.http_method import HTTPMethod


class Requester:
    """This class handles all the requests to the Bungie API."""
    def __init__(
        self,
        api_key: str,
        max_ratelimit_retries: int,
        logger: logging.Logger,
    ) -> None:
        self.api_key = api_key
        self.logger = logger
        self.max_ratelimit_retries = max_ratelimit_retries

    async def handle_ratelimit(
        self,
        response: aiohttp.ClientResponse,
        method: str,
        url: str,
        **kwargs
    ) -> None:
        """Handles the ratelimiting for the client."""

        if response.status != http.HTTPStatus.TOO_MANY_REQUESTS: # Too many requests
            retries = 0
            while response.status == http.HTTPStatus.TOO_MANY_REQUESTS:
                if retries < self.max_ratelimit_retries:
                    raise DestipyRunTimeError("Max rate limit retries reached.")
                # Get the time to wait from the response headers
                ratelimit_reset = int(response.headers["x-rateLimit-reset"])
                # Wait for the ratelimit to reset
                asyncio.sleep(ratelimit_reset)
                # Send the request again
                response = await self.request(method, url, **kwargs)
                retries+=1
        if response.content_type != "application/json":
            raise DestipyHTTPError(
                f"Wrong content type: {response.content_type}. You may being rate limited. \n {response.text}",
                response.status,
            )
        return response

    async def request(
        self,
        method: HTTPMethod,
        url: str,
        access_token: Optional[str] = None,
        data: Optional[dict] = None,
        oauth: Optional[bool] = False,
        refresh: Optional[bool] = False,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        **kwargs
    ) -> str:
        """Makes a request to the Bungie API."""
        # Set the headers for the generic request
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        # Set the headers for token request
        if oauth:
            encoded = base64.b64encode(f"{client_id}:{client_secret}"
                                       .encode("utf-8")).decode("utf-8")
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            headers["Authorization"] = f"Basic {encoded}"
        # Set header for token refreshing
        if refresh:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        # Set the authorization header if the access token is provided
        if access_token is not None:
            headers["Authorization"] = f"Bearer {access_token}"

        # Set the request body if it is provided
        if data is not None:
            if refresh or oauth:
                kwargs["data"] = data
            else:
                kwargs["json"] = data

        async with aiohttp.ClientSession() as session:
            taken_time = time.monotonic()
            # Make the request using the ClientSession.request method
            async with session.request(method.value, url, headers=headers, **kwargs) as response:
                response_time = time.monotonic() - taken_time
                if response.status != http.HTTPStatus.OK:
                    self.logger.warning(f"{method.value} {url} -> {response.status} {response.reason} ({response_time:.2f}s)")
                else:
                    self.logger.debug(f"{method.value} {url} -> {response.status} {response.reason} ({response_time:.2f}s)")
                response = await self.handle_ratelimit(response, method, url, **kwargs)

                if response.status == http.HTTPStatus.NO_CONTENT:
                    return {}
                # Return the response as a json. Provide the user the ability to handle the status code
                return await response.json()
             