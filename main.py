import pygame

import pathfinding

# Set up the window
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# Colors
RED = (165, 40, 30)
GREEN = (75, 100, 25)
BLUE = (45, 55, 90)
YELLOW = (195, 170, 25)
WHITE = (240, 235, 210)
BLACK = (30, 25, 20)
PURPLE = (115, 60, 121)
ORANGE = (180, 105, 30)
GREY = (215, 210, 190)
CYAN = (70, 115, 145)


# Create the grid
def make_grid(rows, width):
    grid = []
    gap = width // rows  # Width of each node
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = pathfinding.Node(i, j, gap, rows)  # Create node
            grid[i].append(node)  # Add node to grid
    return grid


# Draw grid lines
def draw_grid(win, rows, width):
    gap = width // rows  # Width of each node
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))  # Horizontal lines
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))  # Vertical Lines


# Draw the display window
def draw(win, grid, rows, width):
    colors = {
        "empty": WHITE,
        "open": GREEN,
        "closed": RED,
        "barrier": BLACK,
        "start": ORANGE,
        "end": CYAN,
        "path": YELLOW,
    }

    win.fill(WHITE)  # Fill window with white
    for row in grid:
        for node in row:
            pygame.draw.rect(win, colors[node.state], (node.x, node.y, node.width, node.width))  # Draw node
    draw_grid(win, rows, width)  # Draw grid lines
    pygame.display.update()  # Update display


# Get node clicked on
def get_clicked_pos(pos, rows, width):
    gap = width // rows  # Width of each node
    y, x = pos  # Get position of mouse
    row = y // gap  # Get row of node
    col = x // gap  # Get column of node
    return row, col


# Main function
# noinspection PyUnresolvedReferences
def main(win, width):
    rows = 50  # Number of rows
    grid = make_grid(rows, width)  # Create grid
    start = None  # Start node
    end = None  # End node
    run = True  # Run flag

    # Main loop
    while run:
        draw(win, grid, rows, width)  # Draw display window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Quit if user closes window

            if pygame.mouse.get_pressed()[0]:  # On left mouse click
                pos = pygame.mouse.get_pos()  # Get position of mouse
                row, col = get_clicked_pos(pos, rows, width)  # Get node clicked on
                if 0 <= row < rows and 0 <= col < rows:
                    node = grid[row][col]  # Index the node
                    if not start and node.get_node_state() != 'end':  # If start node not set and node is not end node
                        start = node  # Set start node
                        start.set_node_state('start')  # Make start node
                    elif not end and node.get_node_state() != 'start':  # If end node not set and node is not start node
                        end = node  # Set end node
                        end.set_node_state('end')  # Make end node
                    elif node.get_node_state() != 'end' and node.get_node_state() != 'start':  # If node is not start or end
                        node.set_node_state('barrier')  # Make barrier node
                else:
                    continue

            elif pygame.mouse.get_pressed()[2]:  # On right mouse click
                pos = pygame.mouse.get_pos()  # Get position of mouse
                row, col = get_clicked_pos(pos, rows, width)  # Get node clicked on
                if 0 <= row < rows and 0 <= col < rows:
                    node = grid[row][col]  # Index the node
                    # noinspection PyUnresolvedReferences
                    node.set_node_state('empty')  # Reset node
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

            if event.type == pygame.KEYDOWN:  # On key press
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)  # Update neighbors
                    """
                    To visualize the algorithm, comment out the following three lines
                    and uncomment the three lines after them
                    """
                    visited = pathfinding.algorithm(grid, start, end)  # Run algorithm
                    for node in visited:
                        draw(win, grid, rows, width)  # Draw display window

                    # for node in algorithm(grid, start, end):  # Iterate over nodes from algorithm
                    #     draw(win, grid, rows, width)  # Draw display window
                    #     pygame.time.delay(5)  # Delay to control visualization speed

                if event.key == pygame.K_c:  # On c key press
                    start = None
                    end = None
                    grid = make_grid(rows, width)

    pygame.quit()


main(WIN, WIDTH)
