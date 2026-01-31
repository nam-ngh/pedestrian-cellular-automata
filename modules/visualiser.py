import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from matplotlib.animation import FuncAnimation

from modules.grid import CellState, HexGrid

class HexGridVisualizer:
    """Visualize the hexagonal grid with animation."""
    
    COLORS = {
        CellState.EMPTY: "#ede5c2",
        CellState.PEDESTRIAN: "#30529C",
        CellState.OBSTACLE: '#1a1a1a',
        CellState.TARGET: '#ff6b6b',
    }
    
    def __init__(self, grid: HexGrid, hex_size: float = 0.2):
        self.grid = grid
        self.hex_size = hex_size
        self.fig = None
        self.ax = None
        self.patches = None
        self.text = None
        self.total_reached = 0
        self.end_frame = '-'
    
    def setup_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 10), dpi=80)
        self.fig.patch.set_facecolor('#1a1a1a')
        self.ax.set_facecolor('#1a1a1a')
        
        self.patches = {}
        for q in range(self.grid.width):
            for r in range(self.grid.height):
                x, y = self.grid.axial_to_cartesian(q, r, self.hex_size)
                state = self.grid.cells[q, r]
                
                hexagon = RegularPolygon(
                    (x, y),
                    numVertices=6,
                    radius=self.hex_size,
                    orientation=np.pi/6,
                    facecolor=self.COLORS[state],
                    edgecolor='#1a1a1a',
                    linewidth=0.5
                )
                self.ax.add_patch(hexagon)
                self.patches[(q, r)] = hexagon
        
        self.text = self.ax.text(
            0.02, 0.98, '', 
            transform=self.ax.transAxes,
            fontsize=12,
            color='white',
            verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#2d2d2d', alpha=0.8)
        )
        
        self.ax.set_aspect('equal')
        self.ax.autoscale()
        self.ax.axis('off')
        
        self.ax.set_title(
            'Hexagonal CA: Pedestrian Dynamics',
            fontsize=16,
            color='white',
            pad=20
        )
        
        plt.tight_layout()
        
    def update_display(self, frame: int):
        reached = self.grid.step()
        self.total_reached += reached
        
        for q in range(self.grid.width):
            for r in range(self.grid.height):
                state = self.grid.cells[q, r]
                self.patches[(q, r)].set_facecolor(self.COLORS[state])
        
        if len(self.grid.pedestrians) == 0 and self.end_frame == '-':
            self.end_frame = str(frame)

        self.text.set_text(
            f'Frame: {frame}\n'
            f'End frame: {self.end_frame}\n'
            f'Pedestrians: {len(self.grid.pedestrians)}\n'
            f'Reached target: {self.total_reached}'
        )
        
        return list(self.patches.values()) + [self.text]
    
    def save_animation(self, frames: int = 100, interval: int = 200, save_path: str = 'outputs/sim.gif'):
        self.setup_plot()
        anim = FuncAnimation(
            self.fig,
            self.update_display,
            frames=frames,
            interval=interval,
            blit=False,
            repeat=False
        )
        
        print(f"Simulating and saving animation to {save_path}...")
        anim.save(save_path, writer='pillow', fps=1000/interval)
        plt.close()
        print("Done!")