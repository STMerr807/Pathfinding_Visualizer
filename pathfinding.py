from queue import PriorityQueue


# Node class
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row  # Row position of node
        self.col = col  # Column position of node
        self.x = row * width  # X position of node
        self.y = col * width  # Y position of node
        self.color = WHITE  # Color of node
        self.neighbors = []  # List of neighbor nodes
        self.width = width  # Width of node
        self.total_rows = total_rows  # Total rows in grid

    # Get position
    def get_pos(self):
        return self.row, self.col

    # Check if node is closed
    def is_closed(self):
        return self.color == RED

    # Check if node is open
    def is_open(self):
        return self.color == GREEN

    # Check if node is barrier
    def is_barrier(self):
        return self.color == BLACK

    # Check if node is start
    def is_start(self):
        return self.color == ORANGE

    # Check if node is an end node
    def is_end(self):
        return self.color == CYAN

    # Reset node
    def reset(self):
        self.color = WHITE

    # Make start node
    def make_start(self):
        self.color = ORANGE

    # Make node closed
    def make_closed(self):
        self.color = RED

    # Make node open
    def make_open(self):
        self.color = GREEN

    # Make node barrier
    def make_barrier(self):
        self.color = BLACK

    # Make node end
    def make_end(self):
        self.color = CYAN

    # Make node path
    def make_path(self):
        self.color = YELLOW

    # Draw node
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # Update neighbors
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # Down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # Left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


# Heuristic function using Manhattan distance
def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]  # Get current node
        current.make_path()  # Make current node path
        draw()  # Draw display window


# A* algorithm
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()  # Create an open set
    open_set.put((0, count, start))  # Add start node to open set
    came_from = {}  # Keeps track of where a node came from
    g_score = {node: float("inf") for row in grid for node in row}  # Tracks shortest dist from start to current node
    g_score[start] = 0  # Set start node g score to 0
    f_score = {node: float("inf") for row in grid for node in row}  # F score
    f_score[start] = heuristic(start.get_pos(), end.get_pos())  # Set start node f score to heuristic

    open_set_hash = {start}  # Keep track of items in PriorityQueue

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  # Get current node
        open_set_hash.remove(current)  # Remove current node from open set

        if current == end:
            reconstruct_path(came_from, end, draw)  # Reconstruct path
            end.make_end()  # Make end node
            return True  # If current node is end node, return true

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
                    neighbor.make_open()  # Make neighbor open

        draw()  # Draw display window

        if current != start:  # If current node is not start node
            current.make_closed()  # Make current node closed
