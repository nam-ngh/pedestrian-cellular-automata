import numpy as np
import random

from modules.grid import HexGrid
from modules.visualiser import HexGridVisualizer
from config import NUM_PEOPLE, HEX_GRID_W, HEX_GRID_H, CARTESIAN_R

def main(exits: str, seed: int=42):
    '''
    Circular hall simulations. Saves resulting GIFs to .outputs

    :params exits: "opposite" or "quarter"
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
    side_radius = int(CARTESIAN_R // (0.2*1.5))
    long_radius = int(CARTESIAN_R // (0.2*np.sqrt(3)))

    if exits == 'opposite':
        grid.build_side_doors(q_centre_offset=side_radius, width=3) # 3oclock door
        grid.build_side_doors(q_centre_offset=-side_radius, width=3) # 9oclock door
        save_path = 'outputs/circle_opposite_sim.gif'
    if exits == 'quarter':
        grid.build_side_doors(q_centre_offset=side_radius, width=3) # 3oclock door
        grid.build_long_doors(r_centre_offset=long_radius, width=3) # 12oclock door
        save_path = 'outputs/circle_quarter_sim.gif'
    
    ##### ADD PEOPLE #####
    grid.random_init_pedestrian(num_ped=NUM_PEOPLE)
    print(f"Added {len(grid.pedestrians)} pedestrians")
    
    # Create visualizer and save animation
    viz = HexGridVisualizer(grid)
    viz.save_animation(frames=120, save_path=save_path)

if __name__ == "__main__":
    main(exits='quarter')
    main(exits='opposite')