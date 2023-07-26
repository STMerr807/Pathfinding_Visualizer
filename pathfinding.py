"""
pathfinding.py
==============

This module contains the implementation of the A* pathfinding algorithm.
"""

import heapq
import math
from queue import PriorityQueue
from enum import Enum

# Define global data structures used in A* algorithm.
# OPEN_SET is a PriorityQueue used to keep track of nodes to be evaluated.
# G_SCORE and F_SCORE are dictionaries used to keep track of the cost to reach each node.
OPEN_SET = PriorityQueue()
G_SCORE = {}
F_SCORE = {}


# An Enum class representing the possible states a node can be in.
# Each state is represented as an integer.
class State(Enum):
    EMPTY = 0  # The node is not part of the path and does not contain an obstacle.
    START = 1  # The node is the starting point of the path.
    END = 2  # The node is the end point of the path.
    BARRIER = 3  # The node contains an obstacle, so it cannot be part of the path.
    OPEN = 4  # The node is being considered as a possible step in the path.
    CLOSED = 5  # The node has already been considered as a possible step in the path.
    PATH = 6  # The node is part of the final path.


class Node:
    """
    Represents a node or cell on the grid.

    Attributes:
    - row (int): The row position of the node on the grid.
    - col (int): The column position of the node on the grid.
    - neighbors (list): A list of neighboring nodes.
    - state (State): The current state of the node (e.g., EMPTY, START, END, etc.)
    """

    def __init__(self, row, col):
        """
        Initializes a Node with a specified row and column position.

        Args:
        - row (int): The row position of the node.
        - col (int): The column position of the node.
        """
        self.row = row
        self.col = col
        self.neighbors = []
        self.state = State.EMPTY

    def get_node_state(self):
        """
        Returns the current state of the node in lowercase string format.

        Returns:
        - str: The current state of the node.
        """
        return self.state.name.lower()

    def get_pos(self):
        """
        Returns the position of the node as a tuple.

        Returns:
        - tuple: The (row, col) position of the node.
        """
        return self.row, self.col

    def set_node_state(self, state):
        """
        Sets the state of the node.

        Args:
        - state (State): The state to set the node to.

        Raises:
        - AssertionError: If the provided state is not an instance of the State Enum.
        """
        assert isinstance(state, State)
        self.state = state

    def update_neighbors(self, grid, total_rows):
        """
        Updates the list of neighbors for the node based on its position on the grid and
        the state of adjacent nodes. Nodes that are barriers are excluded from the neighbors list.

        Args:
        - grid (list of list of Node): The grid containing all the nodes.
        - total_rows (int): The total number of rows in the grid.
        """
        self.neighbors = []

        # Check the Down neighbor
        if self.row < total_rows - 1 and not (grid[self.row + 1][self.col].get_node_state() == "barrier"):
            self.neighbors.append(grid[self.row + 1][self.col])

        # Check the Up neighbor
        if self.row > 0 and not (grid[self.row - 1][self.col].get_node_state() == "barrier"):
            self.neighbors.append(grid[self.row - 1][self.col])

        # Check the Right neighbor
        if self.col < total_rows - 1 and not (grid[self.row][self.col + 1].get_node_state() == "barrier"):
            self.neighbors.append(grid[self.row][self.col + 1])

        # Check the Left neighbor
        if self.col > 0 and not (grid[self.row][self.col - 1].get_node_state() == "barrier"):
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        """
        Overrides the default less-than method.
        This is used by the PriorityQueue to compare nodes.

        Returns:
        - bool: Always returns False. Nodes are not directly comparable by default.
        """
        return False


def heuristic(p1, p2, dist_method):
    """
    Calculates the heuristic based on the chosen distance metric.

    Args:
    - p1 (tuple): A tuple representing the (x, y) coordinates of the first point.
    - p2 (tuple): A tuple representing the (x, y) coordinates of the second point.
    - dist_method (str): A string representing the chosen distance metric.
        It can be 'manhattan', 'euclidean', or 'chebyshev'.

    Returns:
    - float: The calculated distance between p1 and p2 based on the chosen distance metric.

    Raises:
    - ValueError: If the provided dist_method is not 'manhattan', 'euclidean', or 'chebyshev'.
    """
    x1, y1 = p1
    x2, y2 = p2
    if dist_method == 'manhattan':
        return abs(x1 - x2) + abs(y1 - y2)  # Return Manhattan distance
    elif dist_method == 'euclidean':
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)  # Return Euclidean distance
    elif dist_method == 'chebyshev':
        return max(abs(x1 - x2), abs(y1 - y2))  # Return Chebyshev distance
    else:
        raise ValueError(f"Invalid dist_method: {dist_method}")


def reconstruct_path(came_from, current):
    """
    Reconstructs the path from the start node to the end node based on the came_from dictionary.

    Args:
    - came_from (dict): A dictionary where the key is a node
        and the value is the node that we came from to reach the key node.
    - current (Node): The end node of the path.

    This function modifies the state of the nodes in the path to PATH.
    """
    while current in came_from:
        current = came_from[current]  # Get current node
        current.set_node_state(State.PATH)  # Make current node part of the path


def algorithm(grid, start, end, move_cost, dist_method):
    """
    Implements the A* pathfinding algorithm.

    Args:
    - grid (list of list of Node): The grid containing all the nodes.
    - start (Node): The starting node.
    - end (Node): The ending node.
    - move_cost (int or float): The cost of moving from one node to an adjacent one.
    - dist_method (str): The distance metric to use for the heuristic.
        It can be 'manhattan', 'euclidean', or 'chebyshev'.

    Returns:
    - list of Node: The list of visited nodes.

    Raises:
    - ValueError: If the provided dist_method is not 'manhattan', 'euclidean', or 'chebyshev'.
    """
    # Initialize open set, g score, f score, and count
    open_set = []
    G_SCORE.clear()
    F_SCORE.clear()
    count = 0
    heapq.heappush(open_set, (0, count, start))  # Add start node to open set
    came_from = {}  # Keeps track of where each node came from

    # Initialize g score and f score of all nodes to infinity
    for row in grid:
        for node in row:
            G_SCORE[node] = float("inf")
            F_SCORE[node] = float("inf")

    # Set g score of start node to 0 and its f score to the heuristic
    G_SCORE[start] = 0
    F_SCORE[start] = heuristic(start.get_pos(), end.get_pos(), dist_method)

    open_set_hash = {start}  # Keep track of items in PriorityQueue
    visited = []  # List of visited nodes

    # Main loop of the A* algorithm
    while open_set:
        # Pop the node with the lowest f score from the open set
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        # If the current node is the end node, reconstruct the path and return
        if current == end:
            reconstruct_path(came_from, end)
            end.set_node_state(State.END)
            visited.append(current)
            return visited  # Return the list of visited nodes

        # Consider each neighbor of the current node
        for neighbor in current.neighbors:
            temp_g_score = G_SCORE[current] + move_cost  # The cost of the path through the current node to the neighbor

            # If this path to the neighbor is better than any previous one, record it
            if temp_g_score < G_SCORE[neighbor]:
                came_from[neighbor] = current
                G_SCORE[neighbor] = temp_g_score  # Update g score
                F_SCORE[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos(),
                                                             dist_method)  # Update f score

                # If the neighbor is not in the open set, add it
                if neighbor not in open_set_hash:
                    count += move_cost
                    heapq.heappush(open_set, (F_SCORE[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_node_state(State.OPEN)  # Make neighbor open
                    visited.append(neighbor)  # Add neighbor to visited nodes

        # Once we're done considering all of the neighbors of the current node, mark it as closed
        if current != start:  # If current node is not start node
            current.set_node_state(State.CLOSED)

        # Uncomment below statements to visualize the algorithm, comment out the return statement after them
        # yield current  # Yield current node

    # If no path is found, yield all visited nodes
    # for row in grid:
    #     for node in row:
    #         yield node

    # If no path is found, return the list of visited nodes
    return visited
