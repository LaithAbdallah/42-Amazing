from mazegen import MazeGenerator, Cell
from configuration import Configuration as config
from typing import Any


class BFS:
    """
    Breadth-first search solver for a maze.

    Explores the maze level by level from the entry point, which
    guarantees that the first route reaching the exit is a shortest one.
    Movement between two adjacent cells is only allowed when the wall
    separating them has been broken.

    Attributes:
        cells: The maze grid, filled in by get_path.
        start: The entry point as an (x, y) tuple.
        exit: The exit point as an (x, y) tuple.
        directions: The four moves as (dx, dy) offsets, ordered north,
            south, west, east.
    """

    config.load_config()
    cells: list[list[Cell]] = []  # get the maze
    start = (config.entry["x"], config.entry["y"])  # get the start point
    exit = (config.exit["x"], config.exit["y"])  # get the exit point
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    def __init__(self) -> None:
        """
        Initialise an empty search state.

        Attributes:
            visited: Cells already dequeued by the search.
            parent_map: Maps each discovered cell to the cell it was
                reached from, used to rebuild the path.
            queue: The frontier of cells waiting to be explored.
            path: The solution as a string of N/E/S/W moves.
        """

        self.visited: list[tuple[int, int]] = []
        self.parent_map: dict[tuple[int, int], tuple[int, int]] = dict()
        self.queue: list[tuple[int, int]] = []
        self.path = ""

    def can_i_go(self, current: tuple[int, int], idx: int) -> bool:
        """
        Check whether the wall in a given direction has been broken.

        Args:
            current: The cell being explored, as an (x, y) tuple.
            idx: Index into self.directions, where 0 is north, 1 is
                south, 2 is west and 3 is east.

        Returns:
            True if the wall is open and the move is allowed,
            False if the wall is still standing.
        """

        curr_x, curr_y = current[0], current[1]

        if idx == 0:
            if self.cells[curr_y][curr_x].north == 1:
                return False
        if idx == 1:
            if self.cells[curr_y][curr_x].south == 1:
                return False
        if idx == 2:
            if self.cells[curr_y][curr_x].west == 1:
                return False
        if idx == 3:
            if self.cells[curr_y][curr_x].east == 1:
                return False
        return True

    def check_border(self, next_y: int, next_x: int,
                     neighbor: tuple[int, int]) -> bool:
        """
        Check that a candidate cell is inside the maze and still unseen.

        Args:
            next_y: The row index of the candidate cell.
            next_x: The column index of the candidate cell.
            neighbor: The candidate cell as an (x, y) tuple.

        Returns:
            True if the cell is within bounds and has not been visited,
            False otherwise.
        """

        if next_y >= config.height or next_y < 0:
            return False
        if next_x >= config.width or next_x < 0:
            return False
        if neighbor in self.visited:
            return False
        return True

    def is_available(self, current: tuple[int, int],
                     direction: tuple[int, int]) -> Any:
        """
        Return the neighbour reached by a move, if it can be explored.

        Args:
            current: The cell being explored, as an (x, y) tuple.
            direction: The move as a (dx, dy) offset.

        Returns:
            The neighbour as an (x, y) tuple, or None if the move leaves
            the maze or lands on an already visited cell.
        """

        next_x, next_y = current[0] + direction[0], current[1] + direction[1]
        neighbor = (next_x, next_y)

        if self.check_border(next_y, next_x, neighbor):
            return neighbor
        return None

    def find_the_path(self) -> bool:
        """
        Run the breadth-first search from the entry to the exit.

        Fills parent_map along the way so the route can be rebuilt
        afterwards by walking backwards from the exit.

        Returns:
            True if the exit was reached, False if the queue was
            exhausted without finding it.
        """

        self.queue.append(self.start)

        while len(self.queue):

            current = self.queue.pop(0)
            self.visited.append(current)
            if current == self.exit:
                return True
            idx = 0
            for i in self.directions:
                if self.can_i_go(current, idx):
                    if isinstance(self.is_available(current, i), tuple):
                        neighbor = self.is_available(current, i)
                        self.queue.append(neighbor)
                        self.parent_map[neighbor] = current
                idx += 1
        if current != self.exit:
            return False
        return True

    def get_path(self, generator: MazeGenerator) -> str:
        """
        Generate a maze, solve it and encode the solution as moves.

        Walks parent_map backwards from the exit to the entry, then turns
        each pair of consecutive cells into a single direction character
        by looking at their coordinate difference.

        Args:
            generator: The maze generator used to build the grid.

        Returns:
            The solution as a string of N, E, S and W characters, or an
            empty string if no path exists.
        """

        self.cells = generator.generate_paths(config.seed)

        current = self.exit
        path = [current]

        if self.find_the_path():
            while self.start != self.parent_map[current]:
                current = self.parent_map[current]
                path.append(current)
            path.append(self.start)
            first_point = path.pop()
            while path:
                second_point = path.pop()
                total = (second_point[0] - first_point[0],
                         second_point[1] - first_point[1])
                directions = {(-1, 0): "W", (1, 0): "E",
                              (0, -1): "N", (0, 1): "S"}
                self.path += directions[total]
                first_point = second_point

        return self.path


def run() -> None:
    """
    Generate a maze, solve it and write the result to the output file.

    The maze grid is written first, followed by a blank line, the entry
    point, the exit point and the solution path. This file is the only
    interface between the solving stage and the display stage.
    """

    config.load_config()

    generator = MazeGenerator(config.width, config.height, config.entry,
                              config.exit, config.perfect, config.seed)
    maze = BFS()
    path = maze.get_path(generator)
    generator.maze_output("maze.txt")
    with open(config.output_file, "a") as file:
        file.write(f"\n{maze.start[0]}, {maze.start[1]}\n")
        file.write(f"{maze.exit[0]}, {maze.exit[1]}\n")
        file.write(path)
        file.write("\n")
