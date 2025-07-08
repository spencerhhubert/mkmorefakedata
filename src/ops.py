from typing import Dict, Any, Callable, List, Tuple
from enum import Enum
import numpy as np
from grid import Grid, MAX_VALUE
from config import Config

class OpType(Enum):
    INIT = "init"
    RESHAPE = "reshape"
    CHANGE = "change"

class Op:
    def __init__(self, op_type: OpType, name: str, code: str):
        self.op_type = op_type
        self.name = name
        self.code = code
    
    def execute(self, config: Config, context: Dict[str, Any]) -> None:
        exec(self.code, {"np": np, "Grid": Grid, "MAX_VALUE": MAX_VALUE}, context)

# Operations are essentially snippets of python code that get ran in order.
# They run in a "sandbox" (same runtime as main program) as small self-contained
# python programs that stack on top of each other.
# 
# They can access the GRID variable (unknown shape) and SELECTED variable 
# (describes which cells are selected). They should account for None selected
# case and do nothing instead of crashing.
#
# Rules should generally be agnostic of what the values of the grid are or 
# the shape of the numpy array. For example, instead of setting values at 2,2 
# and 4,4, you might set values at two indices from the left and two from the 
# right so that it remains symmetrical.

# Init operations - initialize values on existing empty grid
INIT_OPS = [
    Op(OpType.INIT, "random_grid", """
GRID.data = np.random.randint(0, MAX_VALUE + 1, GRID.shape)
SELECTED = None
"""),
    
    Op(OpType.INIT, "zeros_grid", """
GRID.data = np.zeros(GRID.shape, dtype=int)
SELECTED = None
"""),
    
    Op(OpType.INIT, "checkerboard", """
if len(GRID.shape) >= 2:
    for i in range(GRID.shape[0]):
        for j in range(GRID.shape[1]):
            GRID.data[i, j] = MAX_VALUE if (i + j) % 2 == 0 else 0
else:
    for i in range(GRID.shape[0]):
        GRID.data[i] = MAX_VALUE if i % 2 == 0 else 0
SELECTED = None
""")
]

# Reshape operations - reshape grid according to rules
RESHAPE_OPS = [
    Op(OpType.RESHAPE, "noop_reshape", """
# No-op reshape - keeps grid as is
pass
"""),
    
    Op(OpType.RESHAPE, "flatten_reshape", """
total_size = GRID.size
GRID = GRID.reshape((total_size,))
""")
]

# Change operations - change values of GRID and SELECTED variables
CHANGE_OPS = [
    Op(OpType.CHANGE, "select_corners", """
if len(GRID.shape) >= 2:
    h, w = GRID.shape[:2]
    if h > 0 and w > 0:
        SELECTED = [(0, 0), (0, w-1), (h-1, 0), (h-1, w-1)]
    else:
        SELECTED = []
else:
    h = GRID.shape[0]
    if h > 1:
        SELECTED = [(0,), (h-1,)]
    elif h == 1:
        SELECTED = [(0,)]
    else:
        SELECTED = []
"""),
    
    Op(OpType.CHANGE, "increment_selected", """
if SELECTED is not None:
    for pos in SELECTED:
        if len(pos) == len(GRID.shape):
            current_val = GRID.data[pos]
            GRID.data[pos] = min(current_val + 50, MAX_VALUE)
"""),
    
    Op(OpType.CHANGE, "mirror_horizontal", """
if len(GRID.shape) >= 2:
    GRID.data = np.fliplr(GRID.data)
"""),
    
    Op(OpType.CHANGE, "add_border", """
if len(GRID.shape) >= 2:
    h, w = GRID.shape[:2]
    # Set border pixels to max value
    GRID.data[0, :] = MAX_VALUE
    GRID.data[-1, :] = MAX_VALUE
    GRID.data[:, 0] = MAX_VALUE
    GRID.data[:, -1] = MAX_VALUE
"""),
    
    Op(OpType.CHANGE, "center_cross", """
if len(GRID.shape) >= 2:
    h, w = GRID.shape[:2]
    mid_h, mid_w = h // 2, w // 2
    # Create cross pattern at center
    GRID.data[mid_h, :] = MAX_VALUE // 2
    GRID.data[:, mid_w] = MAX_VALUE // 2
"""),
    
    Op(OpType.CHANGE, "select_random", """
if len(GRID.shape) == 1:
    h = GRID.shape[0]
    if h > 0:
        num_select = min(3, h)
        indices = np.random.choice(h, num_select, replace=False)
        SELECTED = [(i,) for i in indices]
    else:
        SELECTED = []
elif len(GRID.shape) == 2:
    grid_shape = GRID.shape
    h, w = grid_shape[0], grid_shape[1]
    if h > 0 and w > 0:
        num_select = min(5, h * w)
        flat_indices = np.random.choice(h * w, num_select, replace=False)
        SELECTED = []
        for idx in flat_indices:
            row = idx // w
            col = idx % w
            SELECTED.append((row, col))
    else:
        SELECTED = []
else:
    SELECTED = []
""")
]

def get_random_ops(config: Config) -> Tuple[List[Op], List[Op]]:
    import random
    
    generate_ops = [random.choice(INIT_OPS)]
    generate_ops.extend([random.choice(CHANGE_OPS) for _ in range(np.random.randint(1, 4))])
    
    transform_ops = [random.choice(RESHAPE_OPS)]
    transform_ops.extend([random.choice(CHANGE_OPS) for _ in range(np.random.randint(1, 3))])
    
    return generate_ops, transform_ops