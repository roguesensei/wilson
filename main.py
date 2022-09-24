import os
import shutil
import sys
import wilson.util.logger as log
from wilson.bot import Wilson


def main():
    """Main runtime function
    """
    if not os.path.exists('config.py'):
        try:
            shutil.copyfile('res/config.def.txt', 'config.py')
            print('Generated config.py file, please configure bot before re-running')
        except Exception as exc:
            print('An error occurred generating config.py file, consider writing manually')
            log.log_critical('An error occurred generating config.py file, consider writing manually', exc)
            exit(1)
    else:
        from config import bot_config
        bot = Wilson(bot_config)
        try:
            bot.run_bot()
        except Exception as exc:
            log.log_critical('Could not start the bot', exc)
            exit(1)


if __name__ == '__main__':
    main()
