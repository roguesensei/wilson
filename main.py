import os
import shutil
import sys

from wilson.bot import Wilson
from wilson.util.logger import *


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    if not os.path.exists(f'{dir_path}/config.py'):
        try:
            shutil.copyfile(f'{dir_path}/res/config.def.txt', f'{dir_path}config.py')
            print('Generated config.py file, please configure bot before re-running')
        except Exception as exc:
            log_critical('An error occurred generating config.py file, consider writing manually', exc)
            exit(1)
    else:
        try:
            from config import bot_config
            bot = Wilson(bot_config)
            bot.run_bot()
        except Exception as exc:
            log_critical('Could not start the bot', exc)
            exit(1)


if __name__ == '__main__':
    main()
