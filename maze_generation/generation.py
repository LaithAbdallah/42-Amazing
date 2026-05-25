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
