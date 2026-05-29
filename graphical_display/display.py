from mlx import Mlx
from time import sleep


mlx = Mlx()
connection = mlx.mlx_init()
window_connection = mlx.mlx_new_window(connection, 2560, 1440, "A_MAZE_ING")
data = {}
thems = []
indx_them = 0
show_path = True
first_set = {
    "1": "images/first_set/1.png", "2": "images/first_set/2.png", "3": "images/first_set/3.png",
    "4": "images/first_set/4.png", "5": "images/first_set/5.png", "6": "images/first_set/6.png",
    "7": "images/first_set/7.png", "8": "images/first_set/8.png", "9": "images/first_set/9.png",
    "A": "images/first_set/A.png", "B": "images/first_set/B.png", "C": "images/first_set/C.png",
    "D": "images/first_set/D.png", "E": "images/first_set/E.png", "F": "images/first_set/F.png",
    "0": "images/first_set/0.png", "entry": "images/first_set/entry.png",
    "exit": "images/first_set/exit.png", "path": "images/first_set/path.png",
    "background": "images/first_set/background.png"
}

second_set = {
    "1": "images/second_set/1.png", "2": "images/second_set/2.png", "3": "images/second_set/3.png",
    "4": "images/second_set/4.png", "5": "images/second_set/5.png", "6": "images/second_set/6.png",
    "7": "images/second_set/7.png", "8": "images/second_set/8.png", "9": "images/second_set/9.png",
    "A": "images/second_set/A.png", "B": "images/second_set/B.png", "C": "images/second_set/C.png",
    "D": "images/second_set/D.png", "E": "images/second_set/E.png", "F": "images/second_set/F.png",
    "0": "images/second_set/0.png", "entry": "images/second_set/entry.png",
    "exit": "images/second_set/exit.png", "path": "images/first_set/path.png",
    "background": "images/first_set/background.png"
}

third_set = {
    "1": "images/3rd_set/1.png", "2": "images/3rd_set/2.png", "3": "images/3rd_set/3.png",
    "4": "images/3rd_set/4.png", "5": "images/3rd_set/5.png", "6": "images/3rd_set/6.png",
    "7": "images/3rd_set/7.png", "8": "images/3rd_set/8.png", "9": "images/3rd_set/9.png",
    "A": "images/3rd_set/A.png", "B": "images/3rd_set/B.png", "C": "images/3rd_set/C.png",
    "D": "images/3rd_set/D.png", "E": "images/3rd_set/E.png", "F": "images/3rd_set/F.png",
    "0": "images/3rd_set/0.png", "entry": "images/3rd_set/entry.png",
    "exit": "images/3rd_set/exit.png", "path": "images/3rd_set/path.png",
    "background": "images/3rd_set/background.png"
}

thems.append(first_set)
thems.append(second_set)
thems.append(third_set)

def get_center(width: int, maze_width: int) -> int:
    pixels_width = 26 * maze_width - 6
    return (width - pixels_width) // 2


def get_coordinates(x: int, y: int, point: list[int]) -> list[int]:
    
    coordinates = [x + 26 * point[0], y + 26 * point[1]]

    if point[0] == 0:
        coordinates[0] = x
    if point[1] == 0:
        coordinates[1] = y

    return [coordinates[0], coordinates[1]]
    


def draw_empty_maze(maze: str, maze_width: int, x: int, y: int) -> None:
    
    cells = 1

    for cell in maze:

        image = mlx.mlx_png_file_to_image(connection, thems[indx_them][f"{cell}"])
        mlx.mlx_put_image_to_window(connection, window_connection, image[0], x, y)
        # mlx.mlx_do_sync(connection)
        # sleep(0.0000000001)
        x += 26
        
        # If no. of cells is divisible by maze width then we go to the next row
        if cells % maze_width == 0:
            y += 26
            x = get_center(2560, maze_width)   
        cells += 1


def draw_path(path: str, start_point: list[int]):

    # Start_point is a list of 2 integers, [0] is width and [1] is height
    x = start_point[0]
    y = start_point[1]

    for index in range(len(path) - 1):  # Skip exit point to not draw over it

        if path[index]== "N":
            y -= 26
        elif path[index] == "E":
            x += 26
        elif path[index]== "S":
            y += 26
        elif path[index] == "W":
            x -= 26

        path_pixel = mlx.mlx_png_file_to_image(connection, thems[indx_them]["path"])
        mlx.mlx_put_image_to_window(connection, window_connection, path_pixel[0], x, y)
        mlx.mlx_do_sync(connection)
        sleep(0.001)


def draw_points(entry_coords: list[int], exit_coords: list[int]) -> None:

    entry_img = mlx.mlx_png_file_to_image(connection, thems[indx_them]["entry"]) # To be edited
    exit_img = mlx.mlx_png_file_to_image(connection, thems[indx_them]["exit"]) # To be edited

    mlx.mlx_put_image_to_window(connection, window_connection, entry_img[0], entry_coords[0], entry_coords[1])
    mlx.mlx_put_image_to_window(connection, window_connection, exit_img[0], exit_coords[0], exit_coords[1])


def display_output(specs: dict[str, list[int] | str | int], first_time: bool) -> None:

    global show_path
    global data # check if the global is allowed
    data = specs # to use it on change color and remove the path

    entry_point = specs["entry"]
    exit_point = specs["exit"]
    maze_width = specs["width"]
    maze = specs["maze"]
    path = specs["path"]

    x = get_center(2560, maze_width)
    y = 50  # Starts at y = 50
    entry_coords = get_coordinates(x, y, [entry_point[0], entry_point[1]]) 
    exit_coords = get_coordinates(x, y, [exit_point[0], exit_point[1]])

    # Adds a background
    background = mlx.mlx_png_file_to_image(connection, thems[indx_them]["background"])
    mlx.mlx_put_image_to_window(connection, window_connection, background[0], 0, 0)

    draw_empty_maze(maze, maze_width, x, y)
    draw_points(entry_coords, exit_coords)
    if show_path:
        draw_path(path, entry_coords)
        show_path = False
    else:
        show_path = True
    mlx.mlx_key_hook(window_connection,  buttons, {"m_ptr": connection, "w_ptr": window_connection, "mlx": mlx})
    
    if first_time:
        mlx.mlx_loop(connection)




# quitt = mlx.mlx_png_file_to_image(connection, "images/extra/1.png")
# regen = mlx.mlx_png_file_to_image(connection, "images/extra/2.png")
# pathh = mlx.mlx_png_file_to_image(connection, "images/extra/3.png")
# color = mlx.mlx_png_file_to_image(connection, "images/extra/4.png")


# for i in range(0, 101, 25):
#     if i == 0:
#         mlx.mlx_do_sync(connection)
#         sleep(1)
#         mlx.mlx_string_put(connection, window_connection, 400, 475, 0x39FF14, f"Reading config.txt")
#     elif i == 25:
#         mlx.mlx_string_put(connection, B915579393913D51555539513B9539393D515393AAC5556AAC6AC556D3956A96C6C3C6C6C5387C6A86953D3C6956B95516A956C5513AB955556E953AC52D4543BAD16A93C56A97913AAAC2D539516BC2956953D46C3856E8393AC56AAAAC3C53C696D43AA956BC55556C5396AAAA9556AAC7AD385569556AAC53C555155554696AEC69556A95696A953C3956C53A9553A9393956D455543B92A95296ABA96C3BB96AAD3AEAC6A855553953C2AEAC3AABC2A8556A8696C52A96D3AE93956ABA96C3C3E84696AC5392A96917AC6952C56AC55686AD387C3C3969693AAEAC3AC56D16D4557C5393A9456C53C3EC3A96C6C3ABAA95556939539556AAA87955383A956AC5553AAAC6839556AAD46917AC6E9693C2EC2B9691796AAC396C47952C5396C56D13A92E9693C6A96A96D2C3C695552D6916C555556C6AA9696C556ABC693ABA93C395693AE93939553B92EC3A9157968556C6C46C56C396C296AAC697A86A93AAAC53A94395539555393EAB96ABC695296C786C6AE93AAC7C43BAAD53AAC3AA87C453C3EC553C553C56EAC5393C6A85386AD42C69117C3A95396913C53D503BAAC392A9685693A956AE956C696A96AC57A956AAA83AAAEAD6956AAAD3C56D513A96A969556A9786AEAC6E9695457AAA9291553A86ABAC3C39568569692953C3C39552EC6AEAD3C6A9686B87AAB9479692EC3A947AAD56913C3838556A9456A96AAA956D68552AC396C5556AE96EAC557AE953C292C6AD513E93EA96AD155796969129553C547C3C2E93C396C3AC5283A96939696D6AEABF853FFFC3E96C56A93C693AAC46968696915696AFC7857FBC3AD1396AC396C6C5796BA96D6C156D2FFFAFFF83AC56C6BC3AC5539396B86C5553C555293FAFD52AC17953856C157AAAA94455553C5553C2EFAFFFAC3A96BC4793853AAC68793B93C3953AD6914539696C6943956AE96AAD5696AC683AA92C53AE93AE96915696AD5456968539696956EAEA8796C56A85696C53C7C395396BC7C69694553C56A9691556A95693BC517AC3AC529539696D3969396C3AC53D6C556AC13C387AA956A96AD4556A96AA97AC53C51553BC3EC3AC56C6D3AC5695393C43AAC3C53C39697AA9693AC555513AA95547AAC53EC43857ABAC3856AC56C2D53956AA869393AA97C553C6956C43AC3969517C53AAB96AC3AAAC6AC1517C53A95396C3AC3C3C553C2A86D296AAC53C3C7A917AC6BAA97A8547A957A96AC556AD2C3B87C53AAC3A952AC296E95546952ABC5553C3C3C2A939686BAAC3AAD2C5547955696A8393BABA96D6C6C6BC52AC3AAC3C5397969552BAAC6AAAAA85551793855287C6C5695683C3E93C2C69386A86C553C3AC693EC155793C53EC3A96AD2B96C692C553947C6956C53A9396C53A952C47C3C2AD396A953A87953853B96C2C69556AABA9393AD6C52AD283EAA9696E96AC53E93A9396A86AAAC695396C3AEA96AABC5569417A96AC6C2D2C7AA85543C693AA96AD6AC13956BA9683C553C56956A8793C796C6AC3C53C3AAA956AC3AA93D4553A97AE96C396957A9293C3AEC4693A96AC6C5513C683C5695683A93AAC6C3AC39556A869479553AC3D2A953AD56AC6AAAD556C3C4793AA96956B96ABC3AAABAA9396956A85393969556C6AE96916C3C696AC6AC6AC6B853AC7C6C456D5555456D6C554556D4554556D5447C6window_connection, 400, 475, 0x39FF14, f"Generating Empty Maze")
#     elif i == 50:
#         mlx.mlx_string_put(connection, window_connection, 400, 475, 0x39FF14, f"Generating Paths")
#     elif i == 75:
#         mlx.mlx_string_put(connection, window_connection, 400, 475, 0x39FF14, f"Final Touches")
#     elif i == 100:
#         mlx.mlx_string_put(connection, window_connection, 400, 475, 0x39FF14, f"Loading Completed!")



    # mlx.mlx_string_put(connection, window_connection, 400, 500, 0x39FF14, f"Loading.. {i}")
    # mlx.mlx_do_sync(connection)
    # sleep(1)
    # mlx.mlx_clear_window(connection, window_connection)

# mlx.mlx_string_put(connection, window_connection, 750, 475, 0x66FCF1, f"Loading.. {100}")
# mlx.mlx_clear_window(connection, window_connection)






# mlx.mlx_put_image_to_window(connection, window_connection, regen[0], 1023, 600)
# mlx.mlx_put_image_to_window(connection, window_connection, pathh[0], 1500, 600)
# mlx.mlx_put_image_to_window(connection, window_connection, color[0], 1023, 670)
# mlx.mlx_put_image_to_window(connection, window_connection, quitt[0], 1500, 670)


def buttons(keynum, mystuff):
    global indx_them
    global data
    global show_path
    if keynum == 113 or keynum == 81:  # q or Q to quit
        obj = mystuff["mlx"]
        obj.mlx_destroy_window(mystuff["m_ptr"], mystuff["w_ptr"])
        obj.mlx_release(mystuff["m_ptr"])
    
    elif keynum == 99 or keynum == 67:  # c or C to change the color
        indx_them += 1
        if indx_them >= len(thems):
            indx_them = 0
        display_output(data, False)
    
    elif keynum == 114 or keynum == 82:
        from a_maze_ing import send_specs
        from algorithm.find_paths import run
        run()
        show_path = True
        display_output(send_specs(), False)
    
    elif keynum == 115 or keynum == 83:
        display_output(data, False)


