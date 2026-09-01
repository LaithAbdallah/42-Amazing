from sys import argv
from algorithm import run
from configuration import Configuration
from graphical_display import display_output
from typing import Any


def send_specs() -> Any:
    """
    Read the generated maze file and collect everything the display needs.

    The output file is expected to contain the maze grid as hexadecimal
    characters, a blank line, the entry point, the exit point and the
    solution path, in that order.

    Returns:
        A tuple of (maze, entry_point, exit_point, path, width) where maze
        is the grid flattened into a single string, entry_point and
        exit_point are ["x", "y"] string pairs, path is the sequence of
        N/E/S/W moves and width is the maze width in cells.
    """

    Configuration.load_config(False)

    with open(Configuration.output_file, "r") as file:

        lines_read = ""
        for line in range(Configuration.height):
            lines_read += file.readline().replace("\n", "")
        file.readline()

        entry_point = file.readline().replace("\n", "").split(",")
        entry = []
        entry.append(int(entry_point[0]))
        entry.append(int(entry_point[1]))

        exit_point = file.readline().replace("\n", "").split(",")
        exit = []
        exit.append(int(exit_point[0]))
        exit.append(int(exit_point[1]))

        path = file.readline().replace("\n", "")

        width = Configuration.width

    return lines_read, entry_point, exit_point, path, width


def main() -> None:
    """
    Run the program end to end.

    Checks the command line arguments, validates the configuration file,
    generates and solves the maze, then opens the display window. Any
    configuration error is reported and stops the run before anything is
    drawn.
    """

    if len(argv) != 2 or (len(argv) == 2 and argv[1] != "config.txt"):
        print("Usage: $> python3 a_maze_ing.py config.txt")
        return

    if not Configuration.validate_config():
        return
    try:
        run()
    except Exception as e:
        print(e)
        return
    display_output(send_specs(), True, True)


if __name__ == "__main__":
    main()
