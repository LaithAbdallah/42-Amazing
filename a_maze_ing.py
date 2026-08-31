from sys import argv
from algorithm import run
from configuration import Configuration, ConfigError
from graphical_display import display_output
from typing import Any


def send_specs() -> Any:

    Configuration.load_config()

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

    if len(argv) != 2 or (len(argv) == 2 and argv[1] != "config.txt"):
        print("Usage: $> python3 a_maze_ing.py config.txt")
        return

    if not Configuration.validate_config():
        return
    try:
        run()
    except ConfigError as e:
        print(e)
        return
    display_output(send_specs(), True, True)


if __name__ == "__main__":
    main()
