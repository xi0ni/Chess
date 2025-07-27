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

#black pieces dictionary
    black = {
        "rook": Piece("black", "rook"),
        "knight": Piece("black", "knight"),
        "bishop": Piece("black", "bishop"),
        "queen": Piece("black", "queen"),
        "king": Piece("black", "king"),
        "bishop1": Piece("black", "bishop"),
        "knight1": Piece("black", "knight"),
        "rook1": Piece("black", "rook"),
        "pawn": Piece("black", "pawn"),
    }

#white pieces dictionary
    white = {
        "rook": Piece("white", "rook"),
        "knight": Piece("white", "knight"),
        "bishop": Piece("white", "bishop"),
        "queen": Piece("white", "queen"),
        "king": Piece("white", "king"),
        "bishop1": Piece("white", "bishop"),
        "knight1": Piece("white", "knight"),
        "rook1": Piece("white", "rook"),
        "pawn": Piece("white", "pawn"),
    }

    # Place black pieces
    black["rook"].position = (0, 0, -1)
    black["knight"].position = (1, 0, -1)
    black["bishop"].position = (2, 0, -1)
    black["queen"].position = (3, 0, -1)
    black["king"].position = (4, 0, -1)
    black["bishop1"].position = (5, 0, -1)
    black["knight1"].position = (6, 0, -1)
    black["rook1"].position = (7, 0, -1)

    for x in range(8):
        black["pawn"].position = (x, 1, -1)

    # Place white pieces
    white["rook"].position = (0, 7, -1)
    white["knight"].position = (1, 7, -1)
    white["bishop"].position = (2, 7, -1)
    white["queen"].position = (3, 7, -1)
    white["king"].position = (4, 7, -1)
    white["bishop1"].position = (5, 7, -1)
    white["knight1"].position = (6, 7, -1)
    white["rook1"].position = (7, 7, -1)

    for x in range(8):
        white["pawn"].position = (x, 6, -1)


app = Ursina()

# variables to hold player and cursor
player = Piece("white", "rook")
cursor = Entity(model="quad", texture=player.texture, scale=1)


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
            color_tile = rgb(1, 1, 1) if x % 2 == 1 - y % 2 else rgb(0.28, 0.28, 0.27)
            b = Button(parent=scene, position=(x, y), color=color_tile)
            b_board[x][y] = b

    app.run()


if __name__ == "__main__":
    main()
