from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class Tokens:
    """Tokens endpoints."""
    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.TOKENS_URL = "https://www.bungie.net/Platform/Tokens/"

    async def ForceDropsRepair(self, token: dict) -> dict:
        """Twitch Drops self-repair function - scans twitch for drops not marked as fulfilled and resyncs them.

        Args:
            token (dict): The token to use for authentication.

        Returns:
            dict: Wether or not the repair was successful.
        """
        try:
            self.logger.info("Forcing drops repair...")
            url = self.TOKENS_URL + "Partner/ForceDropsRepair/"
            return await self.requester.request(method=HTTPMethod.POST, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def ClaimPartnerOffer(
        self,
        token: dict,
        partner_offer_id: str,
        bungie_net_membership_id: int,
        transaction_id: str
    ) -> dict:
        """Claim a partner offer as the authenticated user.

        Args:
            token (dict): The token to use for authentication.
            partnerOfferId (str): The partner offer id.
            bungieNetMembershipId (int): The bungie.net membership id.
            transactionId (str): The transaction id.

        Returns:
            dict: Wether or not the claim was successful.
        """
        try:
            self.logger.info("Claiming partner offer...")
            payload = {
                "PartnerOfferId": partner_offer_id,
                "BungieNetMembershipId": bungie_net_membership_id,
                "TransactionId": transaction_id
            }
            url = self.TOKENS_URL + "Partner/ClaimOffer/"
            return await self.requester.request(method=HTTPMethod.POST, url=url, access_token=token["access_token"], data=payload)
        except Exception as ex:
            self.logger.exception(ex)

    async def ApplyMissingPartnerOfferWithoutClaim(
        self,
        token: dict,
        partner_application_id: int,
        target_bnet_membership_id: int
    ) -> dict:
        """Apply a partner offer to the targeted user.
        This endpoint does not claim a new offer, but any already claimed offers will be applied to the game if not already.

        Args:
            token (dict): The token to use for authentication.
            partner_application_id (int): The partner application identifier.
            target_bnet_membership_id (int): The bungie.net user to apply missing offers to. If not self, elevated permissions are required.

        Returns:
            dict: Wether or not the application was successful.
        """
        try:
            self.logger.info("Applying missing partner offer...")
            url = self.TOKENS_URL + "Partner/ApplyMissingOffers/{}/{}/"
            url = url.format(partner_application_id, target_bnet_membership_id)
            return await self.requester.request(method=HTTPMethod.POST, url=url, access_token=token["access_token"], data={})
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPartnerOfferSkulHistory(
        self,
        token: dict,
        partner_application_id: int,
        target_bnet_membership_id: int
    ) -> dict:
        """Returns the partner sku and offer history of the targeted user.
        Elevated permissions are required to see users that are not yourself.

        Args:
            token (dict): The token to use for authentication.
            partner_application_id (int): The partner application identifier.
            target_bnet_membership_id (int): The bungie.net user to apply missing offers to. If not self, elevated permissions are required.

        Returns:
            dict: The partner skul and offer history of the targeted user.
        """
        try:
            self.logger.info("Getting partner offer skul history...")
            url = self.TOKENS_URL + "Partner/History/{}/{}/"
            url = url.format(partner_application_id, target_bnet_membership_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPartnerRewardHistory(
        self,
        token: dict,
        partner_application_id: int,
        target_bnet_membership_id: int
    ) -> dict:
        """Returns the partner rewards history of the targeted user, both partner offers and Twitch drops.

        Args:
            token (dict): The token to use for authentication.
            partner_application_id (int): The partner application identifier.
            target_bnet_membership_id (int): The bungie.net user to apply missing offers to. If not self, elevated permissions are required.

        Returns:
            dict: The partner rewards history of the targeted user.
        """
        try:
            self.logger.info("Getting partner reward history...")
            url = self.TOKENS_URL + "Partner/History/{}/Application/{}/"
            url = url.format(target_bnet_membership_id, partner_application_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetBungieRewardsForUser(self, token: dict, membership_id: int) -> dict:
        """Returns the bungie rewards for the targeted user.

        Args:
            token (dict): The token to use for authentication.
            membership_id (int): bungie.net user membership_id for requested user rewards.
                If not self, elevated permissions are required.

        Returns:
            dict: The bungie rewards for the targeted user.
        """
        try:
            self.logger.info("Getting bungie rewards for user {}...".format(membership_id))
            url = self.TOKENS_URL + "Rewards/GetRewardsForUser/{}/".format(membership_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetBungieRewardsForPlatformUser(
        self,
        token: dict,
        membership_id: int,
        membership_type: int
    ) -> dict:
        """Returns the bungie rewards for the targeted user when a platform membership Id and Type are used.

        Args:
            token (dict): The token to use for authentication.
            membership_id (int): The platform membership_id for requested user rewards. If not self, elevated permissions are required.
            membership_type (int): The target Destiny2 membership type.

        Returns:
            dict: The bungie rewards for the targeted user.
        """
        try:
            self.logger.info("Getting bungie rewards for platform user...")
            url = self.TOKENS_URL + "Rewards/GetRewardsForPlatformUser/{}/{}/"
            url = url.format(membership_id, membership_type)
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetBungieRewardsList(self) -> dict:
        """Returns a list of the current bungie rewards

        Returns:
            dict: The list of the current bungie rewards
        """
        try:
            self.logger.info("Getting current bungie rewards list...")
            url = self.TOKENS_URL + "Rewards/GetBungieRewardsList/"
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)
