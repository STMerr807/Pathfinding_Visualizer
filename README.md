# A* Pathfinding Visualizer

This project is a Python-based visualizer for the A* pathfinding algorithm. Created as a hobby/learning project, it's designed as an educational tool to help users understand how the algorithm works by providing a visual representation of the process. The design for this visualizer was inspired by various online resources and tutorials, and the project represents a compilation and customization of those ideas into a cohesive and interactive application.

## Features

- Interactive GUI to set start point, end point, and barriers.
- Ability to step through the pathfinding process visually.
- Customizable heuristic functions: Manhattan, Euclidean, and Chebyshev.
- Heap-based open set for improved efficiency.
- Modular design of pathfinding logic for easy adaptation to other projects.

## Files

- `main.py`: This is the main file that runs the GUI and visualizer. It also handles the interaction between the user and the grid.
- `pathfinding.py`: This file contains the implementation of the A* algorithm, the Node class, and other pathfinding-related logic.

## Usage

1. Run `main.py` to start the visualizer.
2. Left click on a grid cell to set the start point (first click), the end point (second click), and to draw barriers (subsequent clicks).
3. Right click on a grid cell to erase it.
4. Press `SPACE` to start the pathfinding algorithm.
5. Press `c` to clear the grid and start over.

## Requirements

Python 3.x is required to run this project.
