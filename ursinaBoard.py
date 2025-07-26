from ursina import *
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
        board[1] = [["p", "b"] for _ in range(8)]
        board[-2] = [["p", "w"] for _ in range(8)]

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

    # setting up all the pieces
    # board[1] = [[b.color == ] for _ in range(8)]
    # board[-2] = [[] for _ in range(8)]

    player = Piece("white", "pawn")
    cursor = Entity(
        model="quad",
        texture=player.texture,
        scale=20
    )

    def update():
        # make the piece follow the mouse if desired
        cursor.position = mouse.position

    
    app.run()


if __name__ == "__main__":
    main()
