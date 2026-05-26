# import queue
from maze_generation.generation_utils import generate_paths, get_hexa, maze_output
from config.configuration import Configuration as config


class BFS:

    config.load_config()
    cells = generate_paths(config.height, config.width)  # get the maze
    start = (config.entry["x"], config.entry["y"])  # get the start point
    exit = (config.exit["x"], config.exit["y"])  # get the exit point

    dirctions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visted = []
    parent_map = {}
    queue = []
    path = ""

    def can_i_go(self, current, idx) -> bool:
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

    def is_valibale(self, current: tuple, dirc: tuple):
        next_x, next_y = current[0] + dirc[0], current[1] + dirc[1]
        neighbor = (next_x, next_y)
        if next_x >= config.height or next_x < 0:
            return False
        if next_y >= config.width or next_y < 0:
            return False
        if neighbor in self.visted:
            return False
        return neighbor

    def find_the_path(self) -> str:

        self.queue.append(self.start)

        while len(self.queue):

            current = self.queue.pop(0)
            self.visted.append(current)
            if current == self.exit:
                break
            idx = 0
            for i in self.dirctions:
                if self.can_i_go(current, idx):
                    if isinstance(self.is_valibale(current, i), tuple):
                        neighbor = self.is_valibale(current, i)
                        self.queue.append(neighbor)
                        self.visted.append(neighbor)
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
            dirctions = {(-1, 0): "N", (1, 0): "S",
                         (0, -1): "W", (0, 1): "E"}
            self.path += dirctions[total]
            first_point = second_point

        return path


a = BFS()
a.find_the_path()
maze_output(config.height, config.width, a.cells)
a.get_path()
print(a.path)
