import yaml


class ConfigBotSettings:
    def __init__(self, debug_mode: bool, embed_footer: str, prefix: str):
        self._debug_mode = debug_mode
        self._embed_footer = embed_footer
        self._prefix = prefix

    @property
    def debug_mode(self) -> bool:
        return self._debug_mode

    @property
    def embed_footer(self) -> str:
        return self._embed_footer

    @property
    def prefix(self) -> str:
        return self._prefix


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
        conf = yaml.safe_load(open(path))

        conf_settings = conf['bot_settings']
        conf_intents = conf['intents']

        self._settings = ConfigBotSettings(
            debug_mode=conf_settings['debug_mode'],
            embed_footer=conf_settings['embed_footer'],
            prefix=conf_settings['prefix']
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
