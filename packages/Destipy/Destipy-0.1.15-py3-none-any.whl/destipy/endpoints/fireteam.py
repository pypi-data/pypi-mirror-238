from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class Fireteam:
    """Fireteam endpoints."""
    def __init__(self, requester, logger):
        self.requester: Requester= requester
        self.logger = logger
        self.FIRETEAM_URL = "https://www.bungie.net/Platform/Fireteam/"

    async def GetActivePrivateClanFireteamCount(self, token: dict, group_id: int) -> dict:
        """Gets a count of all active non-public fireteams for the specified clan.
        Maximum value returned is 25.

        Args:
            token (dict): The token to use for authentication
            group_id (int): The group id of the clan.

        Returns:
            dict: The count of all active non-public fireteams for the specified clan.
        """
        try:
            self.logger.info("Getting active non-public fireteam count for {} for clan {}...".format(token["membership_id"], group_id))
            url = self.FIRETEAM_URL + "Clan/{}/ActiveCount/".format(group_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetAvailableClanFireteams(
        self,
        activity_type: int,
        date_range: int,
        group_id: int,
        page: int,
        platform: int,
        public_only: int,
        slot_filter: int,
        lang_filter: str = ""
    ) -> dict:
        """Gets a listing of all of this clan's fireteams that are have available slots.
        Caller is not checked for join criteria so caching is maximized.

        Args:
            activity_type (int): The activity type to filter by.
            date_range (int): The date range to grab available fireteams.
            group_id (int): The group id of the clan.
            page (int): Zero based page
            platform (int): The platform filter.
            public_only (int): Determines public/private filtering.
            slot_filter (int): Filters based on available slots
            lang_filter (str): An optional language filter.

        Returns:
            dict: The available clan fireteams.
        """
        try:
            self.logger.info("Getting available clan fireteams for clan {}...".format(group_id))
            url = self.FIRETEAM_URL + "Clan/{}/Available/{}/{}/{}/{}/{}/{}/?lang_filter={}".format(group_id, platform, activity_type, date_range, slot_filter, public_only, page, lang_filter)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def SearchPublicAvailableClanFireteams(
        self,
        token: dict,
        activity_type: int,
        date_range: int,
        page: int,
        platform: int,
        slot_filter: int,
        lang_filter: str = ""
    ) -> dict:
        """Gets a listing of all public fireteams starting now with open slots.
        Caller is not checked for join criteria so caching is maximized.

        Args:
            token (dict): The token to use for authentication
            activity_type (int): The activity type to filter by.
            date_range (int): The date range to grab available fireteams.
            page (int): Zero based page
            platform (int): The platform filter.
            slot_filter (int): Filters based on available slots
            lang_filter (str): An optional language filter.

        Raises:
            Exception: Error getting available fireteams. Reason: response

        Returns:
            dict: The available public fireteams.
        """
        try:
            self.logger.info("Getting available clan fireteams...")
            url = self.FIRETEAM_URL + "Search/Available/{}/{}/{}/{}/?lang_filter={}"
            url = url.format(platform, activity_type, date_range, slot_filter, page, lang_filter)
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetMyClanFireteams(
        self,
        token: dict,
        group_id: int,
        include_closed: bool,
        page: int,
        platform: int,
        group_filter: bool,
        lang_filter: str = ""
    ) -> dict:
        """Gets a listing of all fireteams that caller is an applicant, a member, or an alternate of.

        Args:
            token (dict): The token to use for authentication
            group_id (int): The group id of the clan. (This parameter is ignored unless the optional query parameter group_filter is true).
            include_closed (bool): If true, return fireteams that have been closed.
            page (int): Deprecated parameter, ignored.
            platform (int): The platform filter.
            group_filter (bool): If true, filter by clan. Otherwise, ignore the clan and show all of the user's fireteams.
            lang_filter (str, optional): An optional language filter.

        Returns:
            dict: The fireteams that caller is an applicant, a member, or an alternate of.
        """
        bool_dict = {True: "true", False: "false"}
        try:
            self.logger.info("Getting own clan fireteams for {} for clan {}...".format(token["membership_id"], group_id))
            url = self.FIRETEAM_URL + "Clan/{}/My/{}/{}/{}/?lang_filter={}&group_filter={}"
            url = url.format(group_id, platform, include_closed, page, lang_filter, bool_dict[group_filter])
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetClanFireteam(
        self,
        token: dict,
        fireteam_id: int,
        group_id: int
    ) -> dict:
        """Gets a specific fireteam.

        Args:
            token (dict): The token to use for authentication
            fireteam_id (int): The unique id of the fireteam.
            group_id (int): The group id of the clan.

        Returns:
            dict: The specific fireteam.
        """
        try:
            self.logger.info("Getting fireteam {} for clan {}...".format(fireteam_id, group_id))
            url = self.FIRETEAM_URL + "Clan/{}/Summary/{}/".format(group_id, fireteam_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)
