import pygame

import pathfinding

# Set up the window
WIDTH, HEIGHT = 1600, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Path Finding Algorithm")

# Define Tile Size in pixels
TILE_SIZE = 16

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
def make_grid(rows):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = pathfinding.Node(i, j)  # Create node
            grid[i].append(node)  # Add node to grid
    return grid


# Draw grid lines
def draw_grid(w_size, rows, w_width):
    node_width = w_width // rows  # Width of each node
    for i in range(rows):
        pygame.draw.line(w_size, GREY, (0, i * node_width), (w_width, i * node_width))  # Horizontal lines
    for j in range(rows):
        pygame.draw.line(w_size, GREY, (j * node_width, 0), (j * node_width, w_width))  # Vertical Lines


# Draw the display window
def draw(w_size, grid, rows, w_width):
    colors = {
        "empty": WHITE,
        "open": GREEN,
        "closed": RED,
        "barrier": BLACK,
        "start": ORANGE,
        "end": CYAN,
        "path": YELLOW,
    }

    w_size.fill(WHITE)  # Fill window with white
    for row in grid:
        for node in row:
            pygame.draw.rect(w_size, colors[node.state.name.lower()], ((node.row * TILE_SIZE), (node.col * TILE_SIZE), TILE_SIZE, TILE_SIZE))  # Draw node
    draw_grid(w_size, rows, w_width)  # Draw grid lines
    pygame.display.update()  # Update display


# Get node clicked on
def get_clicked_pos(pos, rows, w_width):
    node_width = w_width // rows  # Width of each node
    y, x = pos  # Get position of mouse
    row = y // node_width  # Get row of node
    col = x // node_width  # Get column of node
    return row, col


# Main function
# noinspection PyUnresolvedReferences
def main(w_size=WIN, w_width=WIDTH, tile_size=TILE_SIZE):
    total_rows = w_width // tile_size  # Number of rows
    grid = make_grid(total_rows)  # Create grid
    start = None  # Start node
    start_save = None  # Save location of start node
    end = None  # End node
    run = True  # Run flag

    # Main loop
    while run:
        draw(w_size, grid, total_rows, w_width)  # Draw display window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Quit if user closes window

            if pygame.mouse.get_pressed()[0]:  # On left mouse click
                pos = pygame.mouse.get_pos()  # Get position of mouse
                row, col = get_clicked_pos(pos, total_rows, w_width)  # Get node clicked on
                if 0 <= row < total_rows and 0 <= col < total_rows:
                    node = grid[row][col]  # Index the node
                    if not start and node.get_node_state() != 'end':  # If start node not set and node is not end node
                        start = node  # Set start node
                        start_save = start  # Save location of the start node
                        start.set_node_state(pathfinding.State.START)  # Make start node
                    elif not end and node.get_node_state() != 'start':  # If end node not set and node is not start node
                        end = node  # Set end node
                        end.set_node_state(pathfinding.State.END)  # Make end node
                    elif node.get_node_state() != 'end' and node.get_node_state() != 'start':
                        node.set_node_state(pathfinding.State.BARRIER)  # Make barrier node
                else:
                    continue

            elif pygame.mouse.get_pressed()[2]:  # On right mouse click
                pos = pygame.mouse.get_pos()  # Get position of mouse
                row, col = get_clicked_pos(pos, total_rows, w_width)  # Get node clicked on
                if 0 <= row < total_rows and 0 <= col < total_rows:
                    node = grid[row][col]  # Index the node
                    # noinspection PyUnresolvedReferences
                    node.set_node_state(pathfinding.State.EMPTY)  # Reset node
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

            if event.type == pygame.KEYDOWN:  # On key press
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid, total_rows)  # Update neighbors
                    """
                    To visualize the algorithm, comment out the following three lines
                    and uncomment the three lines after them
                    """
                    visited = pathfinding.algorithm(grid, start, end)  # Run algorithm
                    for node in visited:
                        draw(w_size, grid, total_rows, w_width)  # Draw display window

                    # for node in algorithm(grid, start, end):  # Iterate over nodes from algorithm
                    #     draw(win, grid, rows, width)  # Draw display window
                    #     pygame.time.delay(5)  # Delay to control visualization speed

                if event.key == pygame.K_c:  # On c key press
                    start = start_save  # Reset start node
                    start.set_node_state(pathfinding.State.START)  # Make start node
                    reset_flag = False
                    for row in grid:
                        for node in row:
                            if node.get_node_state() in {'open', 'closed', 'path'}:
                                node.set_node_state(pathfinding.State.EMPTY)
                                reset_flag = True
                    if not reset_flag:
                        # Reset grid
                        start = None
                        end = None
                        grid = make_grid(total_rows)

    pygame.quit()


main()
