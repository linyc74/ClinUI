from abc import ABC
from datetime import datetime
from .schema import Schema


class Settings:

    outdir: str
    debug: bool

    def __init__(self, outdir: str, debug: bool):
        self.outdir = outdir
        self.debug = debug


class Logger:

    INFO: str = 'INFO'
    DEBUG: str = 'DEBUG'

    name: str
    level: str

    def __init__(self, name: str, level: str):
        self.name = name
        assert level in [self.INFO, self.DEBUG]
        self.level = level

    def info(self, msg: str):
        print(f'{self.name}\tINFO\t{datetime.now()}', flush=True)
        print(msg + '\n', flush=True)

    def debug(self, msg: str):
        if self.level == self.INFO:
            return
        print(f'{self.name}\tDEBUG\t{datetime.now()}', flush=True)
        print(msg + '\n', flush=True)


class Processor(ABC):

    settings: Settings
    outdir: str
    debug: bool

    logger: Logger

    def __init__(self, settings: Settings):

        self.settings = settings
        self.outdir = settings.outdir
        self.debug = settings.debug

        self.logger = Logger(
            name=self.__class__.__name__,
            level=Logger.DEBUG if self.debug else Logger.INFO
        )
