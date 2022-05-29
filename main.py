import asyncio
import sys
import util.logger as log

from discord import Intents
from discord.ext import commands
from util.bot_config import BotConfig


class Wilson:
    def __init__(self, owner_id: int, token: str, config_path: str = 'config.yml'):
        self._config = BotConfig(config_path)

        intents_conf = self.config.intents
        bot_intents = Intents(
            bans=intents_conf.bans,
            emojis=intents_conf.emojis,
            guilds=intents_conf.guilds,
            members=intents_conf.members,
            message_content=intents_conf.message_content,
            messages=intents_conf.messages,
            reactions=intents_conf.reactions,
            voice_states=intents_conf.voice_states
        )
        self.bot = commands.Bot(command_prefix=self.config.bot_settings.prefix, case_insensitive=True,
                                owner_id=owner_id,
                                intents=bot_intents)
        self.bot.remove_command('help')
        self.token = token

    def run(self):
        try:
            log.log_info('Starting bot', self.config.bot_settings.debug_mode)
            self.bot.run(self.token)
        except Exception as exc:
            log.log_error('An error occurred while running the bot', exc)

    @property
    def config(self) -> BotConfig:
        return self._config


def main():
    if len(sys.argv) < 3:
        raise RuntimeError('Missing arguments')

    try:
        id = int(sys.argv[1])
        tok = sys.argv[2]

        bot = Wilson(id, tok)
        bot.run()
    except Exception as exc:
        log.log_critical('Could not start the bot', exc)
        exit(1)


if __name__ == '__main__':
    main()
