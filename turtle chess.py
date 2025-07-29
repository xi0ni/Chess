# initializes our imports 
import turtle
import math

# creates the turtle window
window = None
WINX, WINY = 1200, 960
# sets the tracer to false so the screen only updates when we want it too
turtle.tracer(False)

# creates the piece images dictionary
piece_images = {}
# creates the piece turtles list
piece_turtles = []

# creates a variable for the current active players turn
cur_turn = "white"

# defines a function to check if the path from a given square to another given square is clear
def IsPathClear(x0, y0, dx, dy):

    # returns false if one of the given two points is outside of the board
    if x0 + dx < 0 or x0 + dx >= 8 or y0 + dy < 0 or y0 + dy >= 8:
        return False
    
    # creates a steps varable that holds the max distance between the two points
    steps = max(abs(dx), abs(dy))

    # if the distance is 0 return true
    if steps == 0:
        return True
    
    # creates step variables for x and y which store how many squares we should move each time we check a square
    step_x = dx // steps if dx != 0 else 0
    step_y = dy // steps if dy != 0 else 0

    # goes through every square in that direction t
    for step in range(1, steps):
        nx = x0 + step_x * step
        ny = y0 + step_y * step
        if board[ny][nx] is not None:
            return False
    return True


class Pawn:
    def __init__(self, color):
        self.color = color
        self.type = "pawn"
        self.start_row = 6 if color == "white" else 1

    def GetValidMoves(self, x, y, board):
        moves = []
        direction = -1 if self.color == "white" else 1
        if 0 <= y + direction < 8 and board[y + direction][x] is None:
            moves.append([0, direction])
            if y == self.start_row and board[y + 2 * direction][x] is None:
                moves.append([0, 2 * direction])
        for dx in [-1, 1]:
            nx, ny = x + dx, y + direction
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[ny][nx]
                if target is not None and target.color != self.color:
                    moves.append([dx, direction])
        return moves


class Knight:
    def __init__(self, color):
        self.color = color
        self.type = "knight"

    def GetValidMoves(self, x, y, board):
        moves = [
            [1, 2],
            [2, 1],
            [-1, 2],
            [-2, 1],
            [1, -2],
            [2, -1],
            [-1, -2],
            [-2, -1],
        ]
        valid_moves = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[ny][nx]
                if target is None or target.color != self.color:
                    valid_moves.append([dx, dy])
        return valid_moves


class Bishop:
    def __init__(self, color):
        self.color = color
        self.type = "bishop"

    def GetValidMoves(self, x, y, board):
        valid_moves = []
        for i in range(1, 8):
            for dx, dy in [[i, i], [-i, -i], [i, -i], [-i, i]]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8 and IsPathClear(x, y, dx, dy):
                    target = board[ny][nx]
                    if target is None or target.color != self.color:
                        valid_moves.append([dx, dy])
        return valid_moves


class Rook:
    def __init__(self, color):
        self.color = color
        self.type = "rook"
        self.has_moved = False

    def GetValidMoves(self, x, y, board):
        valid_moves = []
        for i in range(1, 8):
            for dx, dy in [[i, 0], [-i, 0], [0, i], [0, -i]]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8 and IsPathClear(x, y, dx, dy):
                    target = board[ny][nx]
                    if target is None or target.color != self.color:
                        valid_moves.append([dx, dy])
        return valid_moves


class Queen:
    def __init__(self, color):
        self.color = color
        self.type = "queen"

    def GetValidMoves(self, x, y, board):
        valid_moves = []
        for i in range(1, 8):
            for dx, dy in [
                [i, 0],
                [-i, 0],
                [0, i],
                [0, -i],
                [i, i],
                [-i, -i],
                [i, -i],
                [-i, i],
            ]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8 and IsPathClear(x, y, dx, dy):
                    target = board[ny][nx]
                    if target is None or target.color != self.color:
                        valid_moves.append([dx, dy])
        return valid_moves


class King:
    def __init__(self, color):
        self.color = color
        self.type = "king"
        self.has_moved = False

    def GetValidMoves(self, x, y, board):
        moves = [
            [0, 1],
            [1, 0],
            [0, -1],
            [-1, 0],
            [1, 1],
            [1, -1],
            [-1, 1],
            [-1, -1],
        ]
        valid_moves = []

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[ny][nx]
                if target is None or target.color != self.color:
                    valid_moves.append([dx, dy])

        if not self.has_moved:
            row = 7 if self.color == "white" else 0

            if (
                isinstance(board[row][7], Rook)
                and board[row][7].color == self.color
                and not board[row][7].has_moved
                and IsPathClear(x, row, 3, 0)
            ):
                valid_moves.append([2, 0])

            if (
                isinstance(board[row][0], Rook)
                and board[row][0].color == self.color
                and not board[row][0].has_moved
                and IsPathClear(x, row, -4, 0)
            ):
                valid_moves.append([-2, 0])

        return valid_moves


def main():
    global selected_piece, board, piece_images, piece_turtles, cur_turn
    selected_piece = None

    def setupWin():
        global window
        window = turtle.Screen()
        window.setup(WINX, WINY)
        window.bgcolor("white")

    setupWin()

    piece_names = ["pawn", "knight", "bishop", "rook", "queen", "king"]
    colors = ["white", "black"]
    for color in colors:
        for name in piece_names:
            filename = f"pieces/{color}-{name}.gif"
            turtle.register_shape(filename)
            piece_images[(name, color)] = filename

    BoardTurt = turtle.Turtle()
    PieceTurt = turtle.Turtle()
    turtle.setworldcoordinates(0, 8, 10, 0)

    board = []

    def CreateBoard():
        board.clear()
        BoardTurt.ht()
        PieceTurt.ht()
        PieceTurt.penup()
        PieceTurt.pensize(10)
        BoardTurt.pensize(5)

        for y in range(8):
            board.append([None for _ in range(8)])

        board[1] = [Pawn("black") for _ in range(8)]
        board[6] = [Pawn("white") for _ in range(8)]
        board[0] = [
            Rook("black"),
            Knight("black"),
            Bishop("black"),
            Queen("black"),
            King("black"),
            Bishop("black"),
            Knight("black"),
            Rook("black"),
        ]
        board[7] = [
            Rook("white"),
            Knight("white"),
            Bishop("white"),
            Queen("white"),
            King("white"),
            Bishop("white"),
            Knight("white"),
            Rook("white"),
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

    def UpdateBoard():
        PieceTurt.clear()
        for t in piece_turtles:
            t.hideturtle()
            t.clear()
        piece_turtles.clear()

        for y in range(8):
            for x in range(8):
                piece = board[y][x]
                if piece:
                    img = piece_images.get((piece.type, piece.color))
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
                for dx, dy in piece.GetValidMoves(x0, y0, board):
                    PieceTurt.goto(x0 + dx + 0.1, y0 + dy + 0.1)
                    PieceTurt.pendown()
                    for _ in range(4):
                        PieceTurt.forward(0.8)
                        PieceTurt.right(-90)
                    PieceTurt.penup()
            PieceTurt.pencolor("black")

        PieceTurt.goto(0, 0)

        for x in range(8):
            if board[7][x] is not None:
                if board[7][x].type == 'pawn' and board[7][x].color == 'white':
                    board[7][x] = Queen('white')
        
        for x in range(8):
            if board[0][x] is not None:
                if board[0][x].type == 'pawn' and board[0][x].color == 'black':
                    board[0][x] = Queen('black')

        PieceTurt.penup()
        PieceTurt.goto(9,1)
        PieceTurt.write(cur_turn.capitalize()+"'s",align='center',font=('Arial',60,'normal'))
        PieceTurt.goto(9,1.6)
        PieceTurt.write("Turn",align='center',font=('Arial',60,'normal'))



        turtle.update()
        turtle.ontimer(UpdateBoard, 100)

    def ScreenClicked(x, y):
        global selected_piece, cur_turn
        x = int(math.floor(x))
        y = int(math.floor(y))

        if not (0 <= x < 8 and 0 <= y < 8):
            return

        if selected_piece is None:
            if board[y][x] is not None and board[y][x].color == cur_turn:
                selected_piece = [x, y]
        else:
            x0, y0 = selected_piece
            piece = board[y0][x0]
            if piece:
                valid_moves = piece.GetValidMoves(x0, y0, board)
                move = [x - x0, y - y0]

                if move in valid_moves:
                    if isinstance(piece, King):
                        if move == [2, 0]:
                            board[y][x - 1] = board[y][7]
                            board[y][7] = None
                        elif move == [-2, 0]:
                            board[y][x + 1] = board[y][0]
                            board[y][0] = None
                        piece.has_moved = True

                    if isinstance(piece, Rook):
                        piece.has_moved = True

                    board[y][x] = piece
                    board[y0][x0] = None
                    selected_piece = None
                    cur_turn = "black" if cur_turn == "white" else "white"
                else:
                    selected_piece = None

    turtle.onscreenclick(ScreenClicked)
    UpdateBoard()
    window.mainloop()


main()
