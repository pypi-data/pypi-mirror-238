from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class Content:
    """Content endpoints."""
    def __init__(self, requester, logger):
        self.requester:Requester = requester
        self.logger = logger
        self.CONTENT_URL = "https://www.bungie.net/Platform/Content/"
        self.head_params = {True: "true", False: "false"}

    async def GetContentType(self, content_type: str) -> dict:
        """Gets an object describing a particular variant of content.

        Args:
            content_type (str): The type of content to get.

        Returns:
            dict: The content type.
        """
        try:
            self.logger.info(f"Getting content type for {content_type}...")
            url = self.CONTENT_URL + "GetContentType/{}/".format(content_type)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetContentById(self, content_id: int, locale: str, head: bool = False) -> dict:
        """Returns a content item referenced by id

        Args:
            content_id (int): The id of the content item
            locale (str): The locale to return the content in
            head (bool, optional): Whether to return the head or not. async defaults to False.

        Returns:
            dict: The content item
        """
        try:
            self.logger.info(f"Getting content by id {content_id}...")
            url = self.CONTENT_URL + "GetContentById/{}/{}/?head={}"
            url = url.format(content_id, locale, self.head_params[head])
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetContentByTagAndType(
        self,
        locale: str,
        tag: str,
        content_type: str,
        head: bool = False
    ) -> dict:
        """Returns the newest item that matches a given tag and Content Type.

        Args:
            locale (str): The locale to return the content in
            tag (str): The tag to search for
            content_type (str): The type of content to search for
            head (bool, optional): Whether to return the head or not. async defaults to False.

        Returns:
            dict: The content item
        """
        try:
            self.logger.info(f"Getting content by tag {tag} and type {content_type}...")
            url = self.CONTENT_URL + "GetContentByTagAndType/{}/{}/{}/?head={}"
            url = url.format(tag, content_type, locale, self.head_params[head])
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def SearchContentWithText(
        self,
        locale: str,
        search_text: str,
        c_type: str,
        current_page: int,
        source: str,
        tag: str,
        head: bool = False
    ) -> dict:
        """Gets content based on querystring information passed in. Provides basic search and text search capabilities.

        Args:
            locale (str): The locale to return the content in
            search_text (str): The text to search for
            c_type (str): The type of content to search for
            current_page (int): The current page of results
            source (str): The source of the content
            tag (str): The tag to search for
            head (bool, optional): Whether to return the head or not. async defaults to False.

        Returns:
            dict: The content item
        """
        try:
            self.logger.info(f"Searching for content with text {search_text}...")
            query_params = "?head={}&search_text={}&&ctype={}&current_page={}&source={}&tag={}".format(self.head_params[head], search_text, c_type, current_page, source, tag)
            url = self.CONTENT_URL + "SearchContentWithText/{}/{}"
            url = url.format(locale, query_params)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def SearchContentByTagAndType(
        self,
        tag: str,
        content_type: str,
        locale: str,
        current_page: int,
        items_per_page: int,
        head: bool = False
    ) -> dict:
        """Searches for Content Items that match the given Tag and Content Type.

        Args:
            tag (str): The tag to search for
            content_type (str): The type of content to search for
            locale (str): The locale to return the content in
            current_page (int): The current page of results
            items_per_page (int): The number of items to return per page
            head (bool, optional): Whether to return the head or not. async defaults to False.

        Returns:
            dict: The content item
        """
        try:
            self.logger.info(f"Searching for content with tag {tag} and type {content_type}...")
            query_params = "?head={}&current_page={}&itemsPerPage={}"
            query_params.format(self.head_params[head], current_page, items_per_page)
            url = self.CONTENT_URL + "SearchContentByTagAndType/{}/{}/{}/{}"
            url = url.format(tag, content_type, locale, query_params)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def SearchHelpArticles(self, search_text: str, size: str) -> dict:
        """Search for Help Articles.

        Args:
            search_text (str): The text to search for
            size (str): The size of the results to return

        Returns:
            dict: The help articles
        """
        try:
            self.logger.info(f"Searching for help articles with text {search_text}...")
            url = self.CONTENT_URL + "SearchHelpArticles/{}/{}/".format(search_text, size)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def RssNewsArticle(self, page_token: str) -> dict:
        """Returns a JSON string response that is the RSS feed for news articles.

        Args:
            page_token (str): Zero-based pagination token for paging through result sets.

        Returns:
            dict: The RSS feed for news articles
        """
        try:
            self.logger.info(f"Getting RSS news article for {page_token}...")
            url = self.CONTENT_URL + "Rss/NewsArticle/{}/".format(page_token)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)
