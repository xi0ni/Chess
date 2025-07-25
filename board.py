# imports
import turtle

window = None
WINX, WINY = 1000, 1000


def Board():
    board_turt = turtle.Turtle()
    board_turt.hideturtle()
    turtle.setworldcoordinates(0, 0, 8, 8)
    turtle.tracer(False)

    def setupWin():
        global window
        # making turtle object
        window = turtle.Screen()
        # set screen size
        window.setup(WINX, WINY)
        # set background color
        window.bgcolor("white")

    def DrawBoard():
        # repeats 10 times for the 9 rows
        for i in range(9):
            # draws the vertical line
            board_turt.penup()
            board_turt.goto(i, 0)
            board_turt.pendown()
            board_turt.goto(i, 8)

        # repeats 10 times
        for i in range(9):
            # draws the horizontal line
            board_turt.penup()
            board_turt.goto(0, i)
            board_turt.pendown()
            board_turt.goto(8, i)

    setupWin()

    # creates the board object
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
            ["p", "w"],
        ]

        board[0] = [
            ["r", "b"],
            ["k", "b"],
            ["b", "b"],
            ["c", "b"],
            ["q", "b"],
            ["k", "b"],
            ["b", "b"],
            ["k", "b"],
            ["c", "b"],
        ]
        board[-1] = [
            ["r", "w"],
            ["k", "w"],
            ["b", "w"],
            ["c", "w"],
            ["q", "w"],
            ["k", "w"],
            ["b", "w"],
            ["k", "w"],
            ["c", "w"],
        ]

    CreateBoard()
    for i in board:
        print(i)

    DrawBoard()
    turtle.update()

    window.mainloop()
