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
        
    def get_neighbors(self, q: int, r: int) -> list[tuple[int, int]]:
        neighbors = []
        for dq, dr in self.DIRECTIONS:
            nq, nr = q + dq, r + dr
            if 0 <= nq < self.width and 0 <= nr < self.height:
                neighbors.append((nq, nr))
        return neighbors
    
    def set_targets(self, q: int, r: int):
        self.targets.append((q, r))
        self.cells[q, r] = CellState.TARGET
        self.static_field = self._compute_static_field()
    
    def _compute_static_field(self) -> np.ndarray:
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
    
    def _get_best_move(self, ped: Pedestrian) -> tuple[int, int] | None:
        """Find the neighboring cell closest to target that's available."""
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
        
        # If no cells are closer to target, move randomly from available cells
        if best_cell is None and available_cells:
            best_cell = random.choice(available_cells)
        
        return best_cell
    
    def step(self) -> int:
        # Sort pedestrians by distance to target (closest first gets priority)
        self.pedestrians.sort(key=lambda p: self.static_field[p.q, p.r])
        
        reached_target = []
        
        for ped in self.pedestrians:
            best_move = self._get_best_move(ped)
            nq, nr = best_move
            
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