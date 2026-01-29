from modules.grid import HexGrid
from modules.visualiser import HexGridVisualizer
import random
import os

def main():
    # Create grid
    grid_width = 20
    grid_height = 15
    grid = HexGrid(grid_width, grid_height)
    
    # Set target on the right side
    target_q1 = grid_width - 2
    target_r1 = grid_height // 2
    target_q2 = 2
    target_r2 = grid_height // 2
    grid.set_targets(target_q1, target_r1)
    grid.set_targets(target_q2, target_r2)
    
    num_pedestrians = 90
    added = 0
    for _ in range(num_pedestrians * 5):
        if added >= num_pedestrians:
            break
        q = random.randint(1, grid_width - 2)
        r = random.randint(1, grid_height - 2)
        if grid.add_pedestrian(q, r, ped_id=added):
            added += 1
    
    print(f"Created grid {grid_width}x{grid_height}")
    print(f"Added {len(grid.pedestrians)} pedestrians")
    
    # Create visualizer and save animation
    viz = HexGridVisualizer(grid)
    viz.save_animation(frames=25, interval=200, save_path='outputs/sim.gif')


if __name__ == "__main__":
    main()