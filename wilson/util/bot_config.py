import discord
import yaml


class ConfigBotSettingsPresence:
    activity_name: str
    activity_type: discord.ActivityType
    status: discord.Status


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
    debug_mode: bool
    default_presence: ConfigBotSettingsPresence
    embed_footer: str
    prefix: str
    release: ConfigBotSettingsRelease


class ConfigIntents:
    bans: bool
    emojis: bool
    guilds: bool
    members: bool
    message_content: bool
    messages: bool
    reactions: bool
    voice_states: bool


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

            default_presence = ConfigBotSettingsPresence()
            default_presence.activity_name = conf_settings_presence['activity_name']
            default_presence.activity_type = conf_settings_presence['activity_type']
            default_presence.status = conf_settings_presence['status']

            release = ConfigBotSettingsRelease()
            release.version = ConfigBotSettingsRelease.Version()

            release.update_name = conf_settings_release['update_name']
            release.version.major = conf_settings_release['version']['major']
            release.version.minor = conf_settings_release['version']['minor']
            release.version.patch = conf_settings_release['version']['patch']
            release.version.suffix = conf_settings_release['version']['suffix']

            self._settings = ConfigBotSettings()
            self._settings.debug_mode = bool(conf_settings['debug_mode'])
            self._settings.default_presence = default_presence
            self._settings.embed_footer = conf_settings['embed_footer']
            self._settings.prefix = conf_settings['prefix']
            self._settings.release = release

            self._intents = ConfigIntents()
            self._intents.bans = bool(conf_intents['bans'])
            self._intents.emojis = bool(conf_intents['emojis'])
            self._intents.guilds = bool(conf_intents['guilds'])
            self._intents.members = bool(conf_intents['members'])
            self._intents.message_content = bool(conf_intents['message_content'])
            self._intents.messages = bool(conf_intents['messages'])
            self._intents.reactions = bool(conf_intents['reactions'])
            self._intents.voice_states = conf_intents['voice_states']

    @property
    def bot_settings(self) -> ConfigBotSettings:
        return self._settings

    @property
    def intents(self) -> ConfigIntents:
        return self._intents
