import time
import traceback

from enum import Enum
from termcolor import cprint


class LogLevel(Enum):
    MESSAGE = 0,
    INFO = 1,
    DEBUG = 2,
    WARNING = 3,
    ERROR = 4,
    CRITICAL = 5


def log(message: str, level: LogLevel = LogLevel.MESSAGE):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    cprint(f'{timestamp}', 'cyan', attrs=['bold'], end='')
    cprint(' >> ', 'magenta', end='')

    level_colour = 'white'
    level_text = '[MESSAGE]'

    if level == LogLevel.INFO:
        level_colour = 'blue'
        level_text = '[INFO]'
    elif level == LogLevel.DEBUG:
        level_colour = 'green'
        level_text = '[DEBUG]'
    elif level == LogLevel.WARNING:
        level_colour = 'yellow'
        level_text = '[WARNING]'
    elif level == LogLevel.ERROR:
        level_colour = 'red'
        level_text = '[ERROR]'
    elif level == LogLevel.CRITICAL:
        level_colour = 'white'
        level_text = '[CRITICAL]'

    if not level == LogLevel.CRITICAL:
        cprint(level_text, level_colour, attrs=['bold'], end='')
    else:
        cprint(level_text, level_colour, 'on_red', attrs=['bold'], end='')

    cprint(' >> ', 'magenta', end='')
    print(message)


def log_exception(exc: BaseException):
    cprint(f'{str(exc)}:', 'red', attrs=['bold'])
    tb = traceback.format_tb(exc.__traceback__, limit=-1)
    if tb is not None and len(tb) > 0:
        full = tb[0].split('\n')
        for line in full:
            cprint(text=line, color='red')


def log_message(message: str):
    log(message, LogLevel.MESSAGE)


def log_info(message: str, is_debug: bool = False):
    if is_debug:
        log(message, LogLevel.INFO)


def log_debug(message: str, is_debug: bool = False):
    if is_debug:
        log(message, LogLevel.DEBUG)


def log_warning(message: str):
    log(message, LogLevel.WARNING)


def log_error(message: str, exc: BaseException = None):
    log(message, LogLevel.ERROR)
    if exc is not None:
        log_exception(exc)


def log_critical(message: str, exc: BaseException = None):
    log(message, LogLevel.CRITICAL)
    if exc is not None:
        log_exception(exc)