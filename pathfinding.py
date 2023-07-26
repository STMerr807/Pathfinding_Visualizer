import heapq
from queue import PriorityQueue
from enum import Enum


OPEN_SET = PriorityQueue()
G_SCORE = {}
F_SCORE = {}


# State updater class
class State(Enum):
    EMPTY = 0
    START = 1
    END = 2
    BARRIER = 3
    OPEN = 4
    CLOSED = 5
    PATH = 6


# Node class
class Node:
    def __init__(self, row, col):
        self.row = row  # Row position of node
        self.col = col  # Column position of node
        self.neighbors = []  # List of neighbor nodes
        self.state = State.EMPTY  # Stores what state the node is currently in

    # Check the state of the node
    def get_node_state(self):
        return self.state.name.lower()

    # Get position
    def get_pos(self):
        return self.row, self.col

    # Set the state of the node
    def set_node_state(self, state):
        assert isinstance(state, State)
        self.state = state

    # Update neighbors
    def update_neighbors(self, grid, total_rows):
        self.neighbors = []
        if self.row < total_rows - 1 and not (grid[self.row + 1][self.col].get_node_state() == "barrier"):  # Down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not (grid[self.row - 1][self.col].get_node_state() == "barrier"):  # Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < total_rows - 1 and not (grid[self.row][self.col + 1].get_node_state() == "barrier"):  # Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not (grid[self.row][self.col - 1].get_node_state() == "barrier"):  # Left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


# Heuristic function using chosen distance metric
def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return max(abs(x1 - x2), abs(y1 - y2))  # Return Chebyshev distance
    # return abs(x1 - x2) + abs(y1 - y2)  # Return Manhattan distance
    # return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)  # Return Euclidean distance


def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]  # Get current node
        current.set_node_state(State.PATH)  # Make current node path


# A* algorithm
def algorithm(grid, start, end):
    # Initialize open set, g score, f score, and count
    open_set = []
    G_SCORE.clear()
    F_SCORE.clear()
    count = 0
    heapq.heappush(open_set, (0, count, start))  # Add start node to open set
    came_from = {}  # Keeps track of where a node came from

    for row in grid:
        for node in row:
            # Initialize g score and f score of all nodes to infinity
            G_SCORE[node] = float("inf")
            F_SCORE[node] = float("inf")

    G_SCORE[start] = 0  # Set g score of start node to 0
    F_SCORE[start] = heuristic(start.get_pos(), end.get_pos())  # Set f score of start node to heuristic
    open_set_hash = {start}  # Keep track of items in PriorityQueue
    visited = []  # List of visited nodes

    while open_set:
        current = heapq.heappop(open_set)[2]  # Get current node
        open_set_hash.remove(current)  # Remove current node from open set

        if current == end:
            reconstruct_path(came_from, end)  # Reconstruct path
            end.set_node_state(State.END)  # Make end node
            visited.append(current)  # Add current node to visited list
            return visited  # Return list of visited nodes

        for neighbor in current.neighbors:
            temp_g_score = G_SCORE[current] + 1  # Calculate temp g score
            if temp_g_score < G_SCORE[neighbor]:
                came_from[neighbor] = current
                G_SCORE[neighbor] = temp_g_score  # Update g score
                F_SCORE[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())  # Update f score
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (F_SCORE[neighbor], count, neighbor))  # Add neighbor to open set
                    open_set_hash.add(neighbor)  # Add neighbor to open set hash
                    neighbor.set_node_state(State.OPEN)  # Make neighbor open
                    visited.append(neighbor)  # Add neighbor to visited nodes

        if current != start:  # If current node is not start node
            current.set_node_state(State.CLOSED)  # Make current node closed

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
