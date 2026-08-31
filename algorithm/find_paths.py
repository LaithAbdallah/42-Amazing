from maze_generation import MazeGenerator, Cell
from config import Configuration as config
from typing import Any


class BFS:

    config.load_config()
    cells: list[list[Cell]] = []  # get the maze
    start = (config.entry["x"], config.entry["y"])  # get the start point
    exit = (config.exit["x"], config.exit["y"])  # get the exit point

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    def __init__(self) -> None:

        self.visited: list[tuple[int, int]] = []
        self.parent_map: dict[tuple[int, int], tuple[int, int]] = dict()
        self.queue: list[tuple[int, int]] = []
        self.path = ""

    def can_i_go(self, current: tuple[int, int], idx: int) -> bool:
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

        if next_y >= config.height or next_y < 0:
            return False
        if next_x >= config.width or next_x < 0:
            return False
        if neighbor in self.visited:
            return False
        return True

    def is_available(self, current: tuple[int, int],
                     direction: tuple[int, int]) -> Any:

        next_x, next_y = current[0] + direction[0], current[1] + direction[1]
        neighbor = (next_x, next_y)
        if self.check_border(next_y, next_x, neighbor):
            return neighbor
        return None

    def find_the_path(self) -> bool:

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
                        # self.visited.append(neighbor)
                        self.parent_map[neighbor] = current
                idx += 1
        if current != self.exit:
            return False
        return True

    def get_path(self, generator: MazeGenerator) -> str:

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
