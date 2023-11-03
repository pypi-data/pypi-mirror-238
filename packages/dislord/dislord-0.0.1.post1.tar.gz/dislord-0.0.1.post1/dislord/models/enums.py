from enum import Enum


class ApplicationCommandType(Enum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3


class ApplicationCommandOptionType(Enum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11


class Locale(Enum):
    INDONESIAN = 'id'
    DANISH = 'da'
    GERMAN = 'de'
    BRITISH_ENGLISH = 'en-GB'
    AMERICAN_ENGLISH = 'en-US'
    SPAIN_SPANISH = 'es-ES'
    FRENCH = 'fr'
    CROATIAN = 'hr'
    ITALIAN = 'it'
    LITHUANIAN = 'lt'
    HUNGARIAN = 'hu'
    DUTCH = 'nl'
    NORWEGIAN = 'no'
    POLISH = 'pl'
    BRAZIL_PORTUGUESE = 'pt-BR'
    ROMANIAN = 'ro'
    FINNISH = 'fi'
    SWEDISH = 'sv-SE'
    VIETNAMESE = 'vi'
    TURKISH = 'tr'
    CZECH = 'cs'
    GREEK = 'el'
    BULGARIAN = 'bg'
    RUSSIAN = 'ru'
    UKRAINIAN = 'uk'
    HINDI = 'hi'
    THAI = 'th'
    CHINESE = 'zh-CN'
    JAPANESE = 'ja'
    TAIWAN_CHINESE = 'zh-TW'
    KOREAN = 'ko'

    def __str__(self) -> str:
        return self.value


class ChannelType(Enum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_ANNOUNCEMENT = 5
    ANNOUNCEMENT_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY = 14
    GUILD_FORUM = 15
    GUILD_MEDIA = 16


class InteractionType(Enum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5