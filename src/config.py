import os
from logger import Logger

class Config:
    def __init__(self, debug_level: int, logger: Logger):
        self.debug_level = debug_level
        self.logger = logger

def mkConfig() -> Config:
    debug_level = int(os.environ.get('DEBUG', '0'))
    logger = Logger(debug_level)
    return Config(debug_level, logger)