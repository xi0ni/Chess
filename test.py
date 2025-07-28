import turtle
import math

window = None
WINX, WINY = 800, 800
turtle.tracer(False)  # Disable animation for faster drawing


def main():
    global selected_piece
    selected_piece = None

    def setupWin():
        global window
        window = turtle.Screen()
        window.setup(WINX, WINY)
        window.bgcolor("white")

    setupWin()

    BoardTurt = turtle.Turtle()
    PieceTurt = turtle.Turtle()

    turtle.setworldcoordinates(0, 0, 8, 8)

    global board
    board = []

    def CreateBoard():
        global board
        BoardTurt.ht()
        PieceTurt.ht()
        PieceTurt.penup()
        PieceTurt.pensize(10)
        BoardTurt.pensize(5)

        for y in range(8):
            y_list = []
            for x in range(8):
                y_list.append([])
            board.append(y_list)

        board[1] = [["pawn", "black"]] * 8
        board[-2] = [["pawn", "white"]] * 8

        board[0] = [
            ["rook", "black"], ["knight", "black"], ["bishop", "black"], ["queen", "black"],
            ["king", "black"], ["bishop", "black"], ["knight", "black"], ["rook", "black"]
        ]
        board[-1] = [
            ["rook", "white"], ["knight", "white"], ["bishop", "white"], ["queen", "white"],
            ["king", "white"], ["bishop", "white"], ["knight", "white"], ["rook", "white"]
        ]

    CreateBoard()

    def DrawBoard():
        for y in range(8):
            for x in range(8):
                BoardTurt.penup()
                BoardTurt.goto(x, y)
                BoardTurt.pendown()
                BoardTurt.fillcolor("white" if (x + y) % 2 == 0 else "brown")
                BoardTurt.begin_fill()
                for i in range(4):
                    BoardTurt.forward(1)
                    BoardTurt.right(-90)
                BoardTurt.end_fill()

    DrawBoard()
    turtle.update()

    def CreateMovesList():
        global valid_moves
        valid_moves = {}

        valid_moves["pawn"] = [[0, 1]] 
        valid_moves["knight"] = [
            [1, 2], [2, 1], [-1, 2], [-2, 1],
            [1, -2], [2, -1], [-1, -2], [-2, -1]
        ]
        valid_moves["king"] = [
            [0, 1], [1, 0], [0, -1], [-1, 0],
            [1, 1], [1, -1], [-1, 1], [-1, -1]
        ]

        valid_moves["rook"] = []
        for i in range(1, 8):
            valid_moves["rook"].extend([[i, 0], [-i, 0], [0, i], [0, -i]])

        valid_moves["bishop"] = []
        for i in range(1, 8):
            valid_moves["bishop"].extend([[i, i], [-i, -i], [i, -i], [-i, i]])

        valid_moves["queen"] = valid_moves["rook"] + valid_moves["bishop"]

    CreateMovesList()

    def UpdateBoard():
        global selected_piece
        PieceTurt.clear()

        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] != []:
                    PieceTurt.penup()
                    PieceTurt.goto(x + 0.5, y + 0.5)
                    PieceTurt.write(board[y][x][1], align="center", font=("Arial", 20, "normal"))
                    PieceTurt.goto(x + 0.5, y + 0.2)
                    PieceTurt.write(board[y][x][0], align="center", font=("Arial", 20, "normal"))

        if selected_piece is not None:
            PieceTurt.pencolor("green")
            PieceTurt.penup()
            PieceTurt.goto(selected_piece[0] + 0.1, selected_piece[1] + 0.1)
            PieceTurt.pendown()
            for _ in range(4):
                PieceTurt.forward(0.8)
                PieceTurt.right(-90)
            PieceTurt.penup()

            # Highlight valid moves in red
            PieceTurt.pencolor("red")
            x0, y0 = selected_piece
            piece = board[y0][x0]
            if piece:
                piece_type, piece_color = piece
                moves = valid_moves[piece_type].copy()
                direction = -1 if piece_color == "white" else 1
                start_row = 6 if piece_color == "white" else 1

                if piece_type == "pawn" and y0 == start_row:
                    moves.append([0, 2])

                for move in moves:
                    dx, dy = move[0], move[1] * direction if piece_type == "pawn" else move[1]
                    x, y = x0 + dx, y0 + dy
                    if 0 <= x < 8 and 0 <= y < 8:
                        if board[y][x] == [] or board[y][x][1] != piece_color:
                            PieceTurt.goto(x + 0.1, y + 0.1)
                            PieceTurt.pendown()
                            for _ in range(4):
                                PieceTurt.forward(0.8)
                                PieceTurt.right(-90)
                            PieceTurt.penup()

            PieceTurt.pencolor("black")

        PieceTurt.goto(0, 0)
        turtle.update()
        turtle.ontimer(UpdateBoard, 10)

    def ScreenClicked(x, y):
        global selected_piece, board
        x = int(math.floor(x))
        y = int(math.floor(y))

        if not (0 <= x < 8 and 0 <= y < 8):
            return

        if selected_piece is None:
            if board[y][x] != []:
                selected_piece = [x, y]
        else:
            x0, y0 = selected_piece
            piece = board[y0][x0]
            if piece:
                piece_type, piece_color = piece
                moves = valid_moves[piece_type].copy()
                direction = -1 if piece_color == "white" else 1
                start_row = 6 if piece_color == "white" else 1

                if piece_type == "pawn" and y0 == start_row:
                    moves.append([0, 2])

                for move in moves:
                    dx, dy = move[0], move[1] * direction if piece_type == "pawn" else move[1]
                    target_x, target_y = x0 + dx, y0 + dy
                    if target_x == x and target_y == y:
                        if board[y][x] == [] or board[y][x][1] != piece_color:
                            board[y][x] = board[y0][x0]
                            board[y0][x0] = []
                            selected_piece = None
                            return

            selected_piece = None

    turtle.onscreenclick(ScreenClicked)
    UpdateBoard()
    window.mainloop()


main()
