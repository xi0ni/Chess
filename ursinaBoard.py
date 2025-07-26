from ursina import *
import emoji
from pieces import Piece


def main():
    # creates the board object for our data structure
    board = []

    # defines a create board method
    def CreateBoard():
        # creates a blank board
        for y in range(8):
            y_list = []
            for x in range(8):
                y_list.append([])

            board.append(y_list)

        # sets the second and second to last rows to pawns
        # the first part in the list signifies the piece and the second part signifies the color of the piece so you cant take your own pieces
        board[1] = [
            ["p", "b"],
            ["p", "b"],
            ["p", "b"],
            ["p", "b"],
            ["p", "b"],
            ["p", "b"],
            ["p", "b"],
            ["p", "b"],
        ]
        board[-2] = [
            ["p", "w"],
            ["p", "w"],
            ["p", "w"],
            ["p", "w"],
            ["p", "w"],
            ["p", "w"],
            ["p", "w"],
            ["p", "w"],
        ]

        board[0] = [
            ["r", "b"],
            ["h", "b"],
            ["b", "b"],
            ["q", "b"],
            ["k", "b"],
            ["b", "b"],
            ["h", "b"],
            ["c", "b"],
        ]
        board[-1] = [
            ["r", "w"],
            ["h", "w"],
            ["b", "w"],
            ["q", "w"],
            ["k", "w"],
            ["b", "w"],
            ["h", "w"],
            ["c", "w"],
        ]

    CreateBoard()

    app = Ursina()

    # sets camera in place for the board
    camera.orthographic = True
    camera.fov = 10
    camera.position = (3, 3.5)
    Text.default_resolution *= 2

    # movable cursor to click pieces
    player = Piece("black", "bishop")
    # player.texture("black", "bishop")

    cursor = Tooltip(
        player.name,
        color=color.black if player.color == "black" else color.white,
        origin=(0, 0),
        scale=4,
        enabled=True,
    )

    cursor.background.color = color.clear

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
            if x % 2 == 1 - y % 2:
                b = Button(parent=scene, position=(x, y), color=rgb(255, 255, 255))
            else:
                b = Button(parent=scene, position=(x, y), color=rgb(0, 0, 0))

            b_board[x][y] = b

    app.run()


if __name__ == "__main__":
    main()
