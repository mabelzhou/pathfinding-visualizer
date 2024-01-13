# Pathfinding Visualizer
This is a simple pathfinding visualizer implemented in Python using the Pygame library. It allows you to interactively create mazes, set start and end points, and visualize pathfinding algorithms.

## Tools Used 
- Python 3.11.6
- Pygame 

## Usage
- **LMB**: Place start and end nodes, create barriers
- **RMB**: Remove start/end nodes and barriers
- **SPACE**: Start program
- **ENTER**: Clear the board
- **A Star Button**: Use A* algorithm (enabled by default)
- **Dijkstra Button**: Use Dijkstra's algorithm (WIP)

### Node Colours
- **Empty Node**: White
- **Start Node**: Orange
- **End Node**: Turquoise
- **Barrier Node**: Black
- **Open Set Nodes**: Green
- **Closed Set Nodes**: Red
- **Path Nodes**: Yellow

## Screenshots
![sample](https://github.com/mabelzhou/pathfinding-visualizer/assets/135676782/78874ab4-8ec6-49b7-8afd-6310cdfa3976)  
![sample2](https://github.com/mabelzhou/pathfinding-visualizer/assets/135676782/44a806d7-329e-4098-a8b3-5fb7760e1e9f)

![demo2](https://github.com/mabelzhou/pathfinding-visualizer/assets/135676782/87216973-892a-442c-ae67-8dd3b6488037)
![demo](https://github.com/mabelzhou/pathfinding-visualizer/assets/135676782/3eb2e8b9-5ebc-43be-9a47-825fa0fe95f3)
![demo3](https://github.com/mabelzhou/pathfinding-visualizer/assets/135676782/ab780397-fa23-4e03-b6df-ea83d8e03d1d)

## Notes
- The heuristic used is Euclidean distance.
- Diagonal movements are allowed with a diagonal cost of approximately 1.4.

## Getting Started
1. Install the required dependencies ```pip install pygame```
2. Open the project directory and run the script: ```python pathfinder.py```

## License
This project is licensed under MIT License. 

## Acknowledgements
This project is a modified version of Tim Ruscica's (https://github.com/techwithtim) tutorial
