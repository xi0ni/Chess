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

    # black pieces dictionary
    black = {
        "rook": Piece("black", "rook"),
        "knight": Piece("black", "knight"),
        "bishop": Piece("black", "bishop"),
        "queen": Piece("black", "queen"),
        "king": Piece("black", "king"),
        "bishop1": Piece("black", "bishop"),
        "knight1": Piece("black", "knight"),
        "rook1": Piece("black", "rook"),
        "pawns": [Piece("black", "pawn") for _ in range(8)],
    }

    # white pieces dictionary
    white = {
        "rook": Piece("white", "rook"),
        "knight": Piece("white", "knight"),
        "bishop": Piece("white", "bishop"),
        "queen": Piece("white", "queen"),
        "king": Piece("white", "king"),
        "bishop1": Piece("white", "bishop"),
        "knight1": Piece("white", "knight"),
        "rook1": Piece("white", "rook"),
        "pawns": [Piece("white", "pawn") for _ in range(8)],
    }

    # Place white pieces (bottom)
    white["rook"].place(0,0,-1)
    white["knight"].place(1, 0, -1)
    white["bishop"].place(2, 0, -1)
    white["queen"].place(3, 0, -1)
    white["king"].place(4, 0, -1)
    white["bishop1"].place(5, 0, -1)
    white["knight1"].place(6, 0, -1)
    white["rook1"].place(7, 0, -1)

    for x in range(8):
        white["pawns"][x].place(x, 1, -1)

    # Place black pieces (top)
    black["rook"].place(0, 7, -1)
    black["knight"].place(1, 7, -1)
    black["bishop"].place(2, 7, -1)
    black["queen"].place(3, 7, -1)
    black["king"].place(4, 7, -1)
    black["bishop1"].place(5, 7, -1)
    black["knight1"].place(6, 7, -1)
    black["rook1"].place(7, 7, -1)

    for x in range(8):
        black["pawns"][x].place(x, 6, -1)


# variables to hold player and cursor
player = Piece("white", "rook")
cursor = Entity(model="quad", texture=player.texture, scale=1)
clicked = False



def update():
    global clicked, player

    if mouse.hovered_entity:
        hovered = mouse.hovered_entity
        if isinstance(hovered, Piece):
            cursor.texture = hovered.texture

    if mouse.left and not clicked:
        clicked = True
        if mouse.hovered_entity:
            hovered = mouse.hovered_entity
            if isinstance(hovered, Piece):
                player = hovered
                player.on_place()  
    elif not mouse.left:
        clicked = False

    cursor.position = mouse.position * 10 + Vec3(3, 3.5, -0.5)
