"""
Standalone maze generation module.

Builds a maze with an iterative depth-first search and backtracking,
optionally braids it into an imperfect maze, and writes it out in a
compact hexadecimal wall encoding. This module depends only on the
standard library and can be imported into any other project.
"""

from random import randint, choice, seed


class Cell:
    """
    Represents a single cell in the maze grid.

    Attributes:
        north: North wall state, 1 if present and 0 if broken.
        east: East wall state, 1 if present and 0 if broken.
        south: South wall state, 1 if present and 0 if broken.
        west: West wall state, 1 if present and 0 if broken.
        visited: True if the cell has been visited by the generation algorithm.
        is_42: True if the cell is part of the '42' symbol drawn in the maze.
    """

    def __init__(self) -> None:
        """
        Create a cell with all four walls standing and unvisited.
        """

        self.north = 1
        self.east = 1
        self.west = 1
        self.south = 1
        self.visited = False
        self.is_42 = False

    def break_wall(self, second_cell: "Cell", direction: str) -> None:
        """
        Break the wall between this cell and an adjacent cell.

        Args:
            second_cell: The adjacent cell to break the wall towards.
            direction: The direction of the wall to break
             ("north", "south", "east", "west").
        """

        opposites = {
            "north": "south", "east": "west", "west": "east",
            "south": "north"
        }

        if not self.is_42:
            setattr(self, direction, 0)
        if not second_cell.is_42:
            setattr(second_cell, opposites[direction], 0)


class MazeGenerator:
    """
        Generate a maze of a given size and write it to a file.

        Attributes:
            width: The maze width in cells.
            height: The maze height in cells.
            maze: The 2D grid of cells, empty until generate_paths is called.
            entry: The entry point as {"x": column, "y": row}.
            exit: The exit point as {"x": column, "y": row}.
            perfect: True for exactly one route between any two cells,
                False to braid the maze and introduce loops.
            seed: A non-zero value makes generation reproducible.
    """

    def __init__(self, width: int, height: int, entry: dict[str, int],
                 exit: dict[str, int], perfect: bool, seed: int):
        """
        Store the generation parameters without building anything yet.

        Args:
            width: The maze width in cells.
            height: The maze height in cells.
            entry: The entry point as {"x": column, "y": row}.
            exit: The exit point as {"x": column, "y": row}.
            perfect: True for a perfect maze, False for a braided one.
            seed: A non-zero value makes generation reproducible.
        """

        self.width = width
        self.height = height
        self.maze: list[list[Cell]] = []
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed

    def has_neighbours(self, x: int, y: int) -> bool:
        """
        Check if a cell has any unvisited neighbours.

        Args:
            x: The row index of the cell.
            y: The column index of the cell.

        Returns:
            True if the cell has at least one unvisited neighbour,
              False otherwise.
        """

        # Check north cell
        if x - 1 >= 0 and not self.maze[x - 1][y].visited:
            return True
        # Check south cell
        if x + 1 < self.height and not self.maze[x + 1][y].visited:
            return True
        # Check east cell
        if y + 1 < self.width and not self.maze[x][y + 1].visited:
            return True
        # Check west cell
        if y - 1 >= 0 and not self.maze[x][y - 1].visited:
            return True
        return False

    def mark_visited(self, x: int, y: int, index: str, times: int,
                     direction: str) -> None:
        """
        Mark a line of cells as part of the '42' symbol.

        Args:
            x: The starting row index.
            y: The starting column index.
            index: The axis to traverse,
              "x" for vertical and "y" for horizontal.
            times: The number of cells to mark.
            direction: The direction to traverse
            ("north", "south", "east", "west").
        """

        for time in range(times):
            # Mark the cell as visited so it never get modified (a square)
            self.maze[x][y].visited = True
            self.maze[x][y].is_42 = True

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

    def generate_number_4(self) -> None:
        """
        Draw the number '4' in the center-left of the maze by
        marking cells as part of the '42' symbol.
        """

        center = (self.height // 2, self.width // 2)
        x, y = center[0], center[1]
        y -= 1  # Move the point to the left

        self.mark_visited(x, y, "x", 3, "south")
        self.mark_visited(x, y, "y", 3, "west")
        y -= 2
        self.mark_visited(x, y, "x", 3, "north")

    def generate_number_2(self) -> None:
        """
        Draw the number '2' in the center-right of the maze by
        marking cells as part of the '42' symbol.
        """

        center = (self.height // 2, self.width // 2)
        x, y = center[0], center[1]
        y += 1  # Move the point to the right

        self.mark_visited(x, y, "x", 3, "south")
        x += 2
        self.mark_visited(x, y, "y", 3, "east")
        x -= 2
        self.mark_visited(x, y, "y", 3, "east")
        y += 2
        self.mark_visited(x, y, "x", 3, "north")
        x -= 2
        self.mark_visited(x, y, "y", 3, "west")

    def generate_42(self, stack: list[tuple[int, int]]) -> bool:
        """
        Draw the '42' symbol in the maze if dimensions allow it.

        Args:
            stack: The backtracking stack to push '42' cells onto.

        Returns:
            True if '42' was drawn, False otherwise.
        """

        drew_42 = False

        # Only draws '42' if its the maze size is greater than (8 * 8)
        if self.height >= 9 and self.width >= 9:
            self.generate_number_4()
            self.generate_number_2()
            drew_42 = True

            for row in range(self.height):  # Push '42' cells to the stack
                for column in range(self.width):
                    if self.maze[row][column].visited:
                        stack.append((row, column))

            entry = self.entry
            if self.maze[entry["y"]][entry["x"]].is_42:
                raise Exception("Entry point can't be on 42 cells")

            exit = self.exit
            if self.maze[exit["y"]][exit["x"]].is_42:
                raise Exception("Exit point can't be on 42 cells")

        return drew_42

    def is_available(self, y: int, x: int) -> bool:
        """
        Check whether a cell can be carved into during braiding.

        Args:
            y: The row index of the cell.
            x: The column index of the cell.

        Returns:
            True if the cell is inside the grid and is not part of the
             "42" symbol, False otherwise.
        """

        if y >= self.height or y < 0:
            return False
        if x >= self.width or x < 0:
            return False

        if self.maze[y][x].is_42:
            return False

        return True

    def imperfect_maze(self) -> None:
        """
        Braid the maze by removing its dead ends.

        Sweeps the grid looking for cells with exactly three standing
        walls, which are precisely the dead ends, and breaks one wall at
        random on each of them. Cells belonging to the "42" symbol are
        left untouched. The sweep is repeated several times because
        modifying the maze can create new dead ends that were not detected
        during earlier sweeps.
        """

        directions = ["north", "east", "west", "south"]
        height = self.height
        width = self.width

        for i in range(7):
            for row in range(height):
                for column in range(width):

                    walls = 0
                    cell = self.maze[row][column]

                    if cell.east:
                        walls += 1
                    if cell.north:
                        walls += 1
                    if cell.west:
                        walls += 1
                    if cell.south:
                        walls += 1

                    if walls == 3:

                        wall_broken = False
                        while (not wall_broken):

                            direction = choice(directions)

                            if direction == "north":
                                if self.is_available(row - 1, column):
                                    cell.break_wall(self.maze[row - 1][column],
                                                    direction)
                                    wall_broken = True

                            elif direction == "east":
                                if self.is_available(row, column + 1):
                                    cell.break_wall(self.maze[row][column + 1],
                                                    direction)
                                    wall_broken = True

                            elif direction == "west":
                                if self.is_available(row, column - 1):
                                    cell.break_wall(self.maze[row][column - 1],
                                                    direction)
                                    wall_broken = True

                            else:
                                if self.is_available(row + 1, column):
                                    cell.break_wall(self.maze[row + 1][column],
                                                    direction)
                                    wall_broken = True

    def generate_maze(self) -> None:
        """
        Fill self.maze with a grid of cells that have all walls closed.
        """

        for row in range(self.height):
            self.maze.append([])
            for colum in range(self.width):
                self.maze[row].append(Cell())

    def generate_paths(self, seed_id: int) -> list[list[Cell]]:
        """
        Generate the maze using iterative depth-first search with
        backtracking, then braid it if perfect is False.

        Args:
            seed_id: A non-zero value seeds the random generator so the
                same maze is produced on every run.

        Returns:
            The 2D grid of cells, with the carved walls applied.
        """

        self.generate_maze()

        if seed_id:
            seed(seed_id)

        stack: list[tuple[int, int]] = []
        unvisited = self.height * self.width
        directions = ["north", "east", "west", "south"]
        # x = row, y = column, this is a random point to create paths
        x, y = randint(0, self.height - 1), randint(0, self.width - 1)

        if not self.generate_42(stack):
            print("Couldn't generate 42 symbol!")  # To be moved later
        else:
            unvisited -= 18  # Cells visited while drawing '42'

        while unvisited:
            current_cell = self.maze[x][y]
            if not current_cell.visited:
                current_cell.visited = True
                unvisited -= 1

            if self.has_neighbours(x, y):
                direction = choice(directions)  # Picks a random direction

                if direction == "north":  # Go up a row (x - 1)
                    if x - 1 >= 0 and not self.maze[x - 1][y].visited:
                        x -= 1
                        stack.append((x, y))
                        current_cell.break_wall(self.maze[x][y], direction)

                elif direction == "south":  # Go down a row (x + 1)
                    if x + 1 < self.height and not self.maze[x + 1][y].visited:
                        x += 1
                        stack.append((x, y))
                        current_cell.break_wall(self.maze[x][y], direction)

                elif direction == "east":  # Go right a column (y + 1)
                    if y + 1 < self.width and not self.maze[x][y + 1].visited:
                        y += 1
                        stack.append((x, y))
                        current_cell.break_wall(self.maze[x][y], direction)

                elif direction == "west":  # Go left a column (y - 1)
                    if y - 1 >= 0 and not self.maze[x][y - 1].visited:
                        y -= 1
                        stack.append((x, y))
                        current_cell.break_wall(self.maze[x][y], direction)

            else:
                stack.pop()
                x, y = stack[-1][0], stack[-1][1]

        if not self.perfect:
            self.imperfect_maze()

        return self.maze

    def get_hexa(self, x: int, y: int) -> str:
        """
        Get the hex representation of a cell's wall configuration.

        The north wall is the least significant bit and is worth 1,
        then 2 for east, 4 for south and 8 for west.

        Args:
            x: The row index of the cell.
            y: The column index of the cell.

        Returns:
            A single hex character representing the cell's wall states.
        """

        int_value = 0

        if self.maze[x][y].north:
            int_value += 1
        if self.maze[x][y].east:
            int_value += 2
        if self.maze[x][y].south:
            int_value += 4
        if self.maze[x][y].west:
            int_value += 8
        return hex(int_value).replace("0x", "").upper()

    def maze_output(self, output_file: str) -> None:
        """
        Write the maze to the output file in hex format.

        Args:
            output_file: The path of the file to write to.
        """

        with open(output_file, "w") as file:
            for row in range(self.height):
                for column in range(self.width):
                    file.write(self.get_hexa(row, column))
                file.write("\n")


def main() -> None:
    """
    Demonstrate the module on its own, without the rest of the project.

    Generates a 55x35 braided maze with a fixed seed and writes it to
    output.txt, which makes the generator testable in isolation.
    """

    width = 55
    height = 35
    entry = {"x": 0, "y": 0}
    exit = {"x": 54, "y": 34}
    perfect_maze = False
    #  You can either enter a seed as an int value or leave it blank or
    #  zero to have a different maze every time you regenerate
    seed = 1

    generator = MazeGenerator(width, height, entry, exit, perfect_maze, seed)
    generator.generate_paths(seed)
    generator.maze_output("output.txt")


if __name__ == "__main__":
    main()
