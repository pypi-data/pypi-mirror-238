from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class Trending:
    """Trending endpoints."""
    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.TRENDING_URL = "https://www.bungie.net/Platform/Trending/"

    async def GetTrendingCategories(self) -> dict:
        """Returns trending items for Bungie.net, collapsed into the first page of items per category.
        For pagination within a category, call GetTrendingCategory.

        Returns:
            dict: The trending categories.
        """
        try:
            self.logger.info("Getting trending categories...")
            url = self.TRENDING_URL + "Categories/"
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetTrendingCategory(self, category_id: str, page_number: int) -> dict:
        """Returns paginated lists of trending items for a category.

        Args:
            category_id (str): The ID of the category for whom you want additional results.
            page_number (int): The page # of results to return.

        Returns:
            dict: The trending category.
        """
        try:
            self.logger.info("Getting trending category {}...".format(category_id))
            url = self.TRENDING_URL + "Category/{}/{}/".format(category_id, page_number)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetTrendingEntryDetail(self, identifier: str, trending_entry_type: int) -> dict:
        """Returns the detailed results for a specific trending entry.
        Note that trending entries are uniquely identified by a combination of *both* the TrendingEntryType *and* the identifier:
        the identifier alone is not guaranteed to be globally unique.

        Args:
            identifier (str): The identifier for the entity to be returned.
            trending_entry_type (int): The type of entity to be returned. / The known entity types that you can have returned from Trending.

        Returns:
            dict: The trending entry detail.
        """
        try:
            self.logger.info("Getting trending entry detail for {} of type {}...".format(identifier, trending_entry_type))
            url = self.TRENDING_URL + "Details/{}/{}/".format(trending_entry_type, identifier)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)
