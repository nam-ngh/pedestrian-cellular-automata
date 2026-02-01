from modules.grid import HexGrid
from modules.visualiser import HexGridVisualizer
import random
import numpy as np

def main(exits: str, seed: int=42):
    '''
    Square hall simulations. Saves resulting GIFs to .outputs

    :params exits: "opposite" or "quarter"
    '''
    random.seed(seed)
    np.random.seed(seed)

    ##### SIMULATION PARAMETERS #####
    num_pedestrians = 500
    cartesian_side = 22.36
    w, h = 106, 106 # parent grid dimensions
    ##### _____________________ #####

    # BUILD HALL
    # Cartesian Area = 500
    # Cartesian Square side len ~ 22.36
    # With flat-top orientation, side-len = 22.36/(0.2*1.5), long-len = 22.36/(0.2*np.sqrt(3))

    grid = HexGrid(w, h)

    hex_side_len = int(cartesian_side // (0.2*1.5))
    hex_long_len = int(cartesian_side // (0.2*np.sqrt(3)))
    grid.build_square_hall(side_len=hex_side_len, long_len=hex_long_len)
    
    # Set exits
    exit_doors = []
    mid_w, mid_h = w // 2, h // 2

    q_3oclock = mid_w + int(hex_side_len // 2)
    q_9oclock = mid_w - int(hex_side_len // 2)
    q_12oclock = mid_w

    r_3oclock = mid_h - int(hex_side_len // 4) # calibration for paralellogram
    r_9oclock = mid_h + int(hex_side_len // 4) # calibration for paralellogram
    r_12oclock = mid_h + int(hex_long_len // 2)

    if exits == 'opposite':
        # RHS doors
        exit_doors.append((q_3oclock, r_3oclock + 1))
        exit_doors.append((q_3oclock, r_3oclock + 0))
        exit_doors.append((q_3oclock, r_3oclock - 1))
        # LHS doors
        exit_doors.append((q_9oclock, r_9oclock + 1))
        exit_doors.append((q_9oclock, r_9oclock + 0))
        exit_doors.append((q_9oclock, r_9oclock - 1))
        save_path = 'outputs/square_opposite_sim.gif'
    elif exits == 'quarter':
        # RHS doors
        exit_doors.append((q_3oclock, r_3oclock + 1))
        exit_doors.append((q_3oclock, r_3oclock + 0))
        exit_doors.append((q_3oclock, r_3oclock - 1))
        # Top doors
        exit_doors.append((q_12oclock + 1, r_12oclock - 1//2))
        exit_doors.append((q_12oclock + 0, r_12oclock - 0//2))
        exit_doors.append((q_12oclock - 1, r_12oclock - (-1//2)))
        save_path = 'outputs/square_quarter_sim.gif'
    else:
        raise ValueError('Exits must be "opposite" or "quarter"')

    if len(exit_doors) > 0:
        grid.set_targets(exit_doors)

    # Initialise pedestrian randomly
    added = 0
    for _ in range(num_pedestrians * 5):
        if added >= num_pedestrians:
            break
        q = random.randint(1, w - 2)
        r = random.randint(1, h - 2)
        if grid.add_pedestrian(q, r, ped_id=added):
            added += 1
    
    print(f"Created grid {w}x{h}")
    print(f"Added {len(grid.pedestrians)} pedestrians")
    
    # Create visualizer and save animation
    viz = HexGridVisualizer(grid)
    viz.save_animation(frames=120, save_path=save_path)

if __name__ == "__main__":
    main(exits='quarter')
    main(exits='opposite')