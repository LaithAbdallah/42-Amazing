from sys import argv
from algorithm import run
from config import Configuration
from graphical_display import display_output

def send_specs() -> dict[str, list[str] | str | int]:

    Configuration.load_config()
    with open(Configuration.output_file, "r") as file:
        
        lines_read = ""
        for line in range(Configuration.height):
            lines_read += file.readline().replace("\n", "")
        file.readline()
        
        entry_point = file.readline().replace("\n", "").split(",")
        entry_point[0] = int(entry_point[0])
        entry_point[1] = int(entry_point[1])
        
        exit_point = file.readline().replace("\n", "").split(",")
        exit_point[0] = int(exit_point[0])
        exit_point[1] = int(exit_point[1])

        path = file.readline().replace("\n", "")
        
        width = Configuration.width

    return {
        "maze": lines_read, "entry": entry_point,
        "exit": exit_point, "path": path,
        "width": width
    }


def main() -> None:
    
    if len(argv) != 2 or (len(argv) == 2 and argv[1] != "config.txt"):
        print("Usage: $> python3 a_maze_ing.py config.txt")
        return

    run()
    display_output(send_specs(), True)


if __name__ == "__main__":
    main()