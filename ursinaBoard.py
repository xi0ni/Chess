from ursina import *
from pieces import Piece

board = []


def CreateBoard():
    global board
    # Initialize an empty 8x8 board filled with None
    board = [[None for _ in range(8)] for _ in range(8)]

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
    back_row_white = [
        white["rook"],
        white["knight"],
        white["bishop"],
        white["queen"],
        white["king"],
        white["bishop1"],
        white["knight1"],
        white["rook1"],
    ]
    for x, piece in enumerate(back_row_white):
        piece.place(x, 0, -1)
        board[0][x] = piece

    for x in range(8):
        pawn = white["pawns"][x]
        pawn.place(x, 1, -1)
        board[1][x] = pawn

    # Place black pieces (top)
    back_row_black = [
        black["rook"],
        black["knight"],
        black["bishop"],
        black["queen"],
        black["king"],
        black["bishop1"],
        black["knight1"],
        black["rook1"],
    ]
    for x, piece in enumerate(back_row_black):
        piece.place(x, 7, -1)
        board[7][x] = piece

    for x in range(8):
        pawn = black["pawns"][x]
        pawn.place(x, 6, -1)
        board[6][x] = pawn


# variables to hold player and cursor
player = Piece("white", "rook")
cursor = Entity(model="quad", texture=player.texture, scale=1)
clicked = False


def update():
    global clicked, player

<<<<<<< HEAD
        if mouse.hovered_entity:
            print(mouse.hovered_entity)
            player = mouse.hovered_entity
            cursor.texture = player.texture
=======
    if mouse.left and not clicked:
        clicked = True

        # turn mouse position to board coordinates (0-7) cuz its oigionally 0-1
        board_x = int((mouse.position.x + 1) * 4)
        board_y = int((mouse.position.y + 1) * 4)

        # makes sure coords are within board bounds
        if 0 <= board_x < 8 and 0 <= board_y < 8:
            if mouse.hovered_entity:
                clear_square(board_x, board_y)
                player = mouse.hovered_entity
                if player.texture != '':
                    cursor.texture = player.texture
            else:
                print(f"No hovered entity at ({board_x}, {board_y})")

>>>>>>> 1a9b77b1433f04b55f93e28c417d722171a18d9b
    elif not mouse.left:
        clicked = False

    # Update cursor position
    cursor.position = mouse.position * 10 + Vec3(3, 3.5, -0.5)



def clear_square(x, y):
    global board
    piece = board[y][x]
    if piece:
        piece.disable()
        board[y][x] = None
