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
    white["rook"].position = (0, 0, -1)
    white["knight"].position = (1, 0, -1)
    white["bishop"].position = (2, 0, -1)
    white["queen"].position = (3, 0, -1)
    white["king"].position = (4, 0, -1)
    white["bishop1"].position = (5, 0, -1)
    white["knight1"].position = (6, 0, -1)
    white["rook1"].position = (7, 0, -1)

    for x in range(8):
        white["pawns"][x].position = (x, 1, -1)

    # Place black pieces (top)
    black["rook"].position = (0, 7, -1)
    black["knight"].position = (1, 7, -1)
    black["bishop"].position = (2, 7, -1)
    black["queen"].position = (3, 7, -1)
    black["king"].position = (4, 7, -1)
    black["bishop1"].position = (5, 7, -1)
    black["knight1"].position = (6, 7, -1)
    black["rook1"].position = (7, 7, -1)

    for x in range(8):
        black["pawns"][x].position = (x, 6, -1)

