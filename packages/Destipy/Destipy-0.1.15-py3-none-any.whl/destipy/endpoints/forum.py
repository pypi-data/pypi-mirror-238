from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class Forum:
    """Forum endpoints."""
    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.FORUM_URL = "https://www.bungie.net/Platform/Forum/"

    async def GetTopicsPaged(
        self,
        category_filter: int,
        page: int,
        page_size: int,
        quick_date: int,
        sort: int,
        group: int = 0,
        locales: str = "en",
        tag_string: str = "",
    ) -> dict:
        """Get topics from any forum.

        Args:
            category_filter (int): The category filter
            page (int): Zero paged page number
            page_size (int): Unused
            quick_date (int): The date filter.
            sort (int): The sort mode
            group (int, optional): The group, if any. Defaults to 0.
            locales (str, optional): Comma separated list of locales posts must match to return in the result list. Defaults to "en".
            tag_string (str, optional): The tags to search, if any. Defaults to "".

        Returns:
            dict: The forum topics.
        """
        try:
            self.logger.info("Getting topics from forum...")
            url = self.FORUM_URL + "GetTopicsPages/{}/{}/{}/{}/{}/{}/?locales={}&tagstring={}"
            url = url.format(page, page_size, group, sort, quick_date, category_filter, locales, tag_string)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetCoreTopicsPaged(
        self,
        category_filter: int,
        page: int,
        quick_date: int,
        sort: int,
        locales: str = "en",
    ) -> dict:
        """Gets a listing of all topics marked as part of the core group.

        Args:
            category_filter (int): The category filter
            page (int): Zero paged page number
            quick_date (int): The date filter.
            sort (int): The sort mode
            locales (str, optional): Comma separated list of locales posts must match to return in the result list. Defaults to "en".

        Returns:
            dict: The forum core topics.
        """
        try:
            self.logger.info("Getting core topics from forum...")
            url = self.FORUM_URL + "GetCoreTopicsPaged/{}/{}/{}/{}/?locales={}"
            url = url.format(page, sort, quick_date, category_filter, locales)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPostsThreadedPaged(
        self,
        get_parent_post: bool,
        page: int,
        page_size: int,
        parent_post_id: int,
        reply_size: int,
        root_thread_mode: bool,
        sort_mode: int,
        show_banned: str = "",
    ) -> dict:
        """_summary_

        Args:
            get_parent_post (bool): If true, the parent post will be returned as the first post in the thread.
            page (int): Zero paged page number
            page_size (int): The page size.
            parent_post_id (int): The parent post id.
            reply_size (int): The number of replies to return.
            root_thread_mode (bool): If true, the root post will be returned as the first post in the thread.
            sort_mode (int): The sort mode.
            show_banned (str, optional): If this value is not null or empty, banned posts are requested to be returned.
                Defaults to "".

        Returns:
            dict: The thread of posts.
        """
        try:
            self.logger.info("Getting thread of post...")
            url = self.FORUM_URL + "GetPostsThreadedPaged/{}/{}/{}/{}/{}/{}/{}/?showbanned={}"
            url = url.format(parent_post_id, page, page_size, reply_size, get_parent_post, root_thread_mode, sort_mode, show_banned)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPostsThreadedPagedFromChild(
        self,
        child_post_id: int,
        page: int,
        page_size: int,
        reply_size: int,
        root_thread_mode: bool,
        sort_mode: int,
        show_banned: str = "",
    ) -> dict:
        """Returns a thread of posts starting at the topicId of the input childPostId, optionally returning replies to those posts as well as the original parent.

        Args:
            child_post_id (int): The child post id.
            page (int): Zero paged page number
            page_size (int): The page size.
            reply_size (int): The number of replies to return.
            root_thread_mode (bool): If true, the root post will be returned as the first post in the thread.
            sort_mode (int): The sort mode.
            show_banned (str, optional): If this value is not null or empty, banned posts are requested to be returned. Defaults to "".

        Returns:
            dict: The thread of posts.
        """
        try:
            self.logger.info("Getting thread of post...")
            url = self.FORUM_URL + "GetPostsThreadedPagedFromChild/{}/{}/{}/{}/{}/{}/?showbanned={}"
            url = url.format(child_post_id, page, page_size, reply_size, root_thread_mode, sort_mode, show_banned)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPostAndParent(self, child_post_id: int, show_banned: str = "") -> dict:
        """Returns the post specified and its immediate parent.

        Args:
            child_post_id (int): The child post id.
            showBanned (str, optional): If this value is not null or empty, banned posts are requested to be returned.
            Defaults to "".

        Returns:
            dict: The post and parent.
        """
        try:
            self.logger.info("Getting post and parent...")
            url = self.FORUM_URL + "GetPostAndParent/{}/?showbanned={}"
            url = url.format(child_post_id, show_banned)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPostAndParentAwaitingApproval(
        self,
        child_post_id: int,
        show_banned: str = "",
    ) -> dict:
        """Returns the post specified and its immediate parent of posts that are awaiting approval.

        Args:
            child_post_id (int): The child post id.
            showBanned (str, optional): If this value is not null or empty, banned posts are requested to be returned. Defaults to "".

        Returns:
            dict: The post and parent.
        """
        try:
            self.logger.info("Getting post and parent awaiting approval...")
            url = self.FORUM_URL + "GetPostAndParentAwaitingApproval/{}/?showbanned={}"
            url = url.format(child_post_id, show_banned)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetTopicForContent(self, content_id: int) -> dict:
        """Gets the post Id for the given content item's comments, if it exists.

        Args:
            content_id (int): The content id.

        Returns:
            dict: The topic for content.
        """
        try:
            self.logger.info("Getting topic for content...")
            url = self.FORUM_URL + "GetTopicForContent/{}".format(content_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetForumTagSuggestion(self, partial_tag: str) -> dict:
        """Gets tag suggestions based on partial text entry, matching them with other tags previously used in the forums.

        Args:
            partial_tag (str): The partial tag input to generate suggestions from.

        Returns:
            dict: The forum tag suggestion.
        """
        try:
            self.logger.info("Getting forum tag suggestion...")
            url = self.FORUM_URL + "GetForumTagSuggestions/?partialtag={}".format(partial_tag)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPoll(self, topic_id: int) -> dict:
        """Gets the specified forum poll.

        Args:
            topic_id (int): The post id of the topic that has the poll.

        Returns:
           dict: The poll.
        """
        try:
            self.logger.info("Getting poll from topic {}...".format(topic_id))
            url = self.FORUM_URL + "Poll/{}/".format(topic_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetRecruitmentThreadSummaries(self, body: list) -> dict:
        """Allows the caller to get a list of to 25 recruitment thread summary information objects.

        Args:
            body (list): *

        Returns:
            dict: The forum recruitment details.
        """
        try:
            self.logger.info("Getting recruitment thread summaries...")
            payload = {
                "body": body
            }
            url = self.FORUM_URL + "Recruit/Summaries/"
            return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload)
        except Exception as ex:
            self.logger.exception(ex)
