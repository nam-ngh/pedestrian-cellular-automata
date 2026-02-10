# Pedestrian Simulations with Hexagonal Cellular Automata (CA)

This project aims to model pedestrian dynamics by CA simulations. The desired application is to determine a large hall design that facilitates the most effective evacuation in an emergency scenario. However, the core rule-based simulation [modules](https://github.com/nam-ngh/pedestrian-cellular-automata/tree/main/modules) can be used to simulate almost any situation involving pedestrian dynamics.

### Method

There are 3 main possible grid types for CA: triangular - square - hexagonal grids. Hexagonal grids were chosen here due to their ability to closely simulate a pedestrian's isotropic movement in continuous space and reduce directional bias. On the grid, each cell can be of any 4 states at a given time step t: obstacle - empty - target - pedestrian. Obstacles and target cells tend to be fixed in place. Walls can be built as a series of obstacles. Pedestrians move according to the following rule base:

- Loop through each of 6 neighbouring cells in random order. If a cell with distance closer to the target is encountered, label this as the best cell.
- Rationality: 80% of the time the pedestrian will proceed to choose this best cell, progressing closer to the target. 20% they will panic and choose a random cell next to them
- If no best cells are found, they will move randomly 
- If a pedestrian is completely surrounded by obstacle/other pedestrians, they will stay put.

The distance to the target cells for each cell is stored in a static field, computed by breadth-first-search (BFS). The default grid is a parallelogram and uses axial coordinates for traversal.

### Results
Simulation sequences for each designed scenario are stored in [outputs](https://github.com/nam-ngh/pedestrian-cellular-automata/tree/main/outputs). With the following constraints:

- Hall Capacity: 500
- Hall Area: 500m2
- Maximum 2 exit doors, each 1.2m in width,

a [circular hall](https://github.com/nam-ngh/pedestrian-cellular-automata/blob/main/outputs/circle_opposite_sim.gif) design with opposite exits and NO obstacle placements were found to be the most effective for evacuation. Though square and circular halls offer quite similar evacuation time performance, the circular design was chosen for savings in construction materials due to smaller perimeter with a fixed area.
