from mlx import Mlx
from time import sleep

images = {
    "1": "default_images/1.png", "2": "default_images/2.png",
    "3": "default_images/3.png", "4": "default_images/4.png",
    "5": "default_images/5.png", "6": "default_images/6.png",
    "7": "default_images/7.png", "8": "default_images/8.png",
    "9": "default_images/9.png", "A": "default_images/A.png",
    "B": "default_images/B.png", "C": "default_images/C.png",
    "D": "default_images/D.png", "E": "default_images/E.png",
    "F": "default_images/F.png", "0": "default_images/0.png",
    "entry": "default_images/entry.png",
    "exit": "default_images/exit.png"
}

string = "B9393D51393955539553AAAAA956C6C6D396E952AAAAEC551555386D16BAC6AAD153A9556C396946952C5696EC53D3AAD453AD43D3A955383C2C5396839692C6956AC3C156C3EAC56C17C53C7C3E953E9695556F97AFFF83ABC383A9157FC5057FAC683AEAAAC53FFFAFFFAD16EA96AC79453FAFD529693AAD453AD52FAFFFC696C2853B8693C7C55393A93AA96C696A95157C6AC2AAAC393ABC6BC3953C3AAAABC6AA813C3C6BC56AAAAC53C6EAC543929556AEC392D156B93AEC6953C3D46C56D546C45556D456"


def get_center(width: int, maze_width: int) -> int:
    pixels_width = 32 * maze_width 
    return (width - pixels_width) // 2

def get_coordinates(width: int, height: int, point: tuple[int, int]) -> tuple[int, int]:
    coordinates = [width + point[0] + 32 * point[0], height + point[1] + 32 * point[1]]
    if point[0] > 1:
        coordinates[0] -= 20
    if point[1] > 1:
        coordinates[1] -= 20
    if not point[0]:
        coordinates[0] = width
    if not point[1]:
        coordinates[1] = height
    return coordinates[0], coordinates[1]
    


mlx = Mlx()
connection = mlx.mlx_init()
window_connection = mlx.mlx_new_window(connection, 1500, 950, "Test Project")
c = get_center(1500, 20)
r = 50
d = 1
point = get_coordinates(c, r, ( 19, 19))
entry = mlx.mlx_png_file_to_image(connection, images["entry"])
exit= mlx.mlx_png_file_to_image(connection, images["exit"])


for i in string:

    
    image = mlx.mlx_png_file_to_image(connection, images[f"{i}"])
    mlx.mlx_put_image_to_window(connection, window_connection, image[0], c, r)
    mlx.mlx_do_sync(connection)
    sleep(0.001)
    c += 32
    
    if d % 20 == 0 and d != 0:
        r += 32
        c = get_center(1500, 20)    
    d += 1
    

mlx.mlx_put_image_to_window(connection, window_connection, entry[0], point[0], point[1])
# mlx.mlx_put_image_to_window(connection, window_connection, exit[0], 1038, 658)


def mykey(keynum, mystuff):
    
    if keynum == 32:
        obj = mystuff["mlx"]
        obj.mlx_destroy_window(mystuff["m_ptr"], mystuff["w_ptr"])
        obj.mlx_release(mystuff["m_ptr"])


mlx.mlx_key_hook(window_connection,  mykey, {"m_ptr": connection, "w_ptr": window_connection, "mlx": mlx})

mlx.mlx_loop(connection)