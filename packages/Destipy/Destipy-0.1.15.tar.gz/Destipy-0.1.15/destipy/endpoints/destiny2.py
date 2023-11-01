from datetime import datetime

from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class Destiny2:
    """Destiny 2 endpoints."""
    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.DESTINY2_URL = "https://www.bungie.net/Platform/Destiny2/"

    async def GetDestinyManifest(self) -> dict:
        """Returns the current version of the manifest as a json object.

        Returns:
            dict: The manifest as a json object.
        """
        try:
            self.logger.info("Getting Destiny Manifest...")
            url = self.DESTINY2_URL + "Manifest/"
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetDestinyEntitydefinition(
        self,
        token: dict,
        entity_type: str,
        hash_identifier: int
    ) -> dict:
        """Returns the static async definition of an entity of the given Type and hash identifier.
        Examine the API Documentation for the Type Names of entities that have their own async definitions.
        Note that the return type will always *inherit from* Destinyasync definition, but the specific type returned will be the requested entity type if it can be found.
        Please don't use this as a chatty alternative to the Manifest database if you require large sets of data, but for simple and one-off accesses this should be handy.

        Args:
            token (dict): The token to use for authentication.
            entity_type (str): The type of entity for whom you would like results.
                These correspond to the entity's async definition contract name.
                For instance, if you are looking for items, this property should be 'DestinyInventoryItemasync definition'.
                PREVIEW: This endpoint is still in beta, and may experience rough edges.
                The schema is tentatively in final form, but there may be bugs that prevent desirable operation.
            hash_identifier (int): The hash identifier for the specific Entity you want returned.

        Returns:
            dict: The Destiny Entity async definition as a json object.
        """
        try:
            self.logger.info("Getting Destiny Entity async definition for hash {}...".format(hash_identifier))
            url = self.DESTINY2_URL + "Manifest/{}/{}/"
            url = url.format(entity_type, hash_identifier)
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def SearchDestinyPlayerByBungieName(
        self,
        membership_type: int,
        display_name: str,
        display_name_code: str
    ) -> dict:
        """Returns a list of Destiny memberships given a global Bungie Display Name.
        This method will hide overridden memberships due to cross save.

        Args:
            membership_type (int): A valid non-BungieNet membership type, or All.
                Indicates which memberships to return.
                You probably want this set to All.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.membership_type.
            display_name (str): The display name of the user whose membership you wish to look up.
            display_name_code (str): The display name code of the user whose membership you wish to look up.

        Returns:
            dict: The list of Destiny memberships of the specific membership type.
        """
        try:
            self.logger.info("Searching for Destiny Player by Bungie Name...")
            payload = {
                "displayName": display_name,
                "displayNameCode": display_name_code
            }
            url = self.DESTINY2_URL + "SearchDestinyPlayerByBungieName/{}/"
            url = url.format(membership_type)
            return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetLinkedProfiles(
        self,
        token: dict,
        membership_id: int,
        membership_type: int,
        get_all_memberships: bool = False
    ) -> dict:
        """Returns a summary information about all profiles linked to the requesting membership type/membership ID that have valid Destiny information.
        The passed-in Membership Type/Membership ID may be a Bungie.Net membership or a Destiny membership.
        It only returns the minimal amount of data to begin making more substantive requests, but will hopefully serve as a useful alternative to UserServices for people who just care about Destiny data.
        Note that it will only return linked accounts whose linkages you are allowed to view.

        Args:
            token (dict): The token to use for authentication.
            membership_id (int): The ID of the membership whose linked Destiny accounts you want returned.
                Make sure your membership ID matches its Membership Type: don't pass us a PSN membership ID and the XBox membership type, it's not going to work!
            membership_type (int): The type for the membership whose linked Destiny accounts you want returned.
            get_all_memberships (bool, optional): If set to 'true', all memberships regardless of whether they're obscured by overrides will be returned.
                Normal privacy restrictions on account linking will still apply no matter what.
                Defaults to False.

        Returns:
            dict: The linked profiles.
        """
        params_dict = {False: "false", True: "true"}
        try:
            self.logger.info("Getting linked profiles for member {}...".format(membership_id))
            url = self.DESTINY2_URL + "{}/Profile/{}/LinkedProfiles/?get_all_memberships={}"
            url = url.format(membership_type, membership_id, params_dict[get_all_memberships])
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetProfile(
        self,
        destiny_membership_id: int,
        membership_type: int,
        components: list[int]
    ) -> dict:
        """Returns Destiny Profile information for the supplied membership.

        Args:
            destiny_membership_id (int): Destiny membership ID.
            membership_type (int): A valid non-BungieNet membership type.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.membership_type.
            components (list): A comma separated list of components to return (as strings or numeric values).
                See the DestinyComponentType enum for valid components to request.
                You must request at least one component to receive results.

        Returns:
            dict: The Destiny Profile information
        """
        try:
            self.logger.info("Getting profile components information for member {}...".format(destiny_membership_id))
            url = url = self.DESTINY2_URL + '{}/Profile/{}/?components={}'
            url = url.format(membership_type, destiny_membership_id, ','.join([str(i) for i in components]))
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetCharacter(
        self,
        token: dict,
        character_id: int,
        destiny_membership_id: int,
        membership_type: int,
        components: list[int]
    ) -> dict:
        """Returns character information for the supplied character.

        Args:
            token (dict): The token to use for authentication.
            character_id (int): The ID of the character.
            destiny_membership_id (int): Destiny membership ID.
            membership_type (int): A valid non-BungieNet membership type.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.membership_type.
            components (list): A comma separated list of components to return (as strings or numeric values).
                See the DestinyComponentType enum for valid components to request.
                You must request at least one component to receive results.

        Returns:
            dict: The character information.
        """
        try:
            self.logger.info("Getting character {} of account {}...".format(character_id, destiny_membership_id))
            url = self.DESTINY2_URL + "{}/Profile/{}/Character/{}/?components={}"
            url = url.format(membership_type, destiny_membership_id, character_id, ','.join([str(i) for i in components]))
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetClanWeeklyRewardState(self, group_id: int) -> dict:
        """Returns information on the weekly clan rewards and if the clan has exarned them or not.
        Note that this will always report rewards as not redeemed.

        Args:
            group_id (int): A valid group id of clan.

        Returns:
            dict: The clan weekly reward state.
        """
        try:
            self.logger.info("Getting clan weekly reward state of clan {}...".format(group_id))
            url = self.DESTINY2_URL + "Clan/{}/WeeklyRewardState/".format(group_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetClanBannerSource(self) -> dict:
        """Returns the dictionary of values for the Clan Banner.

        Returns:
            dict: The clan banner source.
        """
        try:
            self.logger.info("Getting clan banner source...")
            url = self.DESTINY2_URL + "Clan/GetAvailableBanners/"
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetItem(
        self,
        destiny_membership_id: int,
        itemInstanceId: int,
        membership_type: int,
        components: list[int]
    ) -> dict:
        """Retrieve the details of an instanced Destiny Item.
        An instanced Destiny item is one with an ItemInstanceId.
        Non-instanced items, such as materials, have no useful instance-specific details and thus are not queryable here.

        Args:
            destiny_membership_id (int): The membership ID of the destiny profile.
            itemInstanceId (int): The Instance ID of the destiny item.
            membership_type (int): A valid non-BungieNet membership type.
            components (list): A comma separated list of components to return (as strings or numeric values).
                See the DestinyComponentType enum for valid components to request.
                You must request at least one component to receive results.

        Returns:
            dict: The instanced item information.
        """
        try:
            self.logger.info("Getting item details of instance {} for account {}...".format(itemInstanceId, destiny_membership_id))
            url = self.DESTINY2_URL + "{}/Profile/{}/Item/{}/?components={}"
            url = url.format(membership_type, destiny_membership_id, itemInstanceId, ','.join([str(i) for i in components]))
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetVendors(
        self,
        token: dict,
        character_id: int,
        destiny_membership_id: int,
        membership_type: int,
        components: list[int],
        filter: int = 0
    ) -> dict:
        """Get currently available vendors from the list of vendors that can possibly have rotating inventory.
        Note that this does not include things like preview vendors and vendors-as-kiosks, neither of whom have rotating/dynamic inventories.
        Use their definitions as-is for those.

        Args:
            token (dict): The token to use for authentication.
            character_id (int): The Destiny Character ID of the character whom we're getting vendor info.
            destiny_membership_id (int): Destiny membership ID of another user.
            membership_type (int): A valid non-BungieNet membership type.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.membership_type.
            components (list): A comma separated list of components to return (as strings or numeric values).
                See the DestinyComponentType enum for valid components to request.
                You must request at least one component to receive results.
            filter (int, optional): The filter of what vendors and items to return, if any.
                Indicates the type of filter to apply to Vendor results
                Defaults to 0 (All).

        Returns:
            dict: The vendor information.
        """
        try:
            self.logger.info("Getting vendor details for character {} of account {}...".format(character_id, destiny_membership_id))
            url = self.DESTINY2_URL + "{}/Profile/{}/Character/{}/Vendors/?components={}&filter={}"
            url = url.format(membership_type, destiny_membership_id, character_id, ','.join([str(i) for i in components]), filter)
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetVendor(
        self,
        token: dict,
        character_id: int,
        destiny_membership_id: int,
        membership_type: int,
        vendor_hash: int,
        components: list[int]
    ) -> dict:
        """Get the details of a specific Vendor.

        Args:
            token (dict): The token to use for authentication.
            character_id (int): The Destiny Character ID of the character whom we're getting vendor info.
            destiny_membership_id (int): Destiny membership ID of another user. You may be denied.
            membership_type (int): A valid non-BungieNet membership type.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.membership_type.
            vendor_hash (int): The Hash identifier of the Vendor to be returned.
            components (list): A comma separated list of components to return (as strings or numeric values).
                See the DestinyComponentType enum for valid components to request.
                You must request at least one component to receive results.

        Returns:
            dict: The vendor information.
        """
        try:
            self.logger.info("Getting vendor details of vendor_hash {}...".format(vendor_hash))
            url = self.DESTINY2_URL + "{}/Profile/{}/Character/{}/Vendors/{}/?components={}"
            url = url.format(membership_type, destiny_membership_id, character_id, vendor_hash, ','.join([str(i) for i in components]))
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPublicVendors(self, components: list[int]) -> dict:
        """*PREVIEW*
        Get items available from vendors where the vendors have items for sale that are common for everyone.
        If any portion of the Vendor's available inventory is character or account specific, we will be unable to return their data from this endpoint due to the way that available inventory is computed.
        As I am often guilty of saying: 'It's a long story...'

        Args:
            components (list): A comma separated list of components to return (as strings or numeric values).
                See the DestinyComponentType enum for valid components to request.
                You must request at least one component to receive results.

        Returns:
            dict: A response containing all valid components for the public Vendors endpoint.<br /><br />
                It is a decisively smaller subset of data compared to what we can get when we know the specific user making the request.
                <br /><br /> If you want any of the other data - item details, whether or not you can buy it, etc... you'll have to call in the context of a character.
                I know, sad but true.
        """
        try:
            self.logger.info("Getting public vendor details with components {}...".format(components))
            url = self.DESTINY2_URL + "Vendors/?components={}"
            url = url.format(','.join([str(i) for i in components]))
        except Exception as ex:
            self.logger.exception(ex)

    async def GetCollectibleNodeDetails(
        self,
        character_id: int,
        collectible_presentation_node_hash: int,
        destiny_membership_id: int,
        membership_type: int,
        components: list[int]
    ) -> dict:
        """Given a Presentation Node that has Collectibles as direct descendants, this will return item details about those descendants in the context of the requesting character.

        Args:
            character_id (int): The Destiny Character ID of the character whom we're getting collectible details.
            collectible_presentation_node_hash (int): The hash identifier of the Presentation Node for whom we should return collectible details.
                Details will only be returned for collectibles that are direct descendants of this node.
            destiny_membership_id (int): Destiny membership ID of another user. You may be denied.
            membership_type (int): A valid non-BungieNet membership type.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.membership_type.
            components (list): A comma separated list of components to return (as strings or numeric values).
                See the DestinyComponentType enum for valid components to request.
                You must request at least one component to receive results.

        Returns:
            dict: The collectible node details.
        """
        try:
            self.logger.info("Getting collectible node details {} for character {} of account {}...".format(collectible_presentation_node_hash, character_id, destiny_membership_id))
            url = self.DESTINY2_URL + "{}/Profile/{}/Character/{}/Collectibles/{}/?components={}"
            url = url.format(membership_type, destiny_membership_id, character_id, collectible_presentation_node_hash, ','.join([str(i) for i in components]))
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def TransferItem(
        self,
        token: dict,
        item_reference_hash: int,
        stack_size: int,
        transfer_to_vault: bool,
        item_id: int,
        character_id: int,
        membership_type: int
        ) -> dict:
        """Transfer an item to/from your vault. You must have a valid Destiny account.
        You must also pass BOTH a reference AND an instance ID if it's an instanced item.

        Args:
            token (dict): The token to use for authentication.
            item_reference_hash (int): The hash identifier of the item to be transferred.
                Mapped to the DestinyInventoryItemDefinition.
            stack_size (int): *
            transfer_to_vault (bool): Wet or not to transfer to the vault.
            item_id (int): The instance ID of the item for this action request.
            character_id (int): The Destiny Character ID of the character whom is requesting the transfer.
            membership_type (int): A valid non-BungieNet membership type.

        Returns:
            dict: The transfer result.
        """
        try:
            self.logger.info("Transferring item {}... for ".format(item_id))
            payload = {
                "itemReferenceHash": item_reference_hash,
                "stackSize": stack_size,
                "transferToVault": transfer_to_vault,
                "itemId": item_id,
                "characterId": character_id,
                "membershipType": membership_type
            }
            url = self.DESTINY2_URL + "Actions/Items/TransferItem/"
            return await self.requester.request(method=HTTPMethod.POST, url=url, access_token=token["access_token"], data=payload)
        except Exception as ex:
            self.logger.exception(ex)

    async def PullFromPostmaster(
        self,
        token: dict,
        item_reference_hash: int,
        stack_size: int,
        item_id: int,
        character_id: int,
        membership_type: int
    ) -> dict:
        """Extract an item from the Postmaster, with whatever implications that may entail.
        You must have a valid Destiny account.
        You must also pass BOTH a reference AND an instance ID if it's an instanced item.


        Args:
            token (dict): The token to use for authentication.
            item_reference_hash (int): The hash identifier of the item to be transferred.
                Mapped to the DestinyInventoryItemDefinition.
            stack_size (int): *
            item_id (int): The instance ID of the item for this action request.
            character_id (int): The Destiny Character ID of the character whom is requesting the transfer.
            membership_type (int): A valid non-BungieNet membership type.

        Returns:
            dict: The pull result.
        """
        try:
            self.logger.info("Pulling item {} from postmaster..".format(item_id))
            payload = {
                "itemReferenceHash": item_reference_hash,
                "stackSize": stack_size,
                "itemId": item_id,
                "characterId": character_id,
                "membershipType": membership_type
            }
            url = self.DESTINY2_URL + "Actions/Items/PullFromPostmaster/"
            return await self.requester.request(method=HTTPMethod.POST, url=url, access_token=token["access_token"], data=payload)
        except Exception as ex:
            self.logger.exception(ex)

    async def EquipItem(
        self,
        token: dict,
        item_id: int,
        character_id: int,
        membership_type: int
    ) -> dict:
        """Equip an item.
        You must have a valid Destiny Account, and either be in a social space, in orbit, or offline.

        Args:
            token (dict): The token to use for authentication.
            item_id (int): The instance ID of the item to equip.
            character_id (int): The Destiny Character ID of the character whom is requesting the transfer.
            membership_type (int): A valid non-BungieNet membership type.

        Returns:
            dict: The equip result.
        """
        try:
            self.logger.info("Equipping item {}...".format(item_id))
            payload = {
                "itemId": item_id,
                "characterId": character_id,
                "membershipType": membership_type
            }
            url = self.DESTINY2_URL + "Actions/Items/EquipItem/"
            return await self.requester.request(method=HTTPMethod.POST, url=url, access_token=token["access_token"], data=payload)
        except Exception as ex:
            self.logger.exception(ex)

    async def EquipItems(
        self,
        token: dict,
        item_ids: list,
        character_id: int,
        membership_type: int
    ) -> dict:
        """Equip a list of items by itemInstanceIds.
        You must have a valid Destiny Account, and either be in a social space, in orbit, or offline.
        Any items not found on your character will be ignored.

        Args:
            token (dict): The token for authentication
            item_ids (list): The list of item instance IDs to equip.
            character_id (int): The Destiny Character ID of the character whom is requesting the transfer.
            membership_typ (int): A valid non-BungieNet membership type.

        Returns:
            dict: The result of the equip.
        """
        try:
            self.logger.info("Equipping items {}...".format(item_ids))
            payload = {
                "itemIds": item_ids,
                "characterId": character_id,
                "membershipType": membership_type
            }
            url = self.DESTINY2_URL + "Actions/Items/EquipItems/"
            return await self.requester.request(method=HTTPMethod.POST, url=url, access_token=token["access_token"], data=payload)
        except Exception as ex:
            self.logger.exception(ex)

    async def SetItemLockState(
        self,
        token: dict,
        state: bool,
        item_id: int,
        character_id: int,
        membership_type: int
    ) -> dict:
        """Set the Lock State for an instanced item.
        You must have a valid Destiny Account.

        Args:
            token (dict): The token to use for authentication
            state (bool): The desired state of the lock.
            item_id (int): The instance ID of the item to lock.
            character_id (int): The Destiny Character ID of the character whom is requesting the transfer.
            membership_type (int): A valid non-BungieNet membership type.

        Returns:
            dict: The result of the lock state change.
        """
        try:
            self.logger.info("Setting lock state for item {}...".format(item_id))
            payload = {
                "state": state,
                "itemId": item_id,
                "characterId": character_id,
                "membershipType": membership_type
            }
            url = self.DESTINY2_URL + "Actions/Items/SetLockState/"
            return await self.requester.request(method=HTTPMethod.POST, url=url, access_token=token["access_token"], data=payload)
        except Exception as ex:
            self.logger.exception(ex)

    async def SetQuestTrackedState(
        self,
        token: dict,
        state: bool,
        item_id: int,
        character_id: int,
        membership_type: int
    ) -> dict:
        """Set the Tracking State for an instanced item, if that item is a Quest or Bounty.
        You must have a valid Destiny Account. Yeah, it's an item.

        Args:
            token (dict): The token to use for authentication
            state (bool): The desired state of the lock.
            item_id (int): The instance ID of the item to lock.
            character_id (int): The Destiny Character ID of the character whom is requesting the transfer.
            membership_type (int): A valid non-BungieNet membership type.

        Returns:
            dict: The result of the lock state change.
        """
        try:
            self.logger.info("Setting tracking state for quest {}...".format(item_id))
            payload = {
                "state": state,
                "itemId": item_id,
                "characterId": character_id,
                "membershipType": membership_type
            }
            url = self.DESTINY2_URL + "Actions/Items/SetTrackedState/"
            return await self.requester.request(method=HTTPMethod.POST, url=url, access_token=token["access_token"], data=payload)
        except Exception as ex:
            self.logger.exception(ex)

    async def InsertSocketPlug(
        self,
        token: dict,
        action_token: str,
        item_instance_id: int,
        socket_index: int,
        socket_array_type: int,
        plug_item_hash: int,
        character_id: int,
        membership_type: int
    ) -> dict:
        """Insert a plug into a socketed item.
        I know how it sounds, but I assure you it's much more G-rated than you might be guessing.
        We haven't decided yet whether this will be able to insert plugs that have side effects, but if we do it will require special scope permission for an application attempting to do so.
        You must have a valid Destiny Account, and either be in a social space, in orbit, or offline.
        Request must include proof of permission for 'InsertPlugs' from the account owner.

        Args:
            token (dict): The token to use for authentication
            action_token (str): The action token provided by the AwaGetActionToken API call.
            item_instance_id (int): The instance ID of the item having a plug inserted.
                Only instanced items can have sockets.
            socket_index (int): The index into the socket array, which identifies the specific socket being operated on.
                We also need to know the socketArrayType in order to uniquely identify the socket.
                Don't point to or try to insert a plug into an infusion socket. It won't work.
            socket_array_type (int): This property, combined with the socketIndex, tells us which socket we are referring to (since operations can be performed on both Intrinsic and "default" sockets, and they occupy different arrays in the Inventory Item Definition).
                I know, I know.
                Don't give me that look.
            plug_item_hash (int): Plugs are never instanced (except in infusion).
                So with the hash alone, we should be able to:
                1) Infer whether the player actually needs to have the item, or if it's a reusable plug
                2) Perform any operation needed to use the Plug, including removing the plug item and running reward sheets.
            character_id (int): The character id of the character performing the action.
            membership_type (int): The membership type of the character performing the action.

        Returns:
            dict: The result of the plug insertion.
        """
        try:
            self.logger.info("Inserting plug {} into item {}...".format(plug_item_hash, item_instance_id))
            plug = {
                "socketIndex": socket_index,
                "socketArrayType": socket_array_type,
                "plugItemHash": plug_item_hash
            }
            payload = {
                "actionToken": action_token,
                "itemInstanceId": item_instance_id,
                "plug": plug,
                "characterId": character_id,
                "membershipType": membership_type
            }
            url = self.DESTINY2_URL + "Actions/Items/InsertSocketPlug/"
            return await self.requester.request(method=HTTPMethod.POST, url=url, access_token=token["access_token"], data=payload)
        except Exception as ex:
            self.logger.exception(ex)

    async def InsertSocketPlugFree(
        self,
        token: dict,
        socket_index: int,
        socket_array_type: int,
        plug_item_hash: int,
        item_instance_id: int,
        character_id: int,
        membership_type: int
    ) -> dict:
        """Insert a 'free' plug into an item's socket.
        This does not require 'Advanced Write Action' authorization and is available to 3rd-party apps, but will only work on 'free and reversible' socket actions (Perks, Armor Mods, Shaders, Ornaments, etc.).
        You must have a valid Destiny Account, and the character must either be in a social space, in orbit, or offline.

        Args:
            socket_index (int): The index into the socket array, which identifies the specific socket being operated on.
                We also need to know the socketArrayType in order to uniquely identify the socket.
                Don't point to or try to insert a plug into an infusion socket. It won't work.
            socket_array_type (int): This property, combined with the socketIndex, tells us which socket we are referring to (since operations can be performed on both Intrinsic and "default" sockets, and they occupy different arrays in the Inventory Item Definition).
                I know, I know.
                Don't give me that look.
            plug_item_hash (int): Plugs are never instanced (except in infusion).
                So with the hash alone, we should be able to:
                1) Infer whether the player actually needs to have the item, or if it's a reusable plug
                2) Perform any operation needed to use the Plug, including removing the plug item and running reward sheets.
            item_instance_id (int): The instance ID of the item having a plug inserted.
                Only instanced items can have sockets.
            character_id (int): The character id of the character performing the action.
            membership_type (int): The membership type of the character performing the action.

        Returns:
            dict: The result of the plug insertion.
        """
        try:
            self.logger.info("Inserting free plug {} into item {}...".format(plug_item_hash, item_instance_id))
            plug = {
                "socketIndex": socket_index,
                "socketArrayType": socket_array_type,
                "plugItemHash": plug_item_hash
            }
            payload = {
                "plug": plug,
                "itemInstanceId": item_instance_id,
                "characterId": character_id,
                "membershipType": membership_type
            }
            url = self.DESTINY2_URL + "Actions/Items/InsertSocketPlugFree/"
            return await self.requester.request(method=HTTPMethod.POST, url=url, access_token=token["access_token"], data=payload)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPostGameCarnageReport(self, activity_id: int) -> dict:
        """Gets the available post game carnage report for the activity ID.

        Args:
            activity_id (int): The ID of the activity whose PGCR is requested.

        Returns:
            dict: The post game carnage report.
        """
        try:
            self.logger.info("Getting post game carnage report for activity {}...".format(activity_id))
            url = self.DESTINY2_URL + "Stats/PostGameCarnageReport/{}/".format(activity_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def ReportOffensivePostGameCarnageReportPlayer(
        self,
        token: dict,
        activity_id: int,
        reason_category_hashes: list,
        reason_hashes: list,
        offending_character_id: int
    ) -> dict:
        """Report a player that you met in an activity that was exngaging in ToS-violating activities.
        Both you and the offending player must have played in the activity_id passed in.
        Please use this judiciously and only when you have strong suspicions of violation, pretty please.

        Args:
            token (dict): The token to use for authorization.
            activity_id (int): The ID of the activity where you ran into the brigand that you're reporting.
            reason_category_hashes (list): So you've decided to report someone instead of cursing them and their descendants.
                Well, okay then.
                This is the category or categories of infractions for which you are reporting the user.
                These are hash identifiers that map to DestinyReportReasonCategoryDefinition entries.
                Mapped to Destiny.Definitions.Reporting.DestinyReportReasonCategoryDefinition.
            reason_hashes (list): If applicable, provide a more specific reason(s) within the general category of problems provided by the reasonHash.
                This is also an identifier for a reason.
                All reasonHashes provided must be children of at least one the reasonCategoryHashes provided.
            offending_character_id (int): Within the PGCR provided when calling the Reporting endpoint, this should be the character ID of the user that you thought was violating terms of use.
                They must exist in the PGCR provided.
        Returns:
            dict: The post game carnage report.
        """
        try:
            self.logger.info("Reporting player...")
            payload = {
                "reasonCategoryHashes": reason_category_hashes,
                "reasonHashes": reason_hashes,
                "offendingCharacterId": offending_character_id
            }
            url = self.DESTINY2_URL + "Stats/PostGameCarnageReport/{}/Report/"
            url = url.format(activity_id)
            return await self.requester.request(method=HTTPMethod.POST, url=url, access_token=token["access_token"], data=payload)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetHistoricalStatsDefinition(self) -> dict:
        """Gets historical stats definitions.

        Returns:
            dict: The historical stats definition.
        """
        try:
            self.logger.info("Getting historical stats definition...")
            url = self.DESTINY2_URL + "Stats/Definition/"
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetClanLeaderboards(
        self,
        group_id: int,
        max_top: int,
        modes: list,
        stat_id: str = ""
    ) -> dict:
        """*PREVIEW*
        Gets leaderboards with the signed in user's friends and the supplied destiny_membership_id as the focus.
        PREVIEW: This endpoint is still in beta, and may experience rough edges.
        The schema is in final form, but there may be bugs that prevent desirable operation.

        Args:
            group_id (int): Group ID of the clan whose leaderboards you wish to fetch.
            max_top (int): Maximum number of top players to return.
                Use a large number to get entire leaderboard.
            modes (int): List of game modes for which to get leaderboards.
                See the documentation for DestinyActivityModeType for valid values, and pass in string representation, comma delimited.
            stat_id (str): ID of stat to return rather than returning all Leaderboard stats.

        Returns:
            dict: The clan leaderboards.
        """
        try:
            self.logger.info("Getting clan leaderboards for clan {}...".format(group_id))
            url = self.DESTINY2_URL + "Stats/Leaderboards/Clans/{}/?maxtop={}&modes={}&statid={}"
            url = url.format(group_id, max_top, ','.join(modes), stat_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetClanAggregateStats(self, group_id: int, modes: list) -> dict:
        """*PREVIEW*
        Gets aggregated stats for a clan using the same categories as the clan leaderboards.
        PREVIEW: This endpoint is still in beta, and may experience rough edges.
        The schema is in final form, but there may be bugs that prevent desirable operation.

        Args:
            group_id (int): Group ID of the clan whose leaderboards you wish to fetch.
            modes (list): List of game modes for which to get leaderboards.
                See the documentation for DestinyActivityModeType for valid values, and pass in string representation, comma delimited.

        Returns:
            dict: The clan aggregate stats.
        """
        try:
            self.logger.info("Getting clan aggregate stats for clan {}...".format(group_id))
            url = self.DESTINY2_URL + "Stats/AggregateClanStats/{}/?modes={}"
            url = url.format(group_id, ','.join([str(i) for i in modes]))
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetLeaderboards(
        self,
        destiny_membership_id: int,
        membership_type: int,
        max_top: int,
        modes: list,
        stat_id: str = ""
    ) -> dict:
        """*PREVIEW*
        Gets leaderboards with the signed in user's friends and the supplied destiny_membership_id as the focus.
        PREVIEW: This endpoint has not yet been implemented.
        It is being returned for a preview of future functionality, and for public comment/suggestion/preparation.

        Args:
            destiny_membership_id (int): The Destiny membership_id of the user to retrieve.
            membership_type (int): A valid non-BungieNet membership type.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.membership_type.
            max_top (int): Maximum number of top players to return.
                Use a large number to get entire leaderboard.
            modes (list): List of game modes for which to get leaderboards.
                See the documentation for DestinyActivityModeType for valid values, and pass in string representation, comma delimited.
            stat_id (str, optional): ID of stat to return rather than returning all Leaderboard stats. Defaults to "".

        Returns:
            dict: The leaderboards.
        """
        try:
            self.logger.info("Getting leaderboards for account {}...".format(destiny_membership_id))
            url = self.DESTINY2_URL + "{}/Account/{}/Stats/Leaderboards/?maxtop={}&modes={}&statid={}"
            url = url.format(membership_type, destiny_membership_id, max_top, ','.join([str(i) for i in modes]), stat_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetLeaderboardsForCharacter(
        self,
        character_id: int,
        destiny_membership_id: int,
        membership_type: int,
        max_top: int,
        modes: list,
        stat_id: str = ""
    ) -> dict:
        """*PREVIEW*
        Gets leaderboards with the signed in user's friends and the supplied destiny_membership_id as the focus.
        PREVIEW: This endpoint is still in beta, and may experience rough edges.
        The schema is in final form, but there may be bugs that prevent desirable operation.

        Args:
            character_id (int): The specific character to build the leaderboard around for the provided Destiny Membership.
            destiny_membership_id (int): The Destiny membership_id of the user to retrieve.
            membership_type (int): A valid non-BungieNet membership type.
                The types of membership the Accounts system supports. This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.membership_type.
            max_top (int): Maximum number of top players to return.
                Use a large number to get entire leaderboard.
            modes (list): List of game modes for which to get leaderboards.
                See the documentation for DestinyActivityModeType for valid values, and pass in string representation, comma delimited.
            stat_id (str, optional): ID of stat to return rather than returning all Leaderboard stats.
                Defaults to "".

        Returns:
            dict: The leaderboards for character.
        """
        try:
            self.logger.info("Getting leaderboards for character {} of account {}...".format(character_id, destiny_membership_id))
            url = self.DESTINY2_URL + "Stats/Leaderboards/{}/{}/{}/?maxtop={}&modes={}&statid={}".format(membership_type, destiny_membership_id, character_id, max_top, ','.join(modes), stat_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def SearchDestinyEntities(self, search_term: str, type: str, page: int) -> dict:
        """Gets a page list of Destiny items.

        Args:
            search_term (str): The string to use when searching for Destiny entities.
            type (str): The type of entity for whom you would like results.
                These correspond to the entity's definition contract name.
                For instance, if you are looking for items, this property should be 'DestinyInventoryItemDefinition'.
            page (int): Page number to return, starting with 0.

        Returns:
            dict: The Destiny entities.
        """
        try:
            self.logger.info("Searching destiny entities for searchterm {}...".format(search_term))
            url = self.DESTINY2_URL + "Armory/Search/Destiny2/{}/{}/?page={}"
            url = url.format(type, search_term, page)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetHistoricalStats(
        self,
        character_id: int,
        destiny_membership_id: int,
        membership_type: int,
        day_end: datetime,
        day_start: datetime,
        groups: list,
        modes: list,
        period_type: int
    ) -> dict:
        """Gets historical stats for indicated character.

        Args:
            character_id (int): The id of the character to retrieve.
                You can omit this character ID or set it to 0 to get aggregate stats across all characters.
            destiny_membership_id (int): The Destiny membership_id of the user to retrieve.
            membership_type (int): A valid non-BungieNet membership type.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.membership_type.
            day_end (datetime): Last day to return when daily stats are requested.
                Use the format YYYY-MM-DD. Currently, we cannot allow more than 31 days of daily data to be requested in a single request.
            day_start (datetime): First day to return when daily stats are requested.
                Use the format YYYY-MM-DD. Currently, we cannot allow more than 31 days of daily data to be requested in a single request.
            groups (list): Group of stats to include, otherwise only general stats are returned.
                Comma separated list is allowed.
                Values: General, Weapons, Medals
            modes (list): Game modes to return.
                See the documentation for DestinyActivityModeType for valid values, and pass in string representation, comma delimited.
            period_type (int): Indicates a specific period type to return.
                Optional.
                May be: Daily, AllTime, or Activity. If not provided, then we will return all available data for the character.

        Returns:
            dict: The historical stats.
        """
        try:
            self.logger.info("Getting historical stats for character {} of account {}...".format(character_id, destiny_membership_id))
            url = self.DESTINY2_URL + "{}/Account/{}/Character/{}/Stats/?modes={}&dayend={}&daystart={}&period_type={}&groups={}"
            url = url.format(membership_type, destiny_membership_id, character_id, ','.join([str(i) for i in modes]), day_end, day_start, period_type, ','.join([str(i) for i in groups]))
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetHistoricalStatsForAccount(
        self,
        destiny_membership_id: int,
        membership_type: int,
        groups: list
    ) -> dict:
        """Gets aggregate historical stats organized around each character for a given account.

        Args:
            destiny_membership_id (int): The Destiny membership_id of the user to retrieve.
            membership_type (int): A valid non-BungieNet membership type.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.membership_type.
            groups (list): Groups of stats to include, otherwise only general stats are returned.
                Comma separated list is allowed.
                Values: General, Weapons, Medals.

        Returns:
            dict: The historical stats for account.
        """
        try:
            self.logger.info("Getting historical stats for account {}...".format(destiny_membership_id))
            url = self.DESTINY2_URL + "{}/Account/{}/Stats/?{}"
            url = url.format(membership_type, destiny_membership_id, ','.join([str(i) for i in groups]))
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetActivityHistory(
        self,
        character_id: int,
        destiny_membership_id: int,
        membership_type: int,
        count: int,
        mode: int,
        page: int
    ) -> dict:
        """Gets activity history stats for indicated character.

        Args:
            character_id (int): The id of the character to retrieve.
            destiny_membership_id (int): The Destiny membership_id of the user to retrieve.
            membership_type (int): A valid non-BungieNet membership type.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.membership_type.
            count (int): Number of rows to return
            mode (int): A filter for the activity mode to be returned. None returns all activities.
                See the documentation for DestinyActivityModeType for valid values, and pass in string representation.
                For historical reasons, this list will have both D1 and D2-relevant Activity Modes in it.
                Please don't take this to mean that some D1-only feature is coming back!
            page (int): Page number to return, starting with 0.

        Returns:
            dict: The activity history.
        """
        try:
            self.logger.info("Getting activity history for character {} of account {}...".format(character_id, destiny_membership_id))
            url = self.DESTINY2_URL + "{}/Account/{}/Character/{}/Stats/Activities/?count={}&mode={}&page={}"
            url = url.format(membership_type, destiny_membership_id, character_id, count, mode, page)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetUniqueWeaponHistory(
        self,
        character_id: int,
        destiny_membership_id: int,
        membership_type: int
    ) -> dict:
        """Gets details about unique weapon usage, including all exotic weapons.

        Args:
            character_id (int): The id of the character to retrieve.
            destiny_membership_id (int): The Destiny membership_id of the user to retrieve.
            membership_type (int): A valid non-BungieNet membership type.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.membership_type.

        Returns:
            dict: The unique weapon history.
        """
        try:
            self.logger.info("Getting unique weapon history for character {} of account {}...".format(character_id, destiny_membership_id))
            url = self.DESTINY2_URL + "{}/Account/{}/Character/{}/Stats/UniqueWeapons/"
            url = url.format(membership_type, destiny_membership_id, character_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetDestinyAggregateActivityStats(
        self,
        character_id: int,
        destiny_membership_id: int,
        membership_type: int
    ) -> dict:
        """Gets all activities the character has participated in together with aggregate statistics for those activities.

        Args:
            character_id (int): The specific character whose activities should be returned.
            destiny_membership_id (int): The Destiny membership_id of the user to retrieve.
            membership_type (int): A valid non-BungieNet membership type.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.membership_type.

        Returns:
            dict: The aggregate activity stats.
        """
        try:
            self.logger.info("Getting aggregate activity stats for character {} of account {}...".format(character_id, destiny_membership_id))
            url = self.DESTINY2_URL + "{}/Account/{}/Character/{}/Stats/AggregateActivityStats/"
            url = url.format(membership_type, destiny_membership_id, character_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPublicMilestoneContent(self, milestoneHash: int) -> dict:
        """Gets custom localized content for the milestone of the given hash, if it exists.

        Args:
            milestoneHash (int): he identifier for the milestone to be returned.

        Returns:
            dict: The public milestone content.
        """
        try:
            self.logger.info("Getting public milestone content for milestone {}...".format(milestoneHash))
            url = self.DESTINY2_URL + "Milestones/{}/Content/".format(milestoneHash)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPublicMilestones(self) -> dict:
        """Gets public information about currently available Milestones.

        Returns:
            dict: The public milestones.
        """
        try:
            self.logger.info("Getting public milestones...")
            url = self.DESTINY2_URL + "Milestones/"
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def AwaInitializeRequest(
        self,
        token: dict,
        type: int,
        affected_item_id: int,
        membership_type: int,
        character_id: int,
    ) -> dict:
        """Initialize a request to perform an advanced write action.

        Args:
            token (dict): The token for authentication
            type (int): Type of advanced write action.
            affected_item_id (int): Item instance ID the action shall be applied to.
                This is optional for all but a new AwaType values.
                Rule of thumb is to provide the item instance ID if one is available.
            membership_type (int): Destiny membership type of the account to modify.
            character_id (int): Destiny character ID, if applicable, that will be affected by the action.

        Returns:
            dict: Object with the correlation ID.
        """
        try:
            self.logger.info("Initializing Awa request...")
            payload = {
                "type": type,
                "affectedItemId": affected_item_id,
                "membershipType": membership_type,
                "characterId": character_id
            }
            url = self.DESTINY2_URL + "Awa/Initialize/"
            return await self.requester.request(method=HTTPMethod.POST, url=url, access_token=token["access_token"], data=payload)
        except Exception as ex:
            self.logger.exception(ex)

    async def AwaProvideAuthorizationResult(
        self,
        token: dict,
        selection: int,
        correlation_id: str,
        nonce: list
    ) -> dict:
        """Provide the result of the user interaction.
        Called by the Bungie Destiny App to approve or reject a request.

        Args:
            token (dict): The token for authentication
            selection (int): Indication of the selection the user has made (Approving or rejecting the action)
            correlation_id (str): Correlation ID of the request
            nonce (list): Secret nonce received via the PUSH notification.

        Returns:
            dict: The authorization result.
        """
        try:
            self.logger.info("Providing authorization result...")
            payload = {
                "selection": selection,
                "correlationId": correlation_id,
                "nonce": nonce
            }
            url = self.DESTINY2_URL + "Awa/AwaProvideAuthorizationResult/"
            return await self.requester.request(method=HTTPMethod.POST, url=url, access_token=token["access_token"], data=payload)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetAwaGetActionToken(self, token: dict, correlation_id: str) -> dict:
        """Returns the action token if user approves the request.

        Args:
            token (dict): The token to use for authentication
            correlation_id (str): The identifier for the advanced write action request.

        Returns:
            dict: The action token.
        """
        try:
            self.logger.info("Getting action token...")
            url = self.DESTINY2_URL + "Awa/GetActionToken/{}".format(correlation_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)
