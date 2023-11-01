from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class Base:
    """Base endpoints."""
    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.BASE_URL = "https://www.bungie.net/Platform/"

    async def GetAvailableLocales(self) -> dict:
        """Returns a list of available localization cultures

        Returns:
            dict: List of available localization cultures
        """
        try:
            self.logger.info("Getting available locales...")
            url = self.BASE_URL + "GetAvailableLocales/"
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetCommonSettings(self) -> dict:
        """Get the common settings used by the Bungie.Net environment.

        Returns:
            dict: The common settings
        """
        try:
            self.logger.info("Getting common settings...")
            url = self.BASE_URL + "Settings/"
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetUserSystemOverrides(self) -> dict:
        """Get the user-specific system overrides that should be respected alongside common systems.

        Raises:
            Exception: Error getting user system overrides. Reason: response
        Returns:
            dict: The user-specific system overrides
        """
        try:
            self.logger.info("Getting user system overrides...")
            url = self.BASE_URL + "UserSystemOverrides/"
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetGlobalAlerts(self, include_streaming: bool = False) -> dict:
        """Gets any active global alert for display in the forum banners, help pages, etc.
        Usually used for DOC alerts.

        Args:
            include_streaming (bool, optional): Whether or not to include streaming alerts. Defaults to False.

        Returns:
            dict: The current global alerts
        """
        param_dict = {True: "true", False: "false"}
        try:
            self.logger.info("Getting global alerts...")
            url = self.BASE_URL + "GlobalAlerts/?includestreaming={}"
            url = url.format(param_dict[include_streaming])
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)
