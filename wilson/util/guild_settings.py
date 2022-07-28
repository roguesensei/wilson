import discord
import json
import os

default_welcome_message = 'Welcome to **[!server]** [@user], enjoy your stay!'


class GuildSettings:
    def __init__(self, guild_id: int, welcome_actions: bool = False, welcome_message: str = default_welcome_message,
                 welcome_channel_id: int = 0, autorole_id: int = 0):
        self.guild_id = guild_id
        self.welcome_actions = welcome_actions
        self.welcome_message = welcome_message
        self.welcome_channel_id = welcome_channel_id
        self.autorole_id = autorole_id

    def save_settings(self) -> None:
        if not os.path.exists('.wilson/guilds/'):
            os.mkdir('.wilson/guilds/')

        with open(f'.wilson/guilds/{self.guild_id}.json', 'w+') as f:
            f.write(json.dumps(self.__dict__))

    @property
    def opted_in(self) -> bool:
        return os.path.exists(f'.wilson/guilds/{self.guild_id}.json')

    @staticmethod
    def get_settings(guild_id: int):
        guild = GuildSettings(guild_id)
        if guild.opted_in:
            with open(f'.wilson/guilds/{guild_id}.json') as f:
                obj = json.loads(f.read())

                guild.welcome_actions = bool(obj['welcome_actions'])
                guild.welcome_message = obj['welcome_message']
                guild.welcome_channel_id = int(obj['welcome_channel_id'])
                guild.autorole_id = int(obj['autorole_id'])
        return guild

    @staticmethod
    def delete_settings(guild_id: int):
        os.remove(f'.wilson/guilds/{guild_id}.json')

