import turtle
import math

window = None
WINX, WINY = 960, 960
turtle.tracer(False)  # Disable animation for faster drawing

piece_images = {}
piece_turtles = []
cur_turn = 'white'


def main():
    global selected_piece, board, piece_images, piece_turtles
    selected_piece = None

    def setupWin():
        global window
        window = turtle.Screen()
        window.setup(WINX, WINY)
        window.bgcolor("white")

    setupWin()

    # Register PNG images
    piece_names = ["pawn", "knight", "bishop", "rook", "queen", "king"]
    colors = ["white", "black"]
    for color in colors:
        for name in piece_names:
            filename = f"pieces/{color}-{name}.gif"
            turtle.register_shape(filename)
            piece_images[(name, color)] = filename

    BoardTurt = turtle.Turtle()
    PieceTurt = turtle.Turtle()

    # Flip Y-axis: white is at the bottom
    turtle.setworldcoordinates(0, 8, 8, 0)

    board = []

    def CreateBoard():
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
            ["rook", "black"],
            ["knight", "black"],
            ["bishop", "black"],
            ["queen", "black"],
            ["king", "black"],
            ["bishop", "black"],
            ["knight", "black"],
            ["rook", "black"],
        ]
        board[-1] = [
            ["rook", "white"],
            ["knight", "white"],
            ["bishop", "white"],
            ["queen", "white"],
            ["king", "white"],
            ["bishop", "white"],
            ["knight", "white"],
            ["rook", "white"],
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
                for _ in range(4):
                    BoardTurt.forward(1)
                    BoardTurt.right(-90)
                BoardTurt.end_fill()

    DrawBoard()
    turtle.update()

    def CreateMovesList():
        global valid_moves
        valid_moves = {}

        # Basic moves, used except for pawn special moves
        valid_moves["knight"] = [
            [1, 2], [2, 1], [-1, 2], [-2, 1],
            [1, -2], [2, -1], [-1, -2], [-2, -1],
        ]
        valid_moves["king"] = [
            [0, 1], [1, 0], [0, -1], [-1, 0],
            [1, 1], [1, -1], [-1, 1], [-1, -1],
        ]

        valid_moves["rook"] = []
        for i in range(1, 8):
            valid_moves["rook"].extend([[i, 0], [-i, 0], [0, i], [0, -i]])

        valid_moves["bishop"] = []
        for i in range(1, 8):
            valid_moves["bishop"].extend([[i, i], [-i, -i], [i, -i], [-i, i]])

        valid_moves["queen"] = valid_moves["rook"] + valid_moves["bishop"]

    CreateMovesList()

    def IsPathClear(x0, y0, dx, dy):
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            return True
        step_x = dx // steps if dx != 0 else 0
        step_y = dy // steps if dy != 0 else 0
        for step in range(1, steps):
            nx = x0 + step_x * step
            ny = y0 + step_y * step
            if board[ny][nx] != []:
                return False
        return True

    def UpdateBoard():
        global selected_piece, piece_turtles
        PieceTurt.clear()

        # Remove previous turtles
        for t in piece_turtles:
            t.hideturtle()
            t.clear()
        piece_turtles.clear()

        for y in range(8):
            for x in range(8):
                piece = board[y][x]
                if piece:
                    piece_type, piece_color = piece
                    img = piece_images.get((piece_type, piece_color))
                    if img:
                        t = turtle.Turtle()
                        t.penup()
                        t.shape(img)
                        t.goto(x + 0.5, y + 0.5)
                        t.setheading(0)
                        t.speed(0)
                        t.turtlesize(1)
                        t.showturtle()
                        piece_turtles.append(t)

        if selected_piece is not None:
            PieceTurt.pencolor("green")
            PieceTurt.penup()
            PieceTurt.goto(selected_piece[0] + 0.1, selected_piece[1] + 0.1)
            PieceTurt.pendown()
            for _ in range(4):
                PieceTurt.forward(0.8)
                PieceTurt.right(-90)
            PieceTurt.penup()

            PieceTurt.pencolor("red")
            x0, y0 = selected_piece
            piece = board[y0][x0]
            if piece:
                piece_type, piece_color = piece

                if piece_type == "pawn":
                    direction = -1 if piece_color == "white" else 1
                    moves = []

                    # Forward 1
                    if 0 <= y0 + direction < 8 and board[y0 + direction][x0] == []:
                        moves.append([0, 1])

                        # Forward 2 from start row if clear
                        start_row = 6 if piece_color == "white" else 1
                        if y0 == start_row and board[y0 + 2 * direction][x0] == []:
                            moves.append([0, 2])

                    # Diagonal captures
                    for dx in [-1, 1]:
                        nx, ny = x0 + dx, y0 + direction
                        if 0 <= nx < 8 and 0 <= ny < 8:
                            target = board[ny][nx]
                            if target != [] and target[1] != piece_color:
                                moves.append([dx, 1])
                else:
                    moves = valid_moves[piece_type].copy()

                for move in moves:
                    dx, dy = move if piece_type != "pawn" else (move[0], move[1] * direction)
                    x, y = x0 + dx, y0 + dy
                    if 0 <= x < 8 and 0 <= y < 8:
                        if piece_type == "pawn":
                            # Pawn moves already validated above
                            pass
                        else:
                            # For other pieces, check capture or empty square
                            if board[y][x] != [] and board[y][x][1] == piece_color:
                                continue
                            if piece_type != "knight" and not IsPathClear(x0, y0, dx, dy):
                                continue

                        # Draw red square for valid move
                        PieceTurt.goto(x + 0.1, y + 0.1)
                        PieceTurt.pendown()
                        for _ in range(4):
                            PieceTurt.forward(0.8)
                            PieceTurt.right(-90)
                        PieceTurt.penup()

            PieceTurt.pencolor("black")

        PieceTurt.goto(0, 0)
        turtle.update()
        turtle.ontimer(UpdateBoard, 100)

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

                if piece_type == "pawn":
                    direction = -1 if piece_color == "white" else 1
                    moves = []

                    # Forward 1
                    if 0 <= y0 + direction < 8 and board[y0 + direction][x0] == []:
                        moves.append([0, 1])

                        # Forward 2 from start row if clear
                        start_row = 6 if piece_color == "white" else 1
                        if y0 == start_row and board[y0 + 2 * direction][x0] == []:
                            moves.append([0, 2])

                    # Diagonal captures
                    for dx in [-1, 1]:
                        nx, ny = x0 + dx, y0 + direction
                        if 0 <= nx < 8 and 0 <= ny < 8:
                            target = board[ny][nx]
                            if target != [] and target[1] != piece_color:
                                moves.append([dx, 1])
                else:
                    moves = valid_moves[piece_type].copy()

                for move in moves:
                    dx, dy = move if piece_type != "pawn" else (move[0], move[1] * direction)
                    target_x, target_y = x0 + dx, y0 + dy

                    if target_x == x and target_y == y:
                        if piece_type == "pawn":
                            # pawn forward moves must be to empty square,
                            # diagonal moves must capture enemy piece
                            if dx == 0:
                                # forward move
                                if board[target_y][target_x] == []:
                                    board[target_y][target_x] = board[y0][x0]
                                    board[y0][x0] = []
                                    selected_piece = None
                                    return
                            else:
                                # pawn capture
                                if board[target_y][target_x] != [] and board[target_y][target_x][1] != piece_color:
                                    board[target_y][target_x] = board[y0][x0]
                                    board[y0][x0] = []
                                    selected_piece = None
                                    return
                        else:
                            # For other pieces, check path clear and capture or move
                            if board[target_y][target_x] == [] or board[target_y][target_x][1] != piece_color:
                                if piece_type == "knight" or IsPathClear(x0, y0, dx, dy):
                                    board[target_y][target_x] = board[y0][x0]
                                    board[y0][x0] = []
                                    selected_piece = None
                                    return

            selected_piece = None
            

    turtle.onscreenclick(ScreenClicked)
    UpdateBoard()
    window.mainloop()


main()
