from typing import List, Optional
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
from grid import Grid, MAX_VALUE
from algo import Algorithm
from config import Config

def visualize_algo(config: Config, algorithm: Algorithm, save_path: Optional[str] = None) -> None:
    generated_grid, transformed_grid = algorithm.execute(config)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Visualize generated grid
    if generated_grid is not None:
        if len(generated_grid.shape) == 1:
            # For 1D grids, show as horizontal bar
            ax1.imshow(generated_grid.data.reshape(1, -1), cmap='viridis',
                      vmin=0, vmax=MAX_VALUE, aspect='auto')
        else:
            ax1.imshow(generated_grid.data, cmap='viridis', vmin=0, vmax=MAX_VALUE)
        ax1.set_title('Generated Grid')
        ax1.set_xlabel(f'Shape: {generated_grid.shape}')

    # Visualize transformed grid
    if transformed_grid is not None:
        if len(transformed_grid.shape) == 1:
            # For 1D grids, show as horizontal bar
            ax2.imshow(transformed_grid.data.reshape(1, -1), cmap='viridis',
                      vmin=0, vmax=MAX_VALUE, aspect='auto')
        else:
            ax2.imshow(transformed_grid.data, cmap='viridis', vmin=0, vmax=MAX_VALUE)
        ax2.set_title('Transformed Grid')
        ax2.set_xlabel(f'Shape: {transformed_grid.shape}')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def visualize_multiple_algos(config: Config, algorithms: List[Algorithm], rows: Optional[int] = None, cols: Optional[int] = None) -> None:
    # Auto-derive rows and cols if not provided
    if rows is None or cols is None:
        num_algorithms = len(algorithms)
        if num_algorithms == 0:
            rows, cols = 1, 1
        else:
            cols = int(num_algorithms ** 0.5)
            if cols * cols < num_algorithms:
                cols += 1
            rows = (num_algorithms + cols - 1) // cols  # Equivalent to ceil(num_algorithms / cols)

    # Create grids directory if it doesn't exist
    os.makedirs('grids', exist_ok=True)

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"grids/algos_{timestamp}.jpg"

    fig, axes = plt.subplots(rows, cols * 2, figsize=(cols * 8, rows * 4))

    for i, algorithm in enumerate(algorithms[:rows * cols]):
        config.logger.info(f"\n--- Processing Algorithm {i+1} ---")
        generated_grid, transformed_grid = algorithm.execute(config)

        row = i // cols
        col = i % cols

        # Generated grid subplot
        gen_ax = axes[row, col * 2] if rows > 1 else axes[col * 2]
        if generated_grid is not None:
            if len(generated_grid.shape) == 1:
                gen_ax.imshow(generated_grid.data.reshape(1, -1), cmap='viridis',
                            vmin=0, vmax=MAX_VALUE, aspect='auto')
            else:
                gen_ax.imshow(generated_grid.data, cmap='viridis', vmin=0, vmax=MAX_VALUE)
            gen_ax.set_title(f'Gen {i+1}: {generated_grid.shape}')
        gen_ax.set_xticks([])
        gen_ax.set_yticks([])

        # Transformed grid subplot
        trans_ax = axes[row, col * 2 + 1] if rows > 1 else axes[col * 2 + 1]
        if transformed_grid is not None:
            if len(transformed_grid.shape) == 1:
                trans_ax.imshow(transformed_grid.data.reshape(1, -1), cmap='viridis',
                              vmin=0, vmax=MAX_VALUE, aspect='auto')
            else:
                trans_ax.imshow(transformed_grid.data, cmap='viridis', vmin=0, vmax=MAX_VALUE)
            trans_ax.set_title(f'Trans {i+1}: {transformed_grid.shape}')
        trans_ax.set_xticks([])
        trans_ax.set_yticks([])

    # Hide unused subplots
    for i in range(len(algorithms), rows * cols):
        row = i // cols
        col = i % cols
        axes[row, col * 2].set_visible(False)
        axes[row, col * 2 + 1].set_visible(False)

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', format='jpg')
    plt.close()

    print(f"Visualization saved to {filename}")

def visualize_grid(config: Config, grid: Grid, title: str = "Grid") -> None:
    plt.figure(figsize=(6, 6))

    if len(grid.shape) == 1:
        plt.imshow(grid.data.reshape(1, -1), cmap='viridis',
                  vmin=0, vmax=MAX_VALUE, aspect='auto')
    else:
        plt.imshow(grid.data, cmap='viridis', vmin=0, vmax=MAX_VALUE)

    plt.title(f'{title} - Shape: {grid.shape}')
    plt.colorbar()
    plt.show()
