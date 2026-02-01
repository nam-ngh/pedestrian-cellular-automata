import numpy as np
from collections import deque
from dataclasses import dataclass
from enum import IntEnum
import random

class CellState(IntEnum):
    EMPTY = 0
    PEDESTRIAN = 1
    OBSTACLE = 2
    TARGET = 3

@dataclass
class Pedestrian:
    q: int
    r: int
    id: int = 0

class HexGrid:
    """Hexagonal grid using axial coordinates."""
    
    DIRECTIONS = [
        (1, 0), (1, -1), (0, -1),
        (-1, 0), (-1, 1), (0, 1)
    ]
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells = np.zeros((width, height), dtype=int)
        self.pedestrians: list[Pedestrian] = []
        self.static_field = None
        self.targets = []
    
    @staticmethod
    def axial_to_cartesian(q: int, r: int, size: float = 1) -> tuple[float, float]:
        '''
        Converts hex-grid coordinates to cartesian coordinates, defaults hex-size = 1
        '''
        x = size * (3/2 * q)
        y = size * (np.sqrt(3)/2 * q + np.sqrt(3) * r)
        return x, y
    
    def get_neighbors(self, q: int, r: int) -> list[tuple[int, int]]:
        '''
        Returns a list of neighbours in random order for any cell (q, r)
        '''
        neighbors = []
        directions = self.DIRECTIONS.copy()
        random.shuffle(directions)
        for dq, dr in directions:
            nq, nr = q + dq, r + dr
            if 0 <= nq < self.width and 0 <= nr < self.height:
                neighbors.append((nq, nr))
        return neighbors
    
    def _compute_static_field(self) -> np.ndarray:
        '''
        Computes distance of every cell from the nearest target by breadth-first search
        '''

        field = np.full((self.width, self.height), np.inf)
        queue = deque()
        for tq, tr in self.targets:
            field[tq, tr] = 0
            queue.append((tq, tr))
        
        # BFS from all targets simultaneously
        while queue:
            q, r = queue.popleft()
            for nq, nr in self.get_neighbors(q, r):
                if field[nq, nr] == np.inf and self.cells[nq, nr] != CellState.OBSTACLE:
                    field[nq, nr] = field[q, r] + 1
                    queue.append((nq, nr))
        return field
    
    ##### GRID CONSTRUCTION FUNCTIONS #####
    def calibrate(self, q: int, r: int) -> tuple[int, int]:
        """
        Convert 'visual' coordinates to axial coordinates.
        Compensates for the parallelogram skew so we can think
        in terms of screen positions (rectangular grid).
        
        Args:
            q: Horizontal position (same in both systems)
            r: Vertical position (as if on rectangular grid)
        
        Returns:
            (q, adjusted_r) in true axial coordinates
        """
        mid_q = self.width // 2
        q_diff = q - mid_q
        r_adjusted = r - q_diff // 2
        return q, r_adjusted

    def set_targets(self, targets):
        for t in targets:
            q, r = t
            self.targets.append((q,r))
            self.cells[q, r] = CellState.TARGET

        print(f'{len(targets)} targets set!')
        self.static_field = self._compute_static_field()
    
    def add_pedestrian(self, q: int, r: int, ped_id: int = 0) -> bool:
        if self.cells[q, r] == CellState.EMPTY:
            ped = Pedestrian(q=q, r=r, id=ped_id)
            self.pedestrians.append(ped)
            self.cells[q, r] = CellState.PEDESTRIAN
            return True
        return False
    
    def add_obstacle(self, q: int, r: int):
        if self.cells[q, r] == CellState.EMPTY:
            self.cells[q, r] = CellState.OBSTACLE

    def build_circular_hall(self, radius: int):
        centre_q, centre_r = int(self.width/2), int(self.height/2)
        centre_x, centre_y = self.axial_to_cartesian(centre_q, centre_r)
        for q in range(self.width):
            for r in range(self.height):
                cell_x, cell_y = self.axial_to_cartesian(q, r)
                dist = np.sqrt((cell_x - centre_x)**2 + (cell_y - centre_y)**2)
                if (radius * 1.616) < dist:
                    self.add_obstacle(q,r)

    def build_square_hall(self, side_len: int, long_len: int):
        centre_q, centre_r = int(self.width/2), int(self.height/2)
        half_side = int(side_len // 2)
        half_long = int(long_len // 2)
        for q in range(self.width):
            for r in range(self.height):
                # Compensate for axial skew at every column 
                # (not using adjusted func for clarity)
                q_diff = q - centre_q
                r_calibration = - int(q_diff // 2)
                
                outside_q = (
                    q < centre_q - half_side
                ) or (
                    q > centre_q + half_side
                )
                outside_r = (
                    r < centre_r - half_long + r_calibration
                ) or (
                    r > centre_r + half_long + r_calibration
                )
                
                if outside_q or outside_r:
                    self.add_obstacle(q, r)

    def build_side_doors(self, q_centre_offset: int, width: int):
        mid_w, mid_h = self.width // 2, self.height // 2
        q, r = self.calibrate(mid_w + q_centre_offset, mid_h)
        min_r = r - width // 2
        door_cells = []
        for i in range(width):
            door_cells.append((q, min_r + i))
        
        if door_cells:
            self.set_targets(door_cells)
            print(f'Added {width} side door cells at q = {q_centre_offset} from centre')

    def build_long_doors(self, r_centre_offset: int, width: int):
        mid_w, mid_h = self.width // 2, self.height // 2
        min_q = mid_w - width // 2
        door_cells = []
        for i in range(width):
            q, r = self.calibrate(min_q + i, mid_h + r_centre_offset)
            door_cells.append((q, r))
        
        if door_cells:
            self.set_targets(door_cells)
            print(f'Added {width} long door cells at r = {r_centre_offset} from centre')
    
    def random_init_pedestrian(self, num_ped: int, seed: int=42):
        # Initialise pedestrian randomly
        random.seed(seed)
        added = 0
        for _ in range(num_ped * 5):
            if added >= num_ped:
                break
            q = random.randint(1, self.width - 2)
            r = random.randint(1, self.height - 2)
            if self.add_pedestrian(q, r, ped_id=added):
                added += 1
    
    ##### SIMULATION LOGIC #####
    def _get_move(self, ped: Pedestrian, rationality: float=0.8) -> tuple[int, int] | None:
        """
        Moving logic
        
        :params ped: a Pedestrian
        :params rationality: the chance a person makes a rational step. 
            0 is completely irrational
            1 is perfectly rational
        """
        q, r = ped.q, ped.r
        best_cell = None
        curr_dist = self.static_field[q, r]
        available_cells = []
        
        for nq, nr in self.get_neighbors(q, r):
            # First check if cell is empty or target
            if self.cells[nq, nr] == CellState.EMPTY or self.cells[nq, nr] == CellState.TARGET:
                available_cells.append((nq, nr))
                distance = self.static_field[nq, nr]
                # If cell is closer to target, move to this cell
                if distance < curr_dist:
                    curr_dist = distance
                    best_cell = (nq, nr)
                    break
        
        if best_cell is not None and random.random() < rationality:
            return best_cell
        
        if available_cells:
            return random.choice(available_cells)
    
        return None
    
    def step(self) -> int:
        # Sort pedestrians by distance to target (closest first gets priority)
        self.pedestrians.sort(key=lambda p: self.static_field[p.q, p.r])
        
        reached_target = []
        for ped in self.pedestrians:
            next_move = self._get_move(ped)
            if next_move is None:
                continue
            elif next_move:
                nq, nr = next_move

            # Check if reached target
            if self.cells[nq, nr] == CellState.TARGET:
                self.cells[ped.q, ped.r] = CellState.EMPTY
                reached_target.append(ped)
                continue
            
            # Move pedestrian
            self.cells[ped.q, ped.r] = CellState.EMPTY
            ped.q, ped.r = nq, nr
            self.cells[ped.q, ped.r] = CellState.PEDESTRIAN
        
        for ped in reached_target:
            self.pedestrians.remove(ped)
        
        return len(reached_target)