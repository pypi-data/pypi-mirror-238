from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class App:
    """App endpoints."""
    def __init__(self, client_id, requester, logger):
        self.client_id = client_id
        self.requester: Requester = requester
        self.logger = logger
        self.APP_URL = "https://www.bungie.net/Platform/App/"

    async def GetApplicationApiUsage(
        self,
        token: dict,
        application_id: int,
        end: str,
        start: str
    ) -> dict:
        """Get API usage by application for time frame specified.
        You can go as far back as 30 days ago, and can ask for up to a 48 hour window of time in a single request.
        You must be authenticated with at least the ReadUserData permission to access this endpoint.

        Args:
            token (dict): The authentication token
            application_id (int, optional): async defaults to the client id in the .env file.
            end (str, optional): End time for query. Use the format YYYY-MM-DD. Goes to now if not specified.
            start (str, optional): Start time for query. Use the format YYYY-MM-DD. Goes to 24 hours ago if not specified.

        Returns:
            dict: The application api usage
        """
        if end and start:
            query = "?end={}&start={}".format(end, start)
        elif start:
            query = "?start={}".format(end)
        elif end:
            query = "?end={}".format(start)
        else:
            query = ""
        try:
            self.logger.info("Fetching application api usage...")
            url = self.APP_URL + "ApplicationApiUsage/{}/{}"
            url = url.format(application_id, query)
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetBungieApplications(self, token: dict) -> dict:
        """Get list of applications created by Bungie.

        Args:
            token (dict): The authentication token

        Returns:
            dict: The bungie applications
        """
        try:
            self.logger.info("Getting bungie applications...")
            url = self.APP_URL + "FirstPlay/"
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)
