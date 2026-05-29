from mlx import Mlx
from time import sleep


mlx = Mlx()
connection = mlx.mlx_init()
window_connection = mlx.mlx_new_window(connection, 2560, 1440, "A_MAZE_ING")

first_set = {
    "1": "images/first_set/1.png", "2": "images/first_set/2.png", "3": "images/first_set/3.png",
    "4": "images/first_set/4.png", "5": "images/first_set/5.png", "6": "images/first_set/6.png",
    "7": "images/first_set/7.png", "8": "images/first_set/8.png", "9": "images/first_set/9.png",
    "A": "images/first_set/A.png", "B": "images/first_set/B.png", "C": "images/first_set/C.png",
    "D": "images/first_set/D.png", "E": "images/first_set/E.png", "F": "images/first_set/F.png",
    "0": "images/first_set/0.png", "entry": "images/first_set/entry.png",
    "exit": "images/first_set/exit.png"
}

second_set = {
    "1": "images/second_set/1.png", "2": "images/second_set/2.png", "3": "images/second_set/3.png",
    "4": "images/second_set/4.png", "5": "images/second_set/5.png", "6": "images/second_set/6.png",
    "7": "images/second_set/7.png", "8": "images/second_set/8.png", "9": "images/second_set/9.png",
    "A": "images/second_set/A.png", "B": "images/second_set/B.png", "C": "images/second_set/C.png",
    "D": "images/second_set/D.png", "E": "images/second_set/E.png", "F": "images/second_set/F.png",
    "0": "images/second_set/0.png", "entry": "images/second_set/entry.png",
    "exit": "images/second_set/exit.png"
}

string = "9157913D13939179555555153B93915553B953939391555179153B939553AE93AAC3AC6AAC56955393A96C2C6A93D06C3C6C6C6A957A96ABC2AC6D3A856AAABAC17AC553C3D2AAAC53E93AAC3E956D55117AA956C3AC16C3D12AE93C6AAC3E92957C3C3C6AC3BC56AAC3C56D1553AA96C4557AC3A93C16EA96C55683C56AC3956BAD52968539687AD155697AAAC539553ABAEAC3A93AA93913AA957C16C3D2A9386D43AC3A9696957856AC53C457C46A9696AAC2AEC2AC6C6917A95692C6AE9396ABAC456D4552D5295079551556ABC56AD6853AC39552C52A956E95296A83C6A95515553C53EAD696956953A83D3A93C7AC3C693E93EC29516D6ABAEC5546D5693BAD545693C3A95696AAC3AC6A956D6956C56C556AD693946C139539553AAAC53953AC56AC3BC56C3C2B968395569791393952956AC393EAC3C6D3AAA817C6BC695547C4555383C2C3AC6955456AC6AC3AAD3C3AAC543A9512C6AAC3914796B95117917AEC3ABAAD52D5517A9547AAC3C3C6AD516A87AE956C3AAC55692C3AE96C3C516C6AA93C395296C5396E969297C13ABAE92969396C6D1552A96C56952B969392C6C3C6D6A9796C39692C693EAAAC56AC56AC5553E93EAA9157C3AAABAC6A953C5395685697C696E93AC3A84553C393A9553C56C3AC6A9392C6AAA93AC3C53AAD3C53A9178556AC3AAA95387AEAAAD3C1517C43BAAC6E93AAAAAA9693C683853AC2C56955696AAA87AE9456AC147C3A95546AA9556C46AAAEAD68556AC7AC3C3B96953C3C6AAFC56FFFC3E9396AA91396C4555793AAC3C53E95569543AD4683C3C1693AAFD5157F9296AABAAEAEC3951553AA869293C56D156D56C393E83AD296AEAFFFAFFFAEC3AAC6C3853AC3E93AAAE96AEC3913A9555556AC56EC3AC3C3A93FAFD54556AA9396E92C3C56AC6A96BA956AAC6C395553A955396ABABC6AEFAFFFB9556C2AAD16C3A93BC53C6D468556C3956A957AAA97AC3C6AC5129503D12C5553E8456D16AAA83BC39553A953BC6D12C552C06947C53A93EC696C3AC5153C3A9553A946C6C47C457AC6BC4553EC393C3A969553C6AC393C396C796BA96EC3BAEAB955555555529529553A93C2ABAAC5693C39296AC56C1556B86A953C2C52AC539555157AC3C4796AAC3EA86C5552C7C6AA9693D1693D443C6947A93C43BAC53BC55696953A96ABC56C55553E9553AA83AC3E96C553A956956AC3D46A97AC539387ABAAC3A85539517969697C6AEAC3C569553AEC556956BA9556A9693C6AA9686A96AC17AC3C3AD2B8153C38545396D528155796916C6D152A96C552AABA96C5696943C3AC5686C3A96E93BAA953AEA953AD2E9513E92C695796AAC469157A96D47AA913C3BAAAD16A86C696C3C47AA96947AA92C57853ABAC5556A93AA95556AAAC7AAAEC56BAC157AD54553AAA9693AC6E9396BC6AC395792AC6AC53D3C6C5546A915786D693A95553AAAAC3AC69556C6D03D2946956EC53C5569455539392AC394553AAC47916C6A856C53C393D116C3AAB9695513C553D297956EAAEC3AA93946C5396E9396C3953C3C6C3AA93C2C6A9697AAD17C568569556C556C6AAA953D46956AA93C6947A953AEAA87A956AD296C569157A93C5513D3953AAEABC393C3BC6AA956B96C3AC3AAA96C55456C55556C5546C5556C56C7C6C56C546C56C556C4556C556C546EC47"
path = "SSEENESSENNNESSSSWWWNWSWSSSEESSWWSESENEEENEENESEENESEEENWNNEENWNEENWNWWWNNESEENEEEEEEESSSESWSWNNNNWSSWNNWWWSESESSSENESSWWSWWWSSWWSESSWSESENENENWNNEENESSESENNWNENNENESSSEESSWWNWSSSEESSSSSWNNNWNWSSESWSESWWNWWSESSESWSESEESENNNNWNENESSESENNNNNNEESSEENENNWNNWSWWNNNNWNEESENEEESSENNNESSSSWWSWSEENESSSSSESWSSEEENWNENESSSSWWWSEEEESESWSSENEESWSWWSEEENEENNWNWNEEESSEENNENNNWNNWNENNNNWSWNNENWNEESSEENENESESWWSESWSWNWSSSENEEENESENNNNENWWNNWWWWWNWNEENEESWSEENNNNENNESESWSEENNNWNWNNESENEEESSSSSWNWSSSSENESSWSESSSWSWNWSSSSSSENNNNESSSESWSWSWSWNNNNWSSSWNNWWWWWSESEENESSEESESENEEESSSSWWWNWWWWSEESSWSSENENESEEESWSSWNWWSWSWNWSWWWSESENESESSESENNNNENESESESSWSE"

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

        image = mlx.mlx_png_file_to_image(connection, second_set[f"{cell}"])
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

        path_pixel = mlx.mlx_png_file_to_image(connection, "images/extra/path.png")
        mlx.mlx_put_image_to_window(connection, window_connection, path_pixel[0], x, y)
        mlx.mlx_do_sync(connection)
        sleep(0.001)


def draw_points(entry_coords: list[int], exit_coords: list[int]) -> None:

    entry_img = mlx.mlx_png_file_to_image(connection, second_set["entry"]) # To be edited
    exit_img = mlx.mlx_png_file_to_image(connection, second_set["exit"]) # To be edited

    mlx.mlx_put_image_to_window(connection, window_connection, entry_img[0], entry_coords[0], entry_coords[1])
    mlx.mlx_put_image_to_window(connection, window_connection, exit_img[0], exit_coords[0], exit_coords[1])


def display_output(specs: dict[str, list[int] | str | int]) -> None:
        
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
    background = mlx.mlx_png_file_to_image(connection, "images/extra/night.png")
    mlx.mlx_put_image_to_window(connection, window_connection, background[0], 0, 0)

    draw_empty_maze(maze, maze_width, x, y)
    draw_points(entry_coords, exit_coords)
    draw_path(path, entry_coords)

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


def quit(keynum, mystuff):
    
    if keynum == 113 or keynum == 81:  # q or Q to quit
        obj = mystuff["mlx"]
        obj.mlx_destroy_window(mystuff["m_ptr"], mystuff["w_ptr"])
        obj.mlx_release(mystuff["m_ptr"])

    elif keynum == 99 or keynum == 67:  # c or C to quit
        obj = mystuff["mlx"]
        obj.mlx_destroy_window(mystuff["m_ptr"], mystuff["w_ptr"])


mlx.mlx_key_hook(window_connection,  quit, {"m_ptr": connection, "w_ptr": window_connection, "mlx": mlx})
