from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class User:
    """User endpoints."""
    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.USER_URL = "https://www.bungie.net/Platform/User/"

    async def GetBungieNetUserById(self, membership_id: int) -> dict:
        """Loads a bungienet user by membership id.

        Args:
            membership_id (int): The requested Bungie.net membership id.

        Returns:
            dict: The user data
        """
        try:
            self.logger.info(f"Getting bungie.net user by id for {membership_id}...")
            url = self.USER_URL + "GetBungieNetUserById/{}/".format(membership_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetSanitizedPlatformDisplayNames(self, membership_id: int) -> dict:
        """Gets a list of all display names linked to this membership id but sanitized (profanity filtered). 
        Obeys all visibility rules of calling user and is heavily cached.

        Args:
            membership_id (int): The requested membership id to load.

        Returns:
            dict: The sanitized platform display names
        """
        try:
            self.logger.info(f"Getting sanitized platform display names for {membership_id}...")
            url = self.USER_URL + "GetSanitizedPlatformDisplayNames/{}/".format(membership_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetCredentialTypesForTargetAccount(self, token: dict, membership_id: int) -> dict:
        """Returns a list of credential types attached to the requested account

        Args:
            token (dict): OAuth token to use for authentication
            membership_id (int): The user's membership id

        Returns:
            dict: The credential types
        """
        try:
            self.logger.info("Getting credential types for target account for {membership_id}...")
            url = self.USER_URL + "GetCredentialTypesForTargetAccount/{}/".format(membership_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetAvailableThemes(self) -> dict:
        """Returns a list of all available user themes.

        Returns:
            dict: The available themes
        """
        try:
            self.logger.info("Getting available themes...")
            url = self.USER_URL + "GetAvailableThemes/"
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetMembershipDataById(self, membership_id: int, membership_type: int) -> dict:
        """Returns a list of accounts associated with the supplied membership ID and membership type.
        This will include all linked accounts (even when hidden) if supplied credentials permit it.

        Args:
            membership_id (int): The membership ID of the target user.
            membership_type (int): Type of the supplied membership ID
            (See Bungie.SharedDefinitions.MembershipType. in the API documentation)

        Returns:
            dict: The membership data
        """
        try:
            self.logger.info(f"Getting membership data by id for {membership_id}...")
            url = self.USER_URL + "GetMembershipsById/{}/{}/"
            url = url.format(membership_id,membership_type)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetMembershipDataForCurrentUser(self, token: dict) -> dict:
        """Returns a list of accounts associated with signed in user.
        This is useful for OAuth implementations that do not give you access to the token response.

        Args:
            token (dict): OAuth token to use for authentication

        Returns:
            dict: The user data
        """
        try:
            self.logger.info(f"Getting membership data for current user for {token['membership_id']}...")
            url = self.USER_URL + "GetMembershipsForCurrentUser/"
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetMembershipFromHardLinkedCredential(
        self,
        credential: str,
        credential_type: int
    ) -> dict:
        """Gets any hard linked membership given a credential.
        Only works for credentials that are public (just SteamID64 right now).
        Cross Save aware.

        Args:
            credential (str): The credential to look up. Must be a valid SteamID64.
            credential_type (int): The credential type.
            (See Bungie.SharedDefinitions.CredentialType in the API documentation)

        Returns:
            dict: The membership data
        """
        try:
            self.logger.info(f"Getting membership from hard linked credential {credential}...")
            url = self.USER_URL + "GetMembershipFromHardLinkedCredential/{}/{}/"
            url = url.format(credential_type, credential)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def SearchByGlobalNamePost(self, page:int, display_name_prefix: str) -> dict:
        """Given the prefix of a global display name, returns all users who share that name.

        Args:
            page (int): The zero-based page of results you desire.
            display_name_prefix (str): The display name prefix you're looking for.

        Returns:
        dict: The users
        """
        try:
            self.logger.info("Searching by global name post...")
            payload = {"display_name_prefix": display_name_prefix}
            url = self.USER_URL + "Search/GlobalName/{}/".format(page)
            return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload)
        except Exception as ex:
            self.logger.exception(ex)
            