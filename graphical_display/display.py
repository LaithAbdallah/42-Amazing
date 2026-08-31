from mlx import Mlx
from time import sleep
from graphical_display.display_utils import themes, controls_set
from typing import Any

mlx = Mlx()
connection = mlx.mlx_init()
window_connection = mlx.mlx_new_window(connection, 1920, 1080, "A_maze_ing")
data = {}
theme_index = 0
show_path = True


def get_center(width: int, maze_width: int) -> int:
    pixels_width = 26 * maze_width - 6
    return (width - pixels_width) // 2


def get_coordinates(x: int, y: int, point: list[int]) -> list[int]:

    coordinates = [x + 26 * int(point[0]), y + 26 * int(point[1])]

    if point[0] == 0:
        coordinates[0] = x
    if point[1] == 0:
        coordinates[1] = y

    return [coordinates[0], coordinates[1]]


def draw_empty_maze(maze: str, maze_width: int, x: int, y: int) -> None:

    cells = 1

    for cell in maze:

        image = mlx.mlx_png_file_to_image(connection,
                                          themes[theme_index][f"{cell}"])
        mlx.mlx_put_image_to_window(connection,
                                    window_connection, image[0], x, y)
        x += 26

        # If no. of cells is divisible by maze width then we go to the next row
        if cells % maze_width == 0:
            y += 26
            x = get_center(2560, maze_width) - 150
        cells += 1


def draw_path(path: str, start_point: list[int]) -> None:

    # Start_point is a list of 2 integers, [0] is width and [1] is height
    x = start_point[0]
    y = start_point[1]

    for index in range(len(path) - 1):  # Skip exit point to not draw over it

        if path[index] == "N":
            y -= 26
        elif path[index] == "E":
            x += 26
        elif path[index] == "S":
            y += 26
        elif path[index] == "W":
            x -= 26

        path_pixel = mlx.mlx_png_file_to_image(connection,
                                               themes[theme_index]["path"])
        mlx.mlx_put_image_to_window(connection,
                                    window_connection, path_pixel[0], x, y)
        sleep(0.01)
        mlx.mlx_do_sync(connection)


def draw_points(entry_coords: list[int], exit_coords: list[int]) -> None:

    entry_img = mlx.mlx_png_file_to_image(connection,
                                          themes[theme_index]["entry"])
    exit_img = mlx.mlx_png_file_to_image(connection,
                                         themes[theme_index]["exit"])

    mlx.mlx_put_image_to_window(connection, window_connection, entry_img[0],
                                entry_coords[0], entry_coords[1])
    mlx.mlx_put_image_to_window(connection, window_connection, exit_img[0],
                                exit_coords[0], exit_coords[1])


def draw_controls(x: int) -> None:

    quit_img = mlx.mlx_png_file_to_image(connection, controls_set["q"])
    regen_img = mlx.mlx_png_file_to_image(connection, controls_set["r"])
    show_img = mlx.mlx_png_file_to_image(connection, controls_set["s"])
    color_img = mlx.mlx_png_file_to_image(connection, controls_set["c"])

    mlx.mlx_put_image_to_window(connection,
                                window_connection, quit_img[0], 25, x)
    mlx.mlx_put_image_to_window(connection,
                                window_connection, regen_img[0], 25, x + 100)
    mlx.mlx_put_image_to_window(connection,
                                window_connection, show_img[0], 25, x + 200)
    mlx.mlx_put_image_to_window(connection,
                                window_connection, color_img[0], 25, x + 300)


def display_output(specs: Any, first_time: bool, show: bool) -> None:

    global data  # check if the global is allowed
    data = specs  # to use it on change color and remove the path
    entry_point, exit_point, maze_width, maze, path = specs

    x = get_center(2560, maze_width) - 150
    y = 50  # Starts at y = 50
    entry_coords = get_coordinates(x, y, [entry_point[0], entry_point[1]])
    exit_coords = get_coordinates(x, y, [exit_point[0], exit_point[1]])

    # Adds a background
    background = mlx.mlx_png_file_to_image(connection,
                                           themes[theme_index]["background"])
    mlx.mlx_put_image_to_window(connection,
                                window_connection, background[0], 0, 0)

    draw_empty_maze(maze, maze_width, x, y)
    draw_points(entry_coords, exit_coords)
    draw_controls(250)

    if show:
        draw_path(path, entry_coords)
    mlx.mlx_key_hook(window_connection, buttons,
                     {"m_ptr": connection, "w_ptr": window_connection,
                      "mlx": mlx})

    if first_time:
        mlx.mlx_loop(connection)


def buttons(keynum: int, mystuff: dict[str, Any]) -> None:

    global theme_index
    global data
    global show_path
    if keynum == 113 or keynum == 81:  # q or Q to quit
        obj = mystuff["mlx"]
        obj.mlx_destroy_window(mystuff["m_ptr"], mystuff["w_ptr"])
        obj.mlx_release(mystuff["m_ptr"])

    elif keynum == 99 or keynum == 67:  # c or C to change the color
        theme_index += 1
        if theme_index >= len(themes):
            theme_index = 0
        display_output(data, False, show_path)

    elif keynum == 114 or keynum == 82:  # r or R to regenerate
        from a_maze_ing import send_specs
        from algorithm.find_paths import run
        run()
        show_path = True
        display_output(send_specs(), False, True)

    elif keynum == 115 or keynum == 83:  # s or S to show/hide path
        show_path = not show_path
        display_output(data, False, show_path)
