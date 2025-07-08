from typing import List, Dict, Any, Optional
from ops import Op, OpType
from grid import Grid
from config import Config

class Algorithm:
    def __init__(self, generate_ops: List[Op], transform_ops: List[Op]):
        self.generate_ops = generate_ops
        self.transform_ops = transform_ops
        
        # Validate that generate starts with init and transform starts with reshape
        if not generate_ops or generate_ops[0].op_type != OpType.INIT:
            raise ValueError("Generate operations must begin with an INIT op")
        
        if not transform_ops or transform_ops[0].op_type != OpType.RESHAPE:
            raise ValueError("Transform operations must begin with a RESHAPE op")
        
        # Validate that generate ops after init are all CHANGE ops
        for op in generate_ops[1:]:
            if op.op_type != OpType.CHANGE:
                raise ValueError("Generate operations after INIT must be CHANGE ops")
        
        # Validate that transform ops after reshape are all CHANGE ops
        for op in transform_ops[1:]:
            if op.op_type != OpType.CHANGE:
                raise ValueError("Transform operations after RESHAPE must be CHANGE ops")
    
    def execute(self, config: Config) -> tuple[Optional[Grid], Optional[Grid]]:
        # Initialize context
        context: Dict[str, Any] = {"GRID": None, "SELECTED": None}
        
        # Execute generation phase
        config.logger.info("=== GENERATION PHASE ===")
        for op in self.generate_ops:
            config.logger.info(f"Executing: {op.name} ({op.op_type.value})")
            op.execute(config, context)
        
        generated_grid = context["GRID"].copy() if context["GRID"] else None
        
        # Execute transformation phase
        config.logger.info("=== TRANSFORMATION PHASE ===")
        for op in self.transform_ops:
            config.logger.info(f"Executing: {op.name} ({op.op_type.value})")
            op.execute(config, context)
        
        transformed_grid = context["GRID"] if context["GRID"] else None
        
        return generated_grid, transformed_grid
    
    def __repr__(self) -> str:
        gen_names = [op.name for op in self.generate_ops]
        trans_names = [op.name for op in self.transform_ops]
        return f"Algorithm(generate={gen_names}, transform={trans_names})"