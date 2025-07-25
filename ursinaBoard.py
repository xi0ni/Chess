from ursina import *


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
        board[1] = [['p','b'],['p','b'],['p','b'],['p','b'],['p','b'],['p','b'],['p','b'],['p','b'],['p','b']]
        board[-2] = [['p','w'],['p','w'],['p','w'],['p','w'],['p','w'],['p','w'],['p','w'],['p','w'],['p','w']]

        board[0] = [['r','b'],['h','b'],['b','b'],['q','b'],['k','b'],['k','b'],['b','b'],['h','b'],['c','b']]
        board[-1] = [['r','w'],['h','w'],['b','w'],['q','w'],['k','w'],['k','w'],['b','w'],['h','w'],['c','w']]

    CreateBoard()

    app = Ursina()

    camera.orthographic = True
    camera.fov = 10
    camera.position = (3, 3.5)
    Text.default_resolution *= 2

    player = Entity(name=" ", color=color.azure)

    cursor = Tooltip(
        player.name, color=player.color, origin=(0, 0), scale=4, enabled=True
    )
    cursor.background.color = color.clear

    bg = Entity(
        parent=scene,
        model="quad",
        texture="sky_default",
        scale=(160, 80),
        z=10,
        color=color.light_gray,
    )

    board = [[None for x in range(8)] for y in range(8)]
    for y in range(8):
        for x in range(8):
            b = Button(parent=scene, position=(x, y))
            board[x][y] = b

    app.run()


if __name__ == "__main__":
    main()
