from config import Configuration
from maze_generation.generation import Cell
from random import randint, choice


# Checks if a cell has neighbours
def has_neighbours(height: int, width: int,
                   maze: list[list[Cell]], x: int, y: int) -> bool:
    """
    Check if a cell has any unvisited neighbours.

    Args:
        height: The height of the maze in cells.
        width: The width of the maze in cells.
        maze: The 2D grid of cells.
        x: The row index of the cell.
        y: The column index of the cell.

    Returns:
        True if the cell has at least one unvisited neighbour, False otherwise.
    """

    if x - 1 >= 0 and not maze[x - 1][y].visited:  # Check north cell
        return True
    if x + 1 < height and not maze[x + 1][y].visited:  # Check south cell
        return True
    if y + 1 < width and not maze[x][y + 1].visited:  # Check east cell
        return True
    if y - 1 >= 0 and not maze[x][y - 1].visited:  # Check west cell
        return True
    return False


def mark_visited(x: int, y: int, index: str, times: int,
                 maze: list[list[Cell]], direction: str) -> None:
    """
    Mark a line of cells as part of the '42' symbol.

    Args:
        x: The starting row index.
        y: The starting column index.
        index: The axis to traverse, "x" for vertical and "y" for horizontal.
        times: The number of cells to mark.
        maze: The 2D grid of cells.
        direction: The direction to traverse
         ("north", "south", "east", "west").
    """

    for time in range(times):
        # Mark the cell as visited so it never get modified (a square)
        maze[x][y].visited = True
        maze[x][y].is_42 = True

        if index == "x":
            if direction == "north":
                x -= 1
            else:
                x += 1
        else:
            if direction == "west":
                y -= 1
            else:
                y += 1


def generate_number_4(height: int, width: int, maze: list[list[Cell]]) -> None:
    """
    Draw the number '4' in the center-left of the maze by
     marking cells as part of the '42' symbol.

    Args:
        height: The height of the maze in cells.
        width: The width of the maze in cells.
        maze: The 2D grid of cells.
    """

    center = (height // 2, width // 2)
    x, y = center[0], center[1]
    y -= 1  # Move the point to the left

    mark_visited(x, y, "x", 3, maze, "south")
    mark_visited(x, y, "y", 3, maze, "west")
    y -= 2
    mark_visited(x, y, "x", 3, maze, "north")


def generate_number_2(height: int, width: int, maze: list[list[Cell]]) -> None:
    """
    Draw the number '2' in the center-right of the maze by
     marking cells as part of the '42' symbol.

    Args:
        height: The height of the maze in cells.
        width: The width of the maze in cells.
        maze: The 2D grid of cells.
    """

    center = (height // 2, width // 2)
    x, y = center[0], center[1]
    y += 1  # Move the point to the right

    mark_visited(x, y, "x", 3, maze, "south")
    x += 2
    mark_visited(x, y, "y", 3, maze, "east")
    x -= 2
    mark_visited(x, y, "y", 3, maze, "east")
    y += 2
    mark_visited(x, y, "x", 3, maze, "north")
    x -= 2
    mark_visited(x, y, "y", 3, maze, "west")


def generate_42(height: int, width: int, maze: list[list[Cell]],
                stack: list[tuple[int, int]]) -> bool:
    """
    Draw the '42' symbol in the maze if dimensions allow it.

    Args:
        height: The height of the maze in cells.
        width: The width of the maze in cells.
        maze: The 2D grid of cells.
        stack: The backtracking stack to push '42' cells onto.

    Returns:
        True if '42' was drawn, False otherwise.
    """

    drew_42 = False

    # Only draws '42' if its double the '42' drawing size (5 * 7)
    if height >= 9 and width >= 9:
        generate_number_4(height, width, maze)
        generate_number_2(height, width, maze)
        drew_42 = True

        for row in range(height):  # Push '42' cells to the stack
            for column in range(width):
                if maze[row][column].visited:
                    stack.append((row, column))

    return drew_42


def generate_maze(height: int, width: int) -> list[list[Cell]]:
    """
    Create a 2D grid of uninitialized cells.

    Args:
        height: The height of the maze in cells.
        width: The width of the maze in cells.

    Returns:
        A 2D list of Cell objects with all walls closed.
    """

    maze: list[list[Cell]] = []

    for row in range(height):
        maze.append([])
        for colum in range(width):
            maze[row].append(Cell())
    return maze


def generate_paths(height: int, width: int) -> list[list[Cell]]:
    """
    Generate a perfect maze using iterative depth-first search
     with backtracking.

    Args:
        height: The height of the maze in cells.
        width: The width of the maze in cells.
    """

    maze = generate_maze(height, width)
    stack: list[tuple[int, int]] = []
    unvisited = height * width
    directions = ["north", "east", "west", "south"]
    # x = row, y = column, this is a random point to create paths
    x, y = randint(0, height - 1), randint(0, width - 1)

    if not generate_42(height, width, maze, stack):
        print("Couldn't generate 42 symbol!")  # To be moved later
    else:
        unvisited -= 18  # Cells visited while drawing '42'

    while unvisited:
        current_cell = maze[x][y]
        if not current_cell.visited:
            current_cell.visited = True
            unvisited -= 1

        if has_neighbours(height, width, maze, x, y):
            direction = choice(directions)  # Picks a random direction

            if direction == "north":  # Go up a row (x - 1)
                if x - 1 >= 0 and not maze[x - 1][y].visited:
                    x -= 1
                    stack.append((x, y))
                    current_cell.break_wall(maze[x][y], direction)

            elif direction == "south":  # Go down a row (x + 1)
                if x + 1 < height and not maze[x + 1][y].visited:
                    x += 1
                    stack.append((x, y))
                    current_cell.break_wall(maze[x][y], direction)

            elif direction == "east":  # Go right a column (y + 1)
                if y + 1 < width and not maze[x][y + 1].visited:
                    y += 1
                    stack.append((x, y))
                    current_cell.break_wall(maze[x][y], direction)

            elif direction == "west":  # Go left a column (y - 1)
                if y - 1 >= 0 and not maze[x][y - 1].visited:
                    y -= 1
                    stack.append((x, y))
                    current_cell.break_wall(maze[x][y], direction)

        else:
            stack.pop()
            x, y = stack[-1][0], stack[-1][1]

    # maze_output(height, width, maze)  # To be moved later
    return maze


# Gets hexa representation for a single maze cell,
# since north is LSB its 1, then 2 for east, 4 for south and 8 for west
def get_hexa(x: int, y: int, maze: list[list[Cell]]) -> str:
    """
    Get the hex representation of a cell's wall configuration.

    Args:
        x: The row index of the cell.
        y: The column index of the cell.
        maze: The 2D grid of cells.

    Returns:
        A single hex character representing the cell's wall states.
    """

    int_value = 0

    if maze[x][y].north:
        int_value += 1
    if maze[x][y].east:
        int_value += 2
    if maze[x][y].south:
        int_value += 4
    if maze[x][y].west:
        int_value += 8
    return hex(int_value).replace("0x", "").upper()


def maze_output(height: int, width: int, maze: list[list[Cell]]) -> None:
    """
    Write the maze to the output file in hex format.

    Args:
        height: The height of the maze in cells.
        width: The width of the maze in cells.
        maze: The 2D grid of cells.
    """

    Configuration.load_config()
    output_file = Configuration.output_file

    with open(output_file, "w") as file:
        for row in range(height):
            for column in range(width):
                file.write(get_hexa(row, column, maze))
            file.write("\n")


# generate_paths(9, 10)
