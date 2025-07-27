from ursina import *
from pieces import Piece

board = []


def CreateBoard():
    global board
    # creates a blank board
    for y in range(8):
        y_list = []
        for x in range(8):
            y_list.append([])
        board.append(y_list)

    # sets the second and second to last rows to pawns
    board[1] = [Piece("black", "pawn") for _ in range(8)]
    board[-2] = [Piece("white", "pawn") for _ in range(8)]

    board[0] = [
        Piece("black", "rook"),
        Piece("black", "knight"),
        Piece("black", "bishop"),
        Piece("black", "queen"),
        Piece("black", "king"),
        Piece("black", "bishop"),
        Piece("black", "knight"),
        Piece("black", "rook"),
    ]
    board[-1] = [
        Piece("white", "rook"),
        Piece("white", "knight"),
        Piece("white", "bishop"),
        Piece("white", "queen"),
        Piece("white", "king"),
        Piece("white", "bishop"),
        Piece("white", "knight"),
        Piece("white", "rook"),
    ]


app = Ursina()

# variables to hold player and cursor
player = Piece("white", "rook")
cursor = Entity(model="quad", texture=player.texture, scale=1)

rook = Piece("black", "rook")
rook.place(-3, 1, 1)



def update():
    mousex = (mouse.position.x) / 0.1
    mousey = (mouse.position.y) / 0.1
    if mouse.position.y >= 0.004:
        mousez = (mousey) * -1
    elif mouse.position.y < 0.004:
        mousez = (mousey) * 1

    cursor.position = (mousex + 3, mousey + 3.5, mousez)
    # print(f"mouse {mouse.position}")
    # print(f"object {cursor.position}")


def main():
    CreateBoard()

    # sets camera in place for the board
    camera.orthographic = True
    camera.fov = 10
    camera.position = (3, 3.5)
    Text.default_resolution *= 2

    # background
    bg = Entity(
        parent=scene,
        model="quad",
        texture="sky_default",
        scale=(160, 80),
        z=10,
        color=color.light_gray,
    )

    # board layout in 8x8
    b_board = [[None for x in range(8)] for y in range(8)]
    for y in range(8):
        for x in range(8):
            color_tile = rgb(255, 255, 255) if x % 2 == 1 - y % 2 else rgb(0, 0, 0)
            b = Button(parent=scene, position=(x, y), color=color_tile)
            b_board[x][y] = b

    app.run()


if __name__ == "__main__":
    main()
