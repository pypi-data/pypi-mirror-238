# from dislord.models.types import Snowflake
# from dislord.models.enums import *
#
#
# class ApplicationCommandOptionChoice:
#     name: str
#     name_localizations: dict[Locale, str]
#     value: [str, int, float]
#
#
# class ApplicationCommandOption:
#     type: ApplicationCommandOptionType
#     name: str
#     name_localizations: dict[Locale, str]
#     description: str
#     description_localizations: dict[Locale, str]
#     required: bool
#     choices: list[ApplicationCommandOptionChoice]
#     options: list[ApplicationCommandOption]
#     channel_types: list[ChannelType]
#     min_value: [int, float]
#     max_value: [int, float]
#     min_length: int
#     max_length: int
#     autocomplete: bool
#
#
# class ApplicationCommand:
#     id: Snowflake
#     type: ApplicationCommandType
#     application_id: Snowflake
#     guild_id: Snowflake
#     name: str
#     name_localizations: dict[Locale, str]
#     description: str
#     description_localizations: dict[Locale, str]
#     options: list[ApplicationCommandOption]
#     default_member_permissions: str
#     dm_permission: bool
#     nsfw: bool
#     version: Snowflake
#
#
#     def __init__(self):
#         pass
#
#     def from_data(self, data):
#         pass
#
#
# class WelcomeScreenChannel:
#     channel_id: Snowflake
#     description: str
#     emoji_id: Snowflake
#     emoji_name: str
#
#
# class WelcomeScreen:
#     desciption: str
#     welcome_channels: list[WelcomeScreenChannel]
#
#
# class Guild:
#     id: Snowflake
#     name: str
#     icon: str
#     icon_hash: str
#     splash: str
#     discovery_splash: str
#     owner: bool
#     owner_id: Snowflake
#     permissions: str
#     region: str
#     afk_channel_id: Snowflake
#     afk_timeout: int
#     widget_enabled: bool
#     widget_channel_id: Snowflake
#     verification_level: int
#     default_message_notifications: int
#     explicit_content_filter: int
#     roles: list[Role]
#     emojis: list[Emoji]
#     features: list[GuildFeature] # FIXME: Add Enum
#     mfa_level: int
#     application_id: Snowflake
#     system_channel_id: Snowflake
#     system_channel_flags: int
#     rules_channel_id: Snowflake
#     max_presences: int
#     max_members: int
#     vanity_url_code: str
#     description: str
#     banner: str
#     premium_tier: int
#     preferred_locale: str
#     public_updates_channel_id: Snowflake
#     max_video_channel_users: int
#     approximate_member_count: int
#     approximate_presence_count: int
#     welcome_screen: WelcomeScreen
#     nsfw_level: int
#     stickers: Sticker
#     premium_progress_bar_enabled: bool
#     safety_alerts_channel_id: Snowflake
#
#
# class PartialGuild(Guild):
#     # UNKNOWN PARTIALITY
#     pass
#
#
# class User:
#     id: Snowflake
#     username: str
#     discriminator: str
#     global_name: str
#     avatar: str
#     bot: bool
#     system: bool
#     mfa_enabled: bool
#     banner: str
#     accent_color: int
#     locale: str
#     verified: bool
#     email: str
#     flags: int
#     premium_type: int
#     public_flags: int
#     avatar_decoration: str
#
#
# class PartialUser:
#     # UNKNOWN PARTIALITY
#     pass
#
#
# class GuildMember:
#     user: User
#     nick: str
#     avatar: str
#     roles: list[Snowflake]
#     joined_at: str  # ISO8601 Timestamp
#     premium_since: str  # ISO8601 Timestamp
#     deaf: bool
#     mute: bool
#     flags: int
#     pending: bool
#     permissions: str
#     communication_disabled_until: str   # ISO8601 Timestamp
#
#
# class PartialMember(GuildMember):
#     # UNKNOWN PARTIALITY
#     pass
#
#
# class RoleTag:
#     bot_id: Snowflake
#     integration_id: Snowflake
#     premium_subscriber: None
#     subscription_listing_id: Snowflake
#     available_for_purchase: None
#     guild_connections: None
#
#
# class Role:
#     id: Snowflake
#     name: str
#     color: int
#     hoist: bool
#     icon: str
#     unicode_emoji: str
#     position: int
#     permissions: str
#     managed: bool
#     mentionable: bool
#     tags: RoleTag
#     flags: int
#
#
# class Overwrite:
#     id: Snowflake
#     type: int  # 0: role, 1: member
#     allow: str
#     deny: str
#
#
# class ThreadMetadata:
#     archived: bool
#     auto_archive_duration: int
#     archive_timestamp: str  # ISO8601 timestamp
#     locked: bool
#     invitable: bool
#     create_timestamp: str  # ISO8601 timestamp
#
#
# class ThreadMember:
#     id: Snowflake
#     user_id: Snowflake
#     join_timestamp: str  # ISO8601 timestamp
#     flags: int
#     member: GuildMember
#
#
# class Tag:
#     id: Snowflake
#     name: str
#     moderated: bool
#     emoji_id: Snowflake
#     emoji_name: str
#
#
# class DefaultReaction:
#     emoji_id: Snowflake
#     emoji_name: str
#
#
# class Channel:
#     id: Snowflake
#     type: int
#     guild_id: Snowflake
#     position: int
#     permission_overwrites: list[Overwrite]
#     name: str
#     topic: str
#     nsfw: bool
#     last_message_id: Snowflake
#     bitrate: int
#     user_limit: int
#     rate_limit_per_user: int
#     recipients: list[User]
#     icon: str
#     owner_id: Snowflake
#     application_id: Snowflake
#     managed: bool
#     parent_id: Snowflake
#     last_pin_timestamp: str  # ISO8601 timestamp
#     rtc_region: str
#     video_quality_mode: int
#     message_count: int
#     member_count: int
#     thread_metadata: ThreadMetadata
#     member: ThreadMember
#     default_auto_archive_duration: int
#     permissions: str
#     flags: int
#     total_message_sent: int
#     available_tags: list[Tag]
#     applied_tags: list[Snowflake]
#     default_reaction_emoji: DefaultReaction
#     default_thread_rate_limit_per_user: int
#     default_sort_order: int
#     default_forum_layout: int
#
#
# class PartialChannel(Channel):
#     # UNKNOWN PARTIALITY
#     pass
#
#
# class ChannelMention:
#     id: Snowflake
#     guild_id: Snowflake
#     type: int
#     name: str
#
#
# class Attachment:
#     id: Snowflake
#     filename: str
#     description: str
#     content_type: str
#     size: int
#     url: str
#     proxy_url: str
#     height: int
#     width: int
#     ephemeral: bool
#     duration_secs: float
#     waveform: str
#     flags: int
#
#
# class EmbedFooter:
#     text: str
#     icon_url: str
#     proxy_icon_url: str
#
#
# class EmbedImage:
#     url: str
#     proxy_url: str
#     height: int
#     width: int
#
#
# class EmbedThumbnail:
#     url: str
#     proxy_url: str
#     height: int
#     width: int
#
#
# class EmbedVideo:
#     url: str
#     proxy_url: str
#     height: int
#     width: int
#
#
# class EmbedProvider:
#     name: str
#     url: str
#
#
# class EmbedAuthor:
#     name: str
#     url: str
#     icon_url: str
#     proxy_icon_url: str
#
#
# class EmbedField:
#     name: str
#     value: str
#     inline: bool
#
#
# class Embed:
#     title: str
#     type: str
#     description: str
#     url: str
#     timestamp: str  # ISO8601 timestamp
#     color: int
#     footer: EmbedFooter
#     image: EmbedImage
#     thumbnail: EmbedThumbnail
#     video: EmbedVideo
#     provider: EmbedProvider
#     author: EmbedAuthor
#     fields: list[EmbedField]
#
#
# class ReactionCountDetails:
#     burst: int
#     normal: int
#
#
# class Emoji:
#     id: Snowflake
#     name: str
#     roles: list[Role]
#     user: User
#     require_colons: bool
#     managed: bool
#     animated: bool
#     available: bool
#
#
# class PartialEmoji:
#     # UNKNOWN PARTIALITY
#     pass
#
#
# class Reaction:
#     count: int
#     count_details: ReactionCountDetails
#     me: bool
#     me_burst: bool
#     emoji: PartialEmoji
#     burst_colors: list[int]
#
#
# class MessageActivity:
#     type: int
#     party_id: str
#
#
# class TeamMember:
#     membership_state: int
#     team_id: Snowflake
#     user: PartialUser
#     role: str
#
#
# class Team:
#     icon: str
#     id: Snowflake
#     members: list[TeamMember]
#     name: str
#     owner_user_id: Snowflake
#
# class InstallParams:
#     scopes: list[str]
#     permissions: str
#
#
# class Application:
#     id: Snowflake
#     name: str
#     icon: str
#     description: str
#     rpc_origins: list[str]
#     bot_public: bool
#     bot_require_code_grant: bool
#     bot: PartialUser
#     terms_of_service_url: str
#     privacy_policy_url: str
#     owner: PartialUser
#     summary: str  # depreciated v11
#     verify_key: str
#     team: Team
#     guild: PartialGuild
#     primary_sku_id: Snowflake
#     slug: str
#     cover_image: str
#     flags: int
#     approximate_guild_count: int
#     redirect_uris: list[str]
#     interactions_endpoint_url: str
#     role_connections_verification_url: str
#     tags: list[str]
#     install_params: InstallParams
#     custom_install_url: str
#
#
# class MessageReference:
#     message_id: Snowflake
#     channel_id: Snowflake
#     guild_id: Snowflake
#     fail_if_not_exists: bool
#
#
# class MessageInteraction:
#     id: Snowflake
#     type: InteractionType
#     name: str
#     user: User
#     member: PartialMember
#
#
# class MessageStickerItem:
#     id: Snowflake
#     name: str
#     format_type: int
#
#
# class Sticker:
#     id: Snowflake
#     pack_id: Snowflake
#     name: str
#     description: str
#     tags: str
#     asset: str
#     type: int
#     format_type: int
#     available: bool
#     guild_id: Snowflake
#     user: User
#     sort_value: int
#
#
# class RoleSubscriptionData:
#     role_subscription_listing_id: Snowflake
#     tier_name: str
#     total_months_subscribed: int
#     is_renewal: bool
#
#
# class Message:
#     id: Snowflake
#     channel_id: Snowflake
#     author: User
#     content: str
#     timestamp: str  # ISO8601 timestamp
#     edited_timestamp: str  # ISO8601 timestamp
#     tts: bool
#     mention_everyone: bool
#     mentions: list[User]
#     mention_roles: list[Role]
#     mention_channels: list[ChannelMention]
#     attachments: list[Attachment]
#     embeds: list[Embed]
#     reactions: list[Reaction]
#     nonce: [int, str]
#     pinned: bool
#     webhook_id: Snowflake
#     type: int
#     activity: MessageActivity
#     application: Application
#     application_id: Snowflake
#     message_reference: MessageReference
#     flags: int
#     referenced_message: Message
#     interaction: MessageInteraction
#     thread: Channel
#     components: list[MessageComponent]  # FIXME: Add Enum
#     sticker_items: list[MessageStickerItem]
#     stickers: list[Sticker]
#     position: int
#     role_subscription_data: RoleSubscriptionData
#     resolved: ResolvedData  # Below
#
# class PartialMessage(Message):
#     # UNKNOWN PARTIALITY
#     pass
#
#
#
#
# class ResolvedData:
#     users: dict[Snowflake, User]
#     members: dict[Snowflake, PartialMember]
#     roles: dict[Snowflake, Role]
#     channels: dict[Snowflake, PartialChannel]
#     messages: dict[Snowflake, PartialMessage]
#     channels: dict[Snowflake, Attachment]
#
#
# class ApplicationCommandInteractionDataOption:
#     name: str
#     type: int
#     value: [str, int, float, bool]
#     options: list[ApplicationCommandInteractionDataOption]
#     focused: bool
#
#
# class InteractionData:
#     id: Snowflake
#     name: str
#     type: int
#     resolved: ResolvedData
#     options: list[ApplicationCommandInteractionDataOption]
#     guild_id: Snowflake
#     target_id: Snowflake
#
#
# class Entitlement:
#     id: Snowflake
#     sku_id: Snowflake
#     application_id: Snowflake
#     user_id: Snowflake
#     type: int
#     deleted: bool
#     starts_at: str  # ISO8601 timestamp
#     ends_at: str  # ISO8601 timestamp
#     guild_id: Snowflake
#
#
# class Interaction:
#     id: Snowflake
#     application_id: Snowflake
#     type: InteractionType
#     data: InteractionData
#     guild_id: Snowflake
#     channel: PartialChannel
#     channel_id: Snowflake
#     member: GuildMember
#     user: GuildMember
#     token: str
#     version: int
#     message: Message
#     app_permissions: str
#     locale: str
#     guild_locale: str
#     entitelements: list[Entitlement]