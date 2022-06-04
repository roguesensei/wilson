import discord
import yaml


class ConfigBotSettingsPresence:
    def __init__(self, activity_name: str, activity_type: discord.ActivityType, status: discord.Status):
        self._activity_name = activity_name
        self._activity_type = activity_type
        self._status = status

    @property
    def activity_name(self) -> str:
        return self._activity_name

    @property
    def activity_type(self) -> discord.ActivityType:
        return self._activity_type

    @property
    def status(self) -> discord.Status:
        return self._status


class ConfigBotSettingsRelease:
    class Version:
        major: int
        minor: int
        patch: int
        suffix: str

        def __str__(self):
            return f'V{self.major}.{self.minor}.{self.patch} {self.suffix}'

    update_name: str
    version: Version


class ConfigBotSettings:
    def __init__(self, debug_mode: bool, default_presence: ConfigBotSettingsPresence, embed_footer: str, prefix: str,
                 release: ConfigBotSettingsRelease):
        self._debug_mode = debug_mode
        self._default_presence = default_presence
        self._embed_footer = embed_footer
        self._prefix = prefix
        self._release = release

    @property
    def debug_mode(self) -> bool:
        return self._debug_mode

    @property
    def default_presence(self) -> ConfigBotSettingsPresence:
        return self._default_presence

    @property
    def embed_footer(self) -> str:
        return self._embed_footer

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def release(self) -> ConfigBotSettingsRelease:
        return self._release


class ConfigIntents:
    def __init__(self, bans: bool, emojis: bool, guilds: bool, members: bool, message_content: bool, messages: bool,
                 reactions: bool, voice_states: bool):
        self._bans = bans
        self._emojis = emojis
        self._guilds = guilds
        self._members = members
        self._message_content = message_content
        self._messages = messages
        self._reactions = reactions
        self._voice_states = voice_states

    @property
    def bans(self) -> bool:
        return self._bans

    @property
    def emojis(self) -> bool:
        return self._emojis

    @property
    def guilds(self) -> bool:
        return self._guilds

    @property
    def members(self) -> bool:
        return self._members

    @property
    def message_content(self) -> bool:
        return self._message_content

    @property
    def messages(self) -> bool:
        return self._messages

    @property
    def reactions(self) -> bool:
        return self._reactions

    @property
    def voice_states(self) -> bool:
        return self._voice_states


class BotConfig:
    def __init__(self, path: str):
        self.__load_config(path)

    def __load_config(self, path: str) -> None:
        with open(path, 'r') as f:
            conf = yaml.safe_load(f)

            conf_settings = conf['bot_settings']
            conf_settings_presence = conf_settings['default_presence']
            conf_settings_release = conf_settings['release']
            conf_intents = conf['intents']

            default_presence = ConfigBotSettingsPresence(
                activity_name=conf_settings_presence['activity_name'],
                activity_type=conf_settings_presence['activity_type'],
                status=conf_settings_presence['status']
            )
            release = ConfigBotSettingsRelease()
            release.version = ConfigBotSettingsRelease.Version()

            release.update_name = conf_settings_release['update_name']
            release.version.major = conf_settings_release['version']['major']
            release.version.minor = conf_settings_release['version']['minor']
            release.version.patch = conf_settings_release['version']['patch']
            release.version.suffix = conf_settings_release['version']['suffix']

            self._settings = ConfigBotSettings(
                debug_mode=conf_settings['debug_mode'],
                default_presence=default_presence,
                embed_footer=conf_settings['embed_footer'],
                prefix=conf_settings['prefix'],
                release=release
            )
            self._intents = ConfigIntents(
                bans=bool(conf_intents['bans']),
                emojis=bool(conf_intents['emojis']),
                guilds=bool(conf_intents['guilds']),
                members=bool(conf_intents['members']),
                message_content=bool(conf_intents['message_content']),
                messages=bool(conf_intents['messages']),
                reactions=bool(conf_intents['reactions']),
                voice_states=conf_intents['voice_states']
            )

    @property
    def bot_settings(self) -> ConfigBotSettings:
        return self._settings

    @property
    def intents(self) -> ConfigIntents:
        return self._intents
