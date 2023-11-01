from destipy.utils.http_method import HTTPMethod
from destipy.utils.requester import Requester


class GroupV2:
    """GroupV2 endpoints."""
    def __init__(self, requester, logger):
        self.requester: Requester = requester
        self.logger = logger
        self.GROUPV2_URL = "https://www.bungie.net/Platform/GroupV2/"

    async def GetAvailableAvatars(self) -> dict:
        """Returns a list of all available group avatars for the signed-in user.

        Returns:
            dict: A list of all available group avatars for the signed-in user.
        """
        try:
            self.logger("Getting available avatars...")
            url = self.GROUPV2_URL + "GetAvailableAvatars/"
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetAvailableThemes(self) -> dict:
        """Returns a list of all available group themes.

        Returns:
            dict: A list of all available group themes.
        """
        try:
            self.logger("Getting available avatars...")
            url = self.GROUPV2_URL + "GetAvailableThemes/"
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetUserClanInviteSetting(self, token: dict, m_type: int) -> dict:
        """Gets the state of the user's clan invite preferences for a particular membership type - true if they wish to be invited to clans, false otherwise.

        Args:
            token (dict): The token for authentication.
            m_type (int): The Destiny membership type of the account we wish to access settings.

        Returns:
            dict: The state of the user's clan invite preferences for a particular membership type.
        """
        try:
            self.logger.info("Getting user clan invite setting...")
            url = self.GROUPV2_URL + "GetUserClanInviteSetting/{}/".format(m_type)
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetRecommendedGroups(self, created_date_range: int, group_type: int) -> dict:
        """Gets groups recommended for you based on the groups to whom those you follow belong.

        Args:
            created_date_range (int): Requested range in which to pull recommended groups
            group_type (int): Type of groups requested

        Returns:
            dict: The Recommended groups
        """
        try:
            self.logger.info("Getting recommended groups...")
            url = self.GROUPV2_URL + "GetRecommendedGroups/{}/{}/"
            url = url.format(group_type, created_date_range)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GroupSearch(
        self,
        name: str,
        group_type: int,
        creation_date: int,
        sort_by: int,
        items_per_page: int,
        current_page: int,
        request_continuation_token: str,
        group_member_count_filter: int = 0,
        locale_filter: str = "",
        tag_text: str = "",
    ) -> dict:
        """Search for Groups.

        NOTE: GroupQuery, as of Destiny 2, has essentially two totally different and incompatible "modes".
        If you are querying for a group, you can pass any of the properties below.
        If you are querying for a Clan, you MUST NOT pass any of the following properties (they must be null or undefined in your request, not just empty string/default values):
        - groupMemberCountFilter - localeFilter - tagText
        If you pass these, you will get a useless InvalidParameters error.

        Args:
            name (str): The name of the group.
            group_type (int): The type of group you are searching for.
            creation_date (int): The date range in which the group was created.
            sort_by (int): The way in which you would like to sort the results.
            group_member_count_filter (int): Some value of predefined enum (see official documentation)  Defaults to None.
            locale_filter (str): The locale to use when searching for groups.  Defaults to None.
            tag_text (str): The tag text to search for. Defaults to None.
            items_per_page (int): The number of items you would like returned per page of results.
            current_page (int): The page number of results to return.
            request_continuation_token (str): A continuation token to use to get the next page of results.

        Returns:
            dict: _description_
        """
        payload = {
            "name": name,
            "groupType": group_type,
            "creationDate": creation_date,
            "sortBy": sort_by,
            "groupMemberCountFilter": group_member_count_filter,
            "localeFilter": locale_filter,
            "tagText": tag_text,
            "itemsPerPage": items_per_page,
            "currentPage": current_page,
            "requestContinuationToken": request_continuation_token,
        }
        if group_member_count_filter is None and locale_filter is None and tag_text is None:
            payload.pop("groupMemberCountFilter")
            payload.pop("localeFilter")
            payload.pop("tagText")
        url = self.GROUPV2_URL + "Search/"
        return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload)

    async def GetGroup(self, group_id: int) -> dict:
        """Get information about a specific group of the given ID.

        Args:
            group_id (int): Requested group's id.

        Returns:
            dict: The requested group.
        """
        try:
            self.logger.info("Getting group...")
            url = self.GROUPV2_URL + "{}/".format(group_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetGroupByName(self, group_name: str, group_type: int) -> dict:
        """Get information about a specific group with the given name and type.

        Args:
            group_name (str): Exact name of the group to find.
            group_type (int): Type of group to find.

        Returns:
            dict: The requested group.
        """
        try:
            self.logger.info("Getting group by name...")
            url = self.GROUPV2_URL + "Name/{}/{}/".format(group_name, group_type)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetGroupByNameV2(self, group_name: str, group_type: int) -> dict:
        """Get information about a specific group with the given name and type. The POST version.

        Args:
            group_name (str): Exact name of the group to find.
            group_type (int): Type of group to find.

        Returns:
            dict:
        """
        try:
            self.logger.info("Getting group by name v2...")
            payload = {
                "groupName": group_name,
                "groupType": group_type,
            }
            url = self.GROUPV2_URL + "NameV2/"
            return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetGroupOptionalConversations(self, group_id:int) -> dict:
        """Gets a list of available optional conversation channels and their settings.

        Args:
            group_id (int): Requested group's id.

        Returns:
            dict: The optional conversations.
        """
        try:
            self.logger.info("Getting optional conversations...")
            url = self.GROUPV2_URL + "{}/OptionalConversations/".format(group_id)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def EditGroup(
        self,
        token: dict,
        group_id: int,
        name: str = None,
        about: str = None,
        motto: str = None,
        theme: str = None,
        avatar_image_index: int = None,
        tags: str = None,
        isPublic: bool = None,
        membershipOption: int = None,
        isPublicTopicAdminOnly: bool = None,
        allowChat: bool = None,
        chatSecurity: int = None,
        callSign: str = None,
        locale: str = None,
        homepage: int = None,
        enableInvitationMessagingForAdmins: bool = None,
        defaultPublicity: int = None,
    ) -> dict:
        """Edit an existing group. You must have suitable permissions in the group to perform this operation.
        This latest revision will only edit the fields you pass in - pass null for properties you want to leave unaltered.

        Args:
            token (dict): The token of the admin requesting the edit.
            group_id (int): The ID of the group to edit.
            name (str, optional): The new name of the group. Defaults to None.
            about (str, optional): The new about text of the group. Defaults to None.
            motto (str, optional): The new motto of the group. Defaults to None.
            theme (str, optional): The new theme of the group. Defaults to None.
            avatar_image_index (int, optional): The new avatar image index of the group. Defaults to None.
            tags (str, optional): The new tags of the group. Defaults to None.
            isPublic (bool, optional): The new public status of the group. Defaults to None.
            membershipOption (int, optional): The new membership option of the group. Defaults to None.
            isPublicTopicAdminOnly (bool, optional): The new public topic admin only status of the group. Defaults to None.
            allowChat (bool, optional): The new chat status of the group. Defaults to None.
            chatSecurity (int, optional): The new chat security of the group. Defaults to None.
            callSign (str, optional): The new call sign of the group. Defaults to None.
            locale (str, optional): The new locale of the group. Defaults to None.
            homepage (int, optional): The new homepage of the group. Defaults to None.
            enableInvitationMessagingForAdmins (bool, optional): The new invitation messaging status of the group. Defaults to None.
            defaultPublicity (int, optional): The new default publicity of the group. Defaults to None.

        Returns:
            dict: The edited group.
        """
        try:
            self.logger.info("Editing group...")
            payload = {
                "name": name,
                "about": about,
                "motto": motto,
                "theme": theme,
                "avatarImageIndex": avatar_image_index,
                "tags": tags,
                "isPublic": isPublic,
                "membershipOption": membershipOption,
                "isPublicTopicAdminOnly": isPublicTopicAdminOnly,
                "allowChat": allowChat,
                "chatSecurity": chatSecurity,
                "callSign": callSign,
                "locale": locale,
                "homepage": homepage,
                "enableInvitationMessagingForAdmins": enableInvitationMessagingForAdmins,
                "defaultPublicity": defaultPublicity,
            }
            url = self.GROUPV2_URL + "{}/Edit".format(group_id)
            return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def EditClanBanner(
        self,
        token: dict,
        group_id: int,
        decal_id: int,
        decal_color_id: int,
        decal_background_color_id: int,
        gonfalon_id: int,
        gonfalon_color_id: int,
        gonfalon_detail_id: int,
        gonfalon_detail_color_id: int,
    ) -> dict:
        """Edit an existing group's clan banner.
        You must have suitable permissions in the group to perform this operation.
        All fields are required.

        Args:
            token (dict): The token of the admin requesting the edit.
            group_id (int): The ID of the group to edit
            decal_id (int, optional): The new decal ID of the group. Defaults to None.
            decal_color_id (int, optional): The new decal color ID of the group. Defaults to None.
            decal_background_color_id (int, optional): The new decal background color ID of the group. Defaults to None.
            gonfalon_id (int, optional): The new gonfalon ID of the group. Defaults to None.
            gonfalon_color_id (int, optional): The new gonfalon color ID of the group. Defaults to None.
            gonfalon_detail_id (int, optional): The new gonfalon detail ID of the group. Defaults to None.
            gonfalon_detail_color_id (int, optional): The new gonfalon detail color ID of the group. Defaults to None.

        Returns:
            dict: The edited group.
        """
        try:
            self.logger.info("Editing clan banner...")
            payload = {
                "decalId": decal_id,
                "decalColorId": decal_color_id,
                "decalBackgroundColorId": decal_background_color_id,
                "gonfalonId": gonfalon_id,
                "gonfalonColorId": gonfalon_color_id,
                "gonfalonDetailId": gonfalon_detail_id,
                "gonfalonDetailColorId": gonfalon_detail_color_id,
            }
            url = self.GROUPV2_URL + "{}/EditClanBanner".format(group_id)
            return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def EditFounderOptions(
        self,
        token: dict,
        group_id: int,
        invite_permission_override: bool,
        update_culture_permission_override: bool,
        host_guided_game_permission_override: int,
        update_banner_permission_override: bool,
        join_level: int,
    ) -> dict:
        """Edit group options only available to a founder.
        You must have suitable permissions in the group to perform this operation.

        Args:
            token (dict): The token of the admin requesting the edit.
            group_id (int): The ID of the group to edit.
            invite_permission_override (bool, optional): Minimum Member Level allowed to invite new members to group
                Always Allowed: Founder, Acting Founder
                True means admins have this power, false means they don't
                Default is false for clans, true for groups.
                Defaults to None.
            update_culture_permission_override (bool, optional): Minimum Member Level allowed to update group culture
                Always Allowed: Founder, Acting Founder
                True means admins have this power, false means they don't
                Default is false for clans, true for groups.
                Defaults to None.
            host_guided_game_permission_override (int, optional): Minimum Member Level allowed to host guided games
                Always Allowed: Founder, Acting Founder, Admin
                Allowed Overrides: None, Member, Beginner
                Default is Member for clans, None for groups, although this means nothing for groups.
                Valid Enum Values: None: 0, Beginner: 1, Member: 2
                Defaults to None.
            update_banner_permission_override (bool, optional): Minimum Member Level allowed to update banner
                Always Allowed: Founder, Acting Founder
                True means admins have this power, false means they don't
                Default is false for clans, true for groups.
                Defaults to None.
            join_level (int, optional): Level to join a member at when accepting an invite, application, or joining an open clan
                Default is Beginner.
                Valid Enum Values: None: 0, Beginner: 1, Member: 2, Admin: 3, Acting Founder: 4, Founder: 5
                Defaults to None.

        Returns:
            dict: The edited group.
        """
        try:
            self.logger.info("Editing founder options...")
            payload = {
                "InvitePermissionOverride": invite_permission_override,
                "UpdateCulturePermissionOverride": update_culture_permission_override,
                "HostGuidedGamePermissionOverride": host_guided_game_permission_override,
                "UpdateBannerPermissionOverride": update_banner_permission_override,
                "joinLevel": join_level,
            }
            url = self.GROUPV2_URL + "{}/EditFounderOptions".format(group_id)
            return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def AddOptionalConversation(
        self,
        token: dict,
        group_id: int,
        chat_name: str,
        chat_security: int,
    ) -> dict:
        """Add a new optional conversation/chat channel.
        Requires admin permissions to the group.

        Args:
            token (dict): The token of the admin requesting the edit.
            group_id (int): The ID of the group to edit.
            chat_name (str): The name of the chat.
            chat_security (int): The security level of the chat.
                Valid Enum Values: Group: 0, Admins: 1
        Returns:
            dict: The edited group.
        """
        try:
            self.logger.info("Adding optional conversation...")
            payload = {
                "chatName": chat_name,
                "chatSecurity": chat_security,
            }
            url = self.GROUPV2_URL + "{}/OptionalConversations/Add/".format(group_id)
            return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def EditOptionalConversation(
        self,
        token: dict,
        conversation_id: int,
        group_id: int,
        chat_enabled: bool,
        chat_name: str,
        chat_security: int,
    ) -> dict:
        """Edit the settings of an optional conversation/chat channel.
        Requires admin permissions to the group.


        Args:
            token (dict): The token of the admin requesting the edit.
            conversation_id (int): Conversation Id of the channel being edited.
            group_id (int): The ID of the group to edit.
            chat_name (str): The name of the chat.
            chat_security (int): The security level of the chat.
                Valid Enum Values: Group: 0, Admins: 1
        Returns:
            dict: The edited group.
        """
        try:
            self.logger.info("Editing optional conversation...")
            payload = {
                "chatEnabled": chat_enabled,
                "chatName": chat_name,
                "chatSecurity": chat_security,
            }
            url = self.GROUPV2_URL + "{}/OptionalConversations/Edit/{}".format(group_id, conversation_id)
            return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetMembersOfGroup(
        self,
        current_page: int,
        group_id: int,
        member_type: int,
        name_search: str,
    ) -> dict:
        """Get the list of members in a given group.

        Args:
            current_page (int): Page number (starting with 1).
                Each page has a fixed size of 50 items per page.
            group_id (int): The ID of the group.
            member_type (int, optional): Filter out other member types. Use None for all members.
            The member levels used by all V2 Groups API. Individual group types use their own mappings in their native storage (general uses BnetDbGroupMemberType and D2 clans use ClanMemberLevel), but they are all translated to this in the runtime api.
                These runtime values should NEVER be stored anywhere, so the values can be changed as necessary.
                Defaults to None.
            name_search (str, optional): The name fragment upon which a search should be executed for members with matching display or unique names.
                Defaults to None.
        Returns:
            dict: The members of the group.
        """
        try:
            self.logger.info("Getting members of group...")
            url = self.GROUPV2_URL + "{}/Members/?memberType={}&nameSearch={}"
            url = url.format(group_id, member_type, name_search)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetAdminsAndFounderOfGroup(self, current_page: int, group_id: int) -> dict:
        """Get the list of members in a given group who are of admin level or higher.

        Args:
            current_page (int): Page number (starting with 1).
                Each page has a fixed size of 50 items per page.
            group_id (int): The ID of the group.
        Returns:
            dict: The admins and founder of the group.
        """
        try:
            self.logger.info("Getting admins and founder of group...")
            url = self.GROUPV2_URL + "{}/AdminsAndFounder/?currentPage={}"
            url = url.format(group_id, current_page)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def EditGroupMembership(
        self,
        token: dict,
        group_id: int,
        membership_id: int,
        membership_type: int,
        member_type: int,
    ) -> dict:
        """Edit the membership type of a given member.
        You must have suitable permissions in the group to perform this operation.

        Args:
            token (dict): The token of the admin requesting the edit.
            group_id (int): ID of the group to which the member belongs.
            membership_id (int): Membership ID to modify.
            membership_type (int): Membership type of the provide membership ID.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.MembershipType.
            member_type (int): New membertype for the specified member.
                The member levels used by all V2 Groups API.
                Individual group types use their own mappings in their native storage (general uses BnetDbGroupMemberType and D2 clans use ClanMemberLevel), but they are all translated to this in the runtime api.
                These runtime values should NEVER be stored anywhere, so the values can be changed as necessary.
        Returns:
            dict: The edited group.
        """
        try:
            self.logger.info("Editing group membership...")
            url = self.GROUPV2_URL + "{}/Members/{}/{}/SetMembershipType/{}"
            url = url.format(group_id, membership_type, membership_id, member_type)
            return await self.requester.request(method=HTTPMethod.POST, url=url, data={}, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def KickMember(
        self,
        token: dict,
        group_id: int,
        membership_id: int,
        membership_type: int,
    ) -> dict:
        """Kick a member from the given group, forcing them to reapply if they wish to re-join the group.
        You must have suitable permissions in the group to perform this operation.

        Args:
            token (dict): The token of the admin requesting the kick.
            group_id (int): ID of the group to which the member belongs.
            membership_id (int): Membership ID to kick.
            membership_type (int): Membership type of the provide membership ID.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.MembershipType.
        Returns:
            dict: The result of the kick.
        """
        try:
            self.logger.info("Kicking member...")
            url = self.GROUPV2_URL + "{}/Members/{}/{}/Kick/"
            url = url.format(group_id, membership_type, membership_id)
            return await self.requester.request(method=HTTPMethod.POST, url=url, data={}, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def BanMember(
            self,
        token: dict,
        group_id: int,
        membership_id: int,
        membership_type: int,
        length: int,
        comment: str = ""
    ) -> dict:
        """Bans the requested member from the requested group for the specified period of time.

        Args:
            token (dict): The token of the admin requesting the ban.
            group_id (int): Group ID that has the member to ban.
            membership_id (int): Membership ID of the member to ban from the group.
            membership_type (int): Membership type of the provide membership ID.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.MembershipType.
            comment (str, Optional): Optional comment to be added to the ban. Defaults to "".
            length (int): Length of the ban in days.

        Returns:
            dict: The result of the kick.
        """
        try:
            self.logger.info("Banning member...")
            payload = {
                "comment": comment,
                "length": length
            }
            url = self.GROUPV2_URL + "{}/Members/{}/{}/Ban/"
            url = url.format(group_id, membership_type, membership_id)
            return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def UnbanMember(
        self,
        token: dict,
        group_id: int,
        membership_id: int,
        membership_type: int
    ) -> dict:
        """Unbans the requested member, allowing them to re-apply for membership.

        Args:
            token (dict): The token of the admin requesting the unban.
            group_id (int): Group ID that has the member to unban.
            membership_id (int): Membership ID of the member to unban from the group
            membership_type (int): Membership type of the provided membership ID.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.MembershipType.
        Returns:
            dict: The result of the kick.
        """
        try:
            self.logger.info("Unbanning member...")
            url = self.GROUPV2_URL + "{}/Members/{}/{}/Unban/"
            url = url.format(group_id, membership_type, membership_id)
            return await self.requester.request(method=HTTPMethod.POST, url=url, data={}, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetBannedMembersOfGroup(self, current_page: int, group_id: int) -> dict:
        """Get the list of banned members in a given group.
        Only accessible to group Admins and above.
        Not applicable to all groups. Check group features.

        Args:
            current_page (int): Page number (starting with 1). Each page has a fixed size of 50 entries.
            group_id (int): Group ID whose banned members you are fetching

        Returns:
            dict: The list of banned members.
        """
        try:
            self.logger.info("Getting banned members...")
            url = self.GROUPV2_URL + "{}/Banned/?currentPage={}"
            url = url.format(group_id, current_page)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def AbdicateFoundership(
        self,
        founder_id_new: int,
        group_id: int,
        membership_type: int,
    ) -> dict:
        """An administrative method to allow the founder of a group or clan to give up their position to another admin permanently.

        Args:
            founder_id_new (int): The new founder for this group. Must already be a group admin.
            group_id (int): The target group id.
            membership_type (int): Membership type of the provided membership ID.
                The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.MembershipType.
        Returns:
            dict: The result of the transfer.
        """
        try:
            self.logger.info("Transferring founder...")
            url = self.GROUPV2_URL + "{}/Admin/AbdicateFoundership/{}/{}"
            url = url.format(group_id, membership_type, founder_id_new)
            return await self.requester.request(method=HTTPMethod.POST, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPendingMemberships(self, token: dict, current_page: int, group_id: int) -> dict:
        """Get the list of users who are awaiting a decision on their application to join a given group.
        Modified to include application info.

        Args:
            token (dict): The token of the admin requesting the pending members.
            current_page (int): Page number (starting with 1). Each page has a fixed size of 50 entries.
            group_id (int): Group ID whose pending members you are fetching.

        Returns:
            dict: The list of pending members.
        """
        try:
            self.logger.info("Getting pending members...")
            url = self.GROUPV2_URL + "{}/Members/Pending/?currentPage={}"
            url = url.format(group_id, current_page)
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetInvitedIndividuals(self, token: dict, current_page: int, group_id: int) -> dict:
        """Get the list of users who have been invited into the group.

        Args:
            token (dict): The token of the admin requesting the invited members.
            current_page (int): Page number (starting with 1). Each page has a fixed size of 50 entries.
            group_id (int): Group ID whose invited members you are fetching.

        Returns:
            dict: The list of invited members.
        """
        try:
            self.logger.info("Getting invited members...")
            url = self.GROUPV2_URL + "{}/Members/InvitedIndividuals/?currentPage={}"
            url = url.format(group_id, current_page)
            return await self.requester.request(method=HTTPMethod.GET, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def ApproveAllPending(self, token: dict, group_id: int, message: str = "") -> dict:
        """Approve all of the pending users for the given group.

        Args:
            token (dict): The token of the admin requesting the approval.
            group_id (int): Group ID whose pending members you are approving.
            message (str, optional): Message to send to the users. Defaults to "".

        Returns:
            dict: The result of the approval.
        """
        try:
            self.logger.info("Approving all pending members...")
            payload = {
                "message": message
            }
            url = self.GROUPV2_URL + "{}/Members/ApproveAll/"
            url = url.format(group_id)
            return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def DenyAllPending(self, token: dict, group_id: int, message: str = "") -> dict:
        """Deny all of the pending users for the given group.

        Args:
            token (dict): The token of the admin requesting the denial.
            group_id (int): Group ID whose pending members you are denying.
            message (str, optional): Message to send to the users. Defaults to "".

        Returns:
            dict: The result of the denial.
        """
        try:
            self.logger.info("Denying all pending members...")
            payload = {
                "message": message
            }
            url = self.GROUPV2_URL + "{}/Members/DenyAll/"
            url = url.format(group_id)
            return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def ApprovePendingForList(
        self,
        token: dict,
        group_id: int,
        memberships: list,
        message: str = ""
    ) -> dict:
        """Approve all of the pending users for the given group.

        Args:
            token (dict): The token of the admin requesting the approval.
            group_id (int): Group ID whose pending members you are approving.
            membership_ids (list): List of memberships to approve.
                A Membership consists of a dict with following properties:
                {membershipType, membershipId, displayName, bungieGlobalDisplayName, bungieGlobalDisplayNameCode}
            message (str, optional): Message to send to the users. Defaults to "".

        Returns:
            dict: The result of the approval.
        """
        try:
            self.logger.info("Approving pending members...")
            payload = {
                "memberships": memberships,
                "message": message
            }
            url = self.GROUPV2_URL + "{}/Members/ApproveList/"
            url = url.format(group_id)
            return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def ApprovePending(
        self,
        token: dict,
        group_id: int,
        membership_id: int,
        membership_type: int,
        message: str = ""
    ) -> dict:
        """Approve the given membershipId to join the group/clan as long as they have applied.

        Args:
            token (dict): The token of the admin requesting the approval.
            group_id (int): Group ID whose pending members you are approving.
            membership_id (int): Membership ID of the user to approve.
            membership_type (int): Membership type of the user to approve.
            message (str, optional): Message to send to the user. Defaults to "".

        Returns:
            dict: The result of the approval.
        """
        try:
            self.logger.info("Approving pending member...")
            payload = {
                "message": message
            }
            url = self.GROUPV2_URL + "{}/Members/Approve/{}/{}/"
            url = url.format(group_id, membership_type, membership_id)
            return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def DenyPendingForList(
        self,
        token: dict,
        group_id: int,
        memberships: list,
        message: str = ""
    ) -> dict:
        """Deny all of the pending users for the given group that match the passed-in.

        Args:
            token (dict): The token of the admin requesting the denial.
            group_id (int): Group ID whose pending members you are denying.
            memberships (list): List of memberships to deny.
                A Membership consists of a dict with following properties:
                {membershipType, membershipId, displayName, bungieGlobalDisplayName, bungieGlobalDisplayNameCode}
        Returns:
            dict: The result of the denial.
        """
        try:
            self.logger.info("Denying pending members...")
            payload = {
                "memberships": memberships,
                "message": message
            }
            url = self.GROUPV2_URL + "{}/Members/DenyList/"
            url = url.format(group_id)
            return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def GetGroupsForMember(
        self,
        membership_type: int,
        destiny_membership_id: int,
        filter: int = 0,
        group: int = 1
    ) -> dict:
        """Get information about the groups that a given member has joined.

        Args:
            membershipType (int): Membership type of the supplied membership ID.
            destinyMembershipId (int): Membership ID to for which to find founded groups.
            filter (int, optional): Filter apply to list of joined groups. Defaults to 0 (All).
            group (int, optional): Type of group the supplied member founded. Defaults to 1 (Clan).

        Raises:
            Exception: Error fetching groups for member. Reason: response

        Returns:
            dict: The groups that the member has joined.
        """
        try:
            url = self.GROUPV2_URL + "User/{}/{}/{}/{}".format(membership_type, destiny_membership_id, filter, group)
            self.logger.info("Getting groups for {}...".format(destiny_membership_id))
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def RecoverGroupForFounder(
        self,
        group_type: int,
        membership_id: int,
        membership_type: int,
    ) -> dict:
        """Allows a founder to manually recover a group they can see in game but not on bungie.net

        Args:
            group_type (int): Type of group the supplied member founded.
            membership_id (int): Membership ID to for which to find founded groups.
            membership_type (int): The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.MembershipType.


        Returns:
            dict: The groups that the member has joined.
        """
        try:
            self.logger.info("Recovering group for {}...".format(membership_id))
            url = self.GROUPV2_URL + "Recover/{}/{}/{}/".format(membership_type, membership_id, group_type)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def GetPotentialGroupsForMember(
        self,
        membership_id: int,
        membership_type: int,
        filter: int = 0,
        group_type: int = 1,
    ) -> dict:
        """Get information about the groups that a given member has applied to or been invited to.

        Args:
            membership_id (int): Membership ID to for which to find applied groups.
            membership_type (int): Membership type of the supplied membership ID.
                The types of membership the Accounts system supports. This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.MembershipType.

            filter (int, optional): Filter apply to list of potential joined groups. Defaults to 0.
            group_type (int, optional): Type of group the supplied member applied. Defaults to 1.

        Returns:
            dict: The groups that the member has applied to or been invited to.
        """
        try:
            self.logger.info("Getting potential groups for {}...".format(membership_id))
            url = self.GROUPV2_URL + "User/Potential/{}/{}/{}/{}/".format(membership_type, membership_id, filter, group_type)
            return await self.requester.request(method=HTTPMethod.GET, url=url)
        except Exception as ex:
            self.logger.exception(ex)

    async def IndividualGroupInvite(
        self,
        token: dict,
        group_id: int,
        membership_id: int,
        membership_type: int,
        message: str = "Welcome",
    ) -> dict:
        """Invite a user to join this group.

        Args:
            token (dict): The token used for authentication
            group_id (int): ID of the group you would like to join.
            destiny_membership_id (int): Destiny Membership id of the account being invited.

            membership_type (int): MembershipType of the account being invited. The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.MembershipType.
            message (str, optional): The message to send along with the invite. Defaults to "Welcome"

        Returns:
            dict: The groups that the member has applied to or been invited to.
        """
        try:
            self.logger.info("Inviting {} to group {}...".format(membership_id, group_id))
            url = self.GROUPV2_URL + "{}/Members/IndividualInvite/{}/{}/"
            url = url.format(group_id, membership_type, membership_id)
            payload = {
                    "message": message
            }
            return await self.requester.request(method=HTTPMethod.POST, url=url, data=payload, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)

    async def IndividualGroupInviteCancel(
        self,
        token: dict,
        group_id: int,
        membership_id: int,
        membership_type: int,
    ) -> dict:
        """Cancels a pending invitation to join a group.

        Args:
            token (dict): The token to user for admin operations.
            group_id (int): ID of the group you would like to join.
            membership_id (int): Membership id of the account being invited.
            membership_type (int): MembershipType of the account being invited. The types of membership the Accounts system supports.
                This is the external facing enum used in place of the internal-only Bungie.SharedDefinitions.MembershipType.

        Returns:
            dict: The groups that the member has applied to or been invited to.
        """
        try:
            self.logger.info("Cancelling invite for {} to group {}...".format(membership_id, group_id))
            url = self.GROUPV2_URL + "{}/Members/IndividualInviteCancel/{}/{}/"
            url = url.format(group_id, membership_type, membership_id)
            return await self.requester.request(method=HTTPMethod.POST, url=url, access_token=token["access_token"])
        except Exception as ex:
            self.logger.exception(ex)
