import pygame
from queue import PriorityQueue


# Node class
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row  # Row position of node
        self.col = col  # Column position of node
        self.x = row * width  # X position of node
        self.y = col * width  # Y position of node
        self.state = "empty"  # Stores what state the node is currently in
        self.neighbors = []  # List of neighbor nodes
        self.width = width  # Width of node
        self.total_rows = total_rows  # Total rows in grid

    # Check the state of the node
    def get_node_state(self):
        return self.state

    # Get position
    def get_pos(self):
        return self.row, self.col

    # Set the state of the node
    def set_node_state(self, state):
        self.state = state

    # Update neighbors
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not (grid[self.row + 1][self.col].get_node_state() == "barrier"):  # Down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not (grid[self.row - 1][self.col].get_node_state() == "barrier"):  # Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not (grid[self.row][self.col + 1].get_node_state() == "barrier"):  # Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not (grid[self.row][self.col - 1].get_node_state() == "barrier"):  # Left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


# Heuristic function using Manhattan distance
def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]  # Get current node
        current.set_node_state('path')  # Make current node path


# A* algorithm
def algorithm(grid, start, end):
    count = 0
    open_set = PriorityQueue()  # Create an open set
    open_set.put((0, count, start))  # Add start node to open set
    came_from = {}  # Keeps track of where a node came from
    g_score = {node: float("inf") for row in grid for node in row}  # Tracks shortest dist from start to current node
    g_score[start] = 0  # Set start node g score to 0
    f_score = {node: float("inf") for row in grid for node in row}  # F score
    f_score[start] = heuristic(start.get_pos(), end.get_pos())  # Set start node f score to heuristic

    open_set_hash = {start}  # Keep track of items in PriorityQueue

    visited = []  # List of visited nodes

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  # Get current node
        open_set_hash.remove(current)  # Remove current node from open set

        if current == end:
            reconstruct_path(came_from, end)  # Reconstruct path
            end.set_node_state('end')  # Make end node
            visited.append(current)  # Add current node to visited list
            return visited  # Return list of visited nodes

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1  # Calculate temp g score

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score  # Update g score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())  # Update f score
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))  # Add neighbor to open set
                    open_set_hash.add(neighbor)  # Add neighbor to open set hash
                    neighbor.set_node_state('open')  # Make neighbor open
                    visited.append(neighbor)  # Add neighbor to visited nodes

        if current != start:  # If current node is not start node
            current.set_node_state('closed')  # Make current node closed

        """
        To visualize the algorithm
        uncomment the statements that follow
        and comment out the return statement after them
        """
        # yield current  # Yield current node

    # for row in grid:
    #     for node in row:
    #         yield node  # If no path is found, yield all visited nodes

    return visited  # Return list of visited nodes if no path found
