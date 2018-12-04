from enum import Enum


class Level(Enum):
    INFO = 1
    DEBUG = 2
    WARNING = 3
    ERROR = 4
    CONSOLE = 5


class Log(object):
    def __init__(self, module, level, message):
        return

