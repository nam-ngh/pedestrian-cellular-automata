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
    target_q = grid_width - 2
    target_r = grid_height // 2
    grid.set_target(target_q, target_r)
    
    # Add wall with gap (optional)
    wall_x = grid_width // 2
    for r in range(3, grid_height - 3):
        if r != grid_height // 2 and r != grid_height // 2 + 1:
            grid.add_obstacle(wall_x, r)
    
    # Add pedestrians on the left side
    num_pedestrians = 30
    added = 0
    for _ in range(num_pedestrians * 5):
        if added >= num_pedestrians:
            break
        q = random.randint(1, grid_width // 3)
        r = random.randint(1, grid_height - 2)
        if grid.add_pedestrian(q, r, ped_id=added):
            added += 1
    
    print(f"Created grid {grid_width}x{grid_height}")
    print(f"Added {len(grid.pedestrians)} pedestrians")
    print(f"Target at ({target_q}, {target_r})")
    
    # Create visualizer and save animation
    viz = HexGridVisualizer(grid)
    viz.save_animation(frames=100, interval=200, save_path='outputs/sim.gif')


if __name__ == "__main__":
    main()