import logging
import logging.handlers

from .endpoints.app import App
from .endpoints.base import Base
from .endpoints.community_content import CommunityContent
from .endpoints.content import Content
from .endpoints.destiny2 import Destiny2
from .endpoints.fireteam import Fireteam
from .endpoints.forum import Forum
from .endpoints.group_v2 import GroupV2
from .endpoints.social import Social
from .endpoints.tokens import Tokens
from .endpoints.trending import Trending
from .endpoints.user import User
from .manifest import Manifest
from .oauth import OAuth
from .utils.requester import Requester


class DestinyClient():
    """This class is used to setup a client to interact with the Bungie API.
    To access the endpoints, use the given categories given in the documentation as attributes.

    Example:

        client = DestinyClient(<api_key>)

        user = await client.user.GetBungieNetUserById(<membership_id>)

        or

        client = DestinyClient(<api_key>)

        userEndpoints = client.user

        user = await userEndpoints.GetBungieNetUserById(<membership_id>)

    Args:
        api_key (str): The API key to use for authentication
        client_id (str, optional): The client ID to use for OAuth authentication. Defaults to "".
        client_secret (str, optional): The client secret to use for OAuth authentication. Defaults to "".
        redirect_uri (str, optional): The redirect URI to use for OAuth authentication. Defaults to "".
        max_retries (int, optional): The maximum number of retries to make when a request fails. Defaults to 3.
        max_ratelimit_retries (int, optional): The maximum number of retries to make when a request fails due to rate limiting. Defaults to 3.
        log_file (str, optional): The file to log to. Defaults to "logs/destipy.log".
        logger (optional): The logger to use. If none is given, a default logger with a TimedRotatingFileHandler wih backupCount of 7 is used.
        session (aiohttp.ClientSession, optional): The session to use for requests. If none is given, a new session is created. Defaults to None.
    """
    def __init__(
        self, api_key: str,
        client_id: str = "",
        client_secret: str = "",
        redirect_uri: str = "",
        max_ratelimit_retries: int = 3,
        log_file: str = "logs/destipy.log",
        logger = None,
    ) -> None:

        default_logger = logging.getLogger("Destipy")
        default_logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)-8s - %(name)s - %(message)s", datefmt="%H:%M:%S")
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename= log_file,
            when="midnight",
            backupCount=7
        )
        file_handler.setFormatter(formatter)
        if default_logger.hasHandlers():
            default_logger.handlers.clear()
        default_logger.addHandler(file_handler)
        self.logger = default_logger if logger is None else logger
        requester = Requester(api_key, max_ratelimit_retries, self.logger)
        self.app: App = App(client_id, requester, self.logger)
        self.base: Base = Base(requester, self.logger)
        self.community_content: CommunityContent = CommunityContent(requester, self.logger)
        self.content: Content = Content(requester, self.logger)
        self.destiny2: Destiny2 = Destiny2(requester, self.logger)
        self.fireteam: Fireteam = Fireteam(requester, self.logger)
        self.forum: Forum = Forum(requester, self.logger)
        self.group_v2: GroupV2 = GroupV2(requester, self.logger)
        self.manifest: Manifest = Manifest(self.destiny2)
        self.oauth: OAuth = OAuth(client_id, client_secret, requester, redirect_uri, self.logger)
        self.social: Social = Social(requester, self.logger)
        self.tokens: Tokens = Tokens(requester, self.logger)
        self.trending: Trending = Trending(requester, self.logger)
        self.user: User = User(requester, self.logger)

    # Source = https://github.com/jgayfer/pydest/blob/master/pydest/pydest.py
    async def decode_hash(self, hash_id, definition, language="en"):
        """Get the corresponding static info for an item given it's hash value from the Manifest
        Args:
            hash_id:
                The unique identifier of the entity to decode
            definition:
                The type of entity to be decoded (ex. 'DestinyClassDefinition')
            language (optional):
                The language to use when retrieving results from the Manifest. Defaults to 'en'
        Returns:
            dict: json corresponding to the given hash_id and definition
        Raises:
            DestipyException
        """
        return await self.manifest.decode_hash(hash_id, definition, language)

    # Source = https://github.com/jgayfer/pydest/blob/master/pydest/pydest.py
    async def update_manifest(self, language='en'):
        """Update the manifest if there is a newer version available
        Args:
            language [optional]:
                The language corresponding to the manifest to update. Defaults to 'en'
        """
        await self.manifest.update_manifest(language)
