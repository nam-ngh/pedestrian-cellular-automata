import numpy as np
import random
from modules.grid import HexGrid
from modules.visualiser import HexGridVisualizer
from config import HEX_GRID_W, HEX_GRID_H, CARTESIAN_SIDE, NUM_PEOPLE

def main(exits: str, seed: int=42):
    '''
    Square hall simulations. Saves resulting GIFs to .outputs

    :params exits: "opposite" or "quarter"
    '''
    random.seed(seed)
    np.random.seed(seed)

    ##### BUILD HALL #####
    grid = HexGrid(HEX_GRID_W, HEX_GRID_H)
    print(f"Created grid {HEX_GRID_W}x{HEX_GRID_H}")

    # Convert cartesian len to hex len for flat-top orientation
    hex_side_len = int(CARTESIAN_SIDE // (0.2*1.5))
    hex_long_len = int(CARTESIAN_SIDE // (0.2*np.sqrt(3)))

    grid.build_square_hall(side_len=hex_side_len, long_len=hex_long_len)
    print(f'Built Square Hall with size {hex_side_len} x {hex_long_len}')

    # Add exits
    if exits == 'opposite':
        grid.build_side_doors(q_centre_offset=int(hex_side_len // 2) + 1, width=3) # 3oclock door
        grid.build_side_doors(q_centre_offset=-(int(hex_side_len // 2) + 1), width=3) # 9oclock door
        save_path = 'outputs/square_opposite_sim.gif'
    if exits == 'quarter':
        grid.build_side_doors(q_centre_offset=int(hex_side_len // 2) + 1, width=3) # 3oclock door
        grid.build_long_doors(r_centre_offset=int(hex_long_len // 2) + 1, width=3) # 12oclock door
        save_path = 'outputs/square_quarter_sim.gif'
    
    ##### ADD PEOPLE #####
    grid.random_init_pedestrian(num_ped=NUM_PEOPLE)
    print(f"Added {len(grid.pedestrians)} pedestrians")
    
    # Create visualizer and save animation
    viz = HexGridVisualizer(grid)
    viz.save_animation(frames=120, save_path=save_path)

if __name__ == "__main__":
    main(exits='quarter')
    main(exits='opposite')