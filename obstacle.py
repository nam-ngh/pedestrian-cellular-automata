import numpy as np
import random

from modules.grid import HexGrid
from modules.visualiser import HexGridVisualizer
from config import NUM_PEOPLE, HEX_GRID_W, HEX_GRID_H, CARTESIAN_R

def main(seed: int=42):
    '''
    Circular hall simulations with obstacles. Saves resulting GIFs to .outputs
    '''
    random.seed(seed)
    np.random.seed(seed)

    ##### BUILD HALL #####
    grid = HexGrid(HEX_GRID_W, HEX_GRID_H)
    print(f"Created grid {HEX_GRID_W}x{HEX_GRID_H}")

    hall_radius = int(CARTESIAN_R//(0.2*1.616)) # hall radius in hex
    grid.build_circular_hall(hall_radius)
    print(f'Built Circle Hall with radius {hall_radius} hex')

    # Add exits
    long_radius = int(CARTESIAN_R // (0.2*np.sqrt(3)))

    grid.build_long_doors(r_centre_offset=long_radius, width=3) # 12oclock door
    grid.build_long_doors(r_centre_offset=-long_radius-1, width=3) # 6oclock door
    save_path = 'outputs/obs_sim.gif'

    # Define and add obstacles
    q1, r1 = HEX_GRID_W//2, HEX_GRID_H//2 + long_radius - 3
    q2, r2 = HEX_GRID_W//2, HEX_GRID_H//2 - long_radius + 2
    obstacles = [
        grid.calibrate(q1, r1),
        grid.calibrate(q1, r1-1),
        grid.calibrate(q2, r2),
        grid.calibrate(q2, r2+1),
    ]
    for q,r in obstacles:
        grid.add_obstacle(q,r)
    
    ##### ADD PEOPLE #####
    grid.random_init_pedestrian(num_ped=NUM_PEOPLE)
    print(f"Added {len(grid.pedestrians)} pedestrians")
    
    # Create visualizer and save animation
    viz = HexGridVisualizer(grid)
    viz.save_animation(frames=120, save_path=save_path)

if __name__ == "__main__":
    main()