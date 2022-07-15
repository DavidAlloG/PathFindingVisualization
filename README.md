# PathFindingVisualization
Visualization of the process followed by A* algorithm to find the shortest path.

#### Author: David García Allo
#### Date: 11/07/2022

#### Description
we can visualize all the neighbors considered and the moves made by the A* algorithm in the process of finding the shortest path between the start and end points.
The first left-click adds the start point in the Node clicked, the next one the end point and the rest of clicks create barriers, it means non-available nodes.


The right-click resets the node clicked (white node)


The key 'space' initializes the algorithm.


The key 'c' clears the all the grid (if algo is not running).


Pygame module needed

#### Ideas to improve
- Maybe add some buttons that allows to execute algorithm, reset and kill the process
- Add more path finding algorithms
