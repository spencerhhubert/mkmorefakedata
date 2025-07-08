from typing import List
import numpy as np
from algo import Algorithm
from ops import get_random_ops
from viz import visualize_algo, visualize_multiple_algos
from config import mkConfig

def create_random_algorithm(config) -> Algorithm:
    generate_ops, transform_ops = get_random_ops(config)
    return Algorithm(generate_ops, transform_ops)

def main():
    config = mkConfig()
    
    print("Data Generation Program")
    print("=" * 50)
    
    # Create a few random algorithms
    algorithms: List[Algorithm] = []
    
    for i in range(6):
        try:
            algo = create_random_algorithm(config)
            algorithms.append(algo)
            print(f"Algorithm {i+1}: {algo}")
        except Exception as e:
            print(f"Error creating algorithm {i+1}: {e}")
    
    print(f"\nCreated {len(algorithms)} algorithms")
    
    # Visualize individual algorithm
    if algorithms:
        print("\nVisualizing first algorithm individually...")
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        individual_filename = f"grids/individual_algo_{timestamp}.jpg"
        visualize_algo(config, algorithms[0], individual_filename)
        print(f"Individual algorithm saved to {individual_filename}")
    
    # Visualize multiple algorithms
    if len(algorithms) > 1:
        print("\nVisualizing all algorithms together...")
        visualize_multiple_algos(config, algorithms)

if __name__ == "__main__":
    main()