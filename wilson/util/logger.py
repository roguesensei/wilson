import time
import traceback

# from config import bot_config
from enum import Enum


class LogLevel(Enum):
    MESSAGE = 0,
    INFO = 1,
    DEBUG = 2,
    WARNING = 3,
    ERROR = 4,
    CRITICAL = 5


separator = '\033[95m>>\033[0m'
debug_mode = False


def set_debug_mode(value: bool) -> None:
    debug_mode = value


def log(message: str, level: LogLevel = LogLevel.MESSAGE):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    level_text = '[MESSAGE]'
    if level == LogLevel.INFO:
        level_text = '\033[34m[INFO]'
    elif level == LogLevel.DEBUG:
        level_text = '\033[32m[DEBUG]'
    elif level == LogLevel.WARNING:
        level_text = '\033[93m[WARNING]'
    elif level == LogLevel.ERROR:
        level_text = '\033[31m[ERROR]'
    elif level == LogLevel.CRITICAL:
        level_text = '\033[41m\033[93m[CRITICAL]'

    print(
        f'\033[36m{timestamp}\033[0m {separator} \033[01m{level_text}\033[0m {separator}\t{message}')


def log_exception(exc: BaseException):
    print('\033[01m\033[95m[PYERR]\033[0m')
    print(f'{separator} \033[01m\033[91m{str(exc)}\033[0m')
    tb = traceback.format_tb(exc.__traceback__, limit=-1)
    if tb is not None and len(tb) > 0:
        full = tb[0].split('\n')
        for line in full:
            print(f'{separator} \033[91m{line}\033[0m')
    print('\033[01m\033[95m[PYEND]\033[0m')


def log_message(message: str):
    log(message, LogLevel.MESSAGE)


def log_info(message: str):
    if debug_mode:
        log(message, LogLevel.INFO)


def log_debug(message: str):
    if debug_mode:
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
