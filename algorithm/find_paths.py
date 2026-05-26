# import queue
from maze_generation.generation_utils import generate_paths, get_hexa, maze_output
from config import Configuration as config


class BFS:

    config.load_config()
    cells = generate_paths(config.height, config.width)  # get the maze
    start = (config.entry["x"], config.entry["y"])  # get the start point
    exit = (config.exit["x"], config.exit["y"])  # get the exit point

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited: list[tuple[int, int]] = []
    parent_map: dict[tuple[int, int], tuple[int, int]] = dict()
    queue = []
    path = ""

    def can_i_go(self, current: tuple[int, int], idx: int) -> bool:
        curr_x, curr_y = current[0], current[1]
        if idx == 0:
            if self.cells[curr_x][curr_y].north == 1:
                return False
        if idx == 1:
            if self.cells[curr_x][curr_y].south == 1:
                return False
        if idx == 2:
            if self.cells[curr_x][curr_y].west == 1:
                return False
        if idx == 3:
            if self.cells[curr_x][curr_y].east == 1:
                return False
        return True

    def is_available(self, current: tuple, direction: tuple):
        next_x, next_y = current[0] + direction[0], current[1] + direction[1]
        neighbor = (next_x, next_y)
        if next_x >= config.height or next_x < 0:
            return False
        if next_y >= config.width or next_y < 0:
            return False
        if neighbor in self.visited:
            return False
        return neighbor

    def find_the_path(self) -> None:

        self.queue.append(self.start)

        while len(self.queue):

            current = self.queue.pop(0)
            self.visited.append(current)
            if current == self.exit:
                break
            idx = 0
            for i in self.directions:
                if self.can_i_go(current, idx):
                    if isinstance(self.is_available(current, i), tuple):
                        neighbor = self.is_available(current, i)
                        self.queue.append(neighbor)
                        self.visited.append(neighbor)
                        self.parent_map[neighbor] = current
                idx += 1
        if current != self.exit:
            print("there is no path")

    def get_path(self):
        current = self.exit
        path = [current]
        while self.start != self.parent_map[current]:
            current = self.parent_map[current]
            path.append(current)
        path.append(self.start)
        first_point = path.pop()
        while path:
            second_point = path.pop()
            total = (second_point[0] - first_point[0],
                     second_point[1] - first_point[1])
            directions = {(-1, 0): "N", (1, 0): "S",
                         (0, -1): "W", (0, 1): "E"}
            self.path += directions[total]
            first_point = second_point

        return path


a = BFS()
a.find_the_path()
maze_output(config.height, config.width, a.cells)
a.get_path()
print(a.path)
