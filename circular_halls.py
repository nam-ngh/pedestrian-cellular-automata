from modules.grid import HexGrid
from modules.visualiser import HexGridVisualizer
import random
import numpy as np

def main(exits: str, seed: int=42):
    '''
    Circular hall simulations. Saves resulting GIFs to .outputs

    :params exits: "opposite" or "quarter"
    '''
    random.seed(seed)
    np.random.seed(seed)

    ##### SIMULATION PARAMETERS #####
    cartesian_r = 18
    hall_radius = 56
    w, h = 128, 128
    mid_w, mid_h = w // 2, h // 2
    num_pedestrians = 500
    ##### _____________________ #####

    # BUILD HALL
    # Cartesian Area = 1000
    # Cartesian Radius ~ 18
    # Avg axial Radius = 18/(0.2*1.616) ~ 56
    # (hex_size = 0.2, 1 cartesian ~ 1 axial x 1.616)
    # With flat-top orientation, side-r = 18/(0.2*1.5), long-r = 18/(0.2*np.sqrt(3))

    grid = HexGrid(w, h)
    grid.build_circular_hall(hall_radius)
    # Set exits
    exit_doors = []
    side_radius = int(cartesian_r // (0.2*1.5)) + 1
    long_radius = int(cartesian_r // (0.2*np.sqrt(3))) + 1

    q_3oclock = mid_w + side_radius
    q_9oclock = mid_w - side_radius
    q_12oclock = mid_w

    r_3oclock = mid_h - int(side_radius//2) # calibration for paralellogram
    r_9oclock = mid_h + int(side_radius//2) # calibration for paralellogram
    r_12oclock = mid_h + long_radius

    if exits == 'opposite':
        # RHS doors
        exit_doors.append((q_3oclock, r_3oclock + 2))
        exit_doors.append((q_3oclock, r_3oclock + 1))
        exit_doors.append((q_3oclock, r_3oclock + 0))
        exit_doors.append((q_3oclock, r_3oclock - 1))
        exit_doors.append((q_3oclock, r_3oclock - 2))
        # LHS doors
        exit_doors.append((q_9oclock, r_9oclock + 2))
        exit_doors.append((q_9oclock, r_9oclock + 1))
        exit_doors.append((q_9oclock, r_9oclock + 0))
        exit_doors.append((q_9oclock, r_9oclock - 1))
        exit_doors.append((q_9oclock, r_9oclock - 2))
        save_path = 'outputs/circle_opposite_sim.gif'
    elif exits == 'quarter':
        # RHS doors
        exit_doors.append((q_3oclock, r_3oclock + 2))
        exit_doors.append((q_3oclock, r_3oclock + 1))
        exit_doors.append((q_3oclock, r_3oclock + 0))
        exit_doors.append((q_3oclock, r_3oclock - 1))
        exit_doors.append((q_3oclock, r_3oclock - 2))
        # Top doors
        exit_doors.append((q_12oclock + 2, r_12oclock - 2//2))
        exit_doors.append((q_12oclock + 1, r_12oclock - 1//2))
        exit_doors.append((q_12oclock + 0, r_12oclock - 0//2))
        exit_doors.append((q_12oclock - 1, r_12oclock - (-1//2)))
        exit_doors.append((q_12oclock - 2, r_12oclock - (-2//2)))
        save_path = 'outputs/circle_quarter_sim.gif'
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
    viz.save_animation(frames=180, save_path=save_path)

if __name__ == "__main__":
    main(exits='quarter')
    main(exits='opposite')