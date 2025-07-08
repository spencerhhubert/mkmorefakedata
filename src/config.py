import os
from typing import Sequence, Tuple
from logger import Logger

class Config:
    def __init__(self, debug_level: int, logger: Logger, shapes: Sequence[Tuple[int, ...]], save_individual: bool, save_algos: bool):
        self.debug_level = debug_level
        self.logger = logger
        self.shapes = shapes
        self.save_individual = save_individual
        self.save_algos = save_algos

def mkConfig(save_individual: bool = False, save_algos: bool = True) -> Config:
    debug_level = int(os.environ.get('DEBUG', '0'))
    logger = Logger(debug_level)
    shapes = [
        (16, 16)
    ]
    return Config(debug_level, logger, shapes, save_individual, save_algos)
