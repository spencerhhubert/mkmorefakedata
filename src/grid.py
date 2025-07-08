from typing import Tuple, Optional
import numpy as np

MAX_VALUE = 255

class Grid:
    def __init__(self, shape: Tuple[int, ...], data: Optional[np.ndarray] = None):
        self.shape = shape
        if data is not None:
            self.data = data
        else:
            self.data = np.zeros(shape, dtype=int)
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def reshape(self, new_shape: Tuple[int, ...]) -> 'Grid':
        return Grid(new_shape, self.data.reshape(new_shape))
    
    def copy(self) -> 'Grid':
        return Grid(self.shape, self.data.copy())
    
    @property
    def size(self) -> int:
        return self.data.size
    
    def __repr__(self) -> str:
        return f"Grid(shape={self.shape}, data=\n{self.data})"