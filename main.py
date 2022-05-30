import sys
import wilson.util.logger as log

from wilson.bot import Wilson


def main():
    if len(sys.argv) < 3:
        raise RuntimeError('Missing arguments')

    try:
        id = int(sys.argv[1])
        tok = sys.argv[2]

        bot = Wilson(id, tok)
        bot.run_bot()
    except Exception as exc:
        log.log_critical('Could not start the bot', exc)
        exit(1)


if __name__ == '__main__':
    main()
