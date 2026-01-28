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
        self.target = None
        
    def get_neighbors(self, q: int, r: int) -> list[tuple[int, int]]:
        neighbors = []
        for dq, dr in self.DIRECTIONS:
            nq, nr = q + dq, r + dr
            if 0 <= nq < self.width and 0 <= nr < self.height:
                neighbors.append((nq, nr))
        return neighbors
    
    def set_target(self, q: int, r: int):
        self.target = (q, r)
        self.cells[q, r] = CellState.TARGET
        self.static_field = self._compute_static_field()
    
    def _compute_static_field(self) -> np.ndarray:
        field = np.full((self.width, self.height), np.inf)
        field[self.target] = 0
        queue = deque([self.target])
        
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
    
    def _compute_transition_probs(self, ped: Pedestrian) -> dict:
        q, r = ped.q, ped.r
        probs = {}
        k_s = 2.0  # Sensitivity parameter
        
        for nq, nr in self.get_neighbors(q, r):
            if self.cells[nq, nr] == CellState.EMPTY:
                distance = self.static_field[nq, nr]
                if distance < np.inf:
                    probs[(nq, nr)] = np.exp(k_s * (self.static_field[q, r] - distance))
            elif self.cells[nq, nr] == CellState.TARGET:
                probs[(nq, nr)] = np.exp(k_s * 2)
        
        if probs:
            total = sum(probs.values())
            probs = {k: v / total for k, v in probs.items()}
        
        return probs
    
    def step(self) -> int:
        random.shuffle(self.pedestrians)
        reached_target = []
        
        for ped in self.pedestrians:
            probs = self._compute_transition_probs(ped)
            
            if not probs:
                continue
            
            cells = list(probs.keys())
            weights = list(probs.values())
            chosen = random.choices(cells, weights=weights)[0]
            
            if self.cells[chosen[0], chosen[1]] == CellState.TARGET:
                self.cells[ped.q, ped.r] = CellState.EMPTY
                reached_target.append(ped)
                continue
            
            self.cells[ped.q, ped.r] = CellState.EMPTY
            ped.q, ped.r = chosen
            self.cells[ped.q, ped.r] = CellState.PEDESTRIAN
        
        for ped in reached_target:
            self.pedestrians.remove(ped)
        
        return len(reached_target)