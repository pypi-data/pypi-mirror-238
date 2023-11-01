from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class CommunityContent:
    """Community content endpoints."""
    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.COMMUNITY_CONTENT_URL = "https://www.bungie.net/Platform/CommunityContent/"
        self.BASE_URL = "https://www.bungie.net/Platform/"

    async def GetCommunityContent(self, media_filter: int, page: int, sort: int) -> dict:
        """Returns community content.

        Args:
            media_filter (int): The type of media to get
            page (int): Zero based page
            sort (int): The sort mode

        Returns:
            dict: Community content
        """
        try:
            self.logger.info("Getting community content...")
            url = self.BASE_URL + "CommunityContent/Get/{}/{}/{}"
            url = url.format(media_filter, page, sort)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)
