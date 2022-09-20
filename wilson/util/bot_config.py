import discord

class BotPresence:
    activity_name: str
    activity_type: discord.ActivityType
    status: discord.Status


class BotRelease:
    update_name: str
    version: str


class BotSettings:
    owner_id: int
    bot_token: str
    debug_mode: bool
    default_presence: BotPresence
    embed_footer: str
    prefix: str
    release: BotRelease


class BotConfig:
    bot_settings: BotSettings
    intents: discord.Intents
