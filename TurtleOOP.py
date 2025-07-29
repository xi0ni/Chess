import turtle
import math

window = None
WINX, WINY = 960, 960
turtle.tracer(False)  # Disable animation for faster drawing

piece_images = {}
piece_turtles = []
cur_turn = 'white'

def IsPathClear(x0, y0, dx, dy):

    if  x0 + dx < 0 or x0 + dx >= 8 or y0 + dy < 0 or y0 + dy >= 8:
        return False
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return True
    step_x = dx // steps if dx != 0 else 0
    step_y = dy // steps if dy != 0 else 0
    for step in range(1, steps):
        nx = x0 + step_x * step
        ny = y0 + step_y * step
        if board[ny][nx] != None:
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

        # Forward 1
        if 0 <= y + direction < 8 and board[y + direction][x] is None:
            moves.append([0, direction])

            # Forward 2 from start row if clear
            if y == self.start_row and y + 2 * direction <= 8 and y+ 2 * direction >= 0:
                if board[y + 2 * direction][x] is None:
                    moves.append([0, 2*direction])

        # Diagonal captures
        for dx in [-1, 1]:
            nx, ny = x + dx, y + direction
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[ny][nx]
                if target != None:
                    if target.color != self.color:
                        moves.append([dx, 1*direction])
        return moves

class Knight:
    def __init__(self, color):
        self.color = color
        self.type = "knight"

    def GetValidMoves(self, x, y, board):
        moves = [
            [1, 2], [2, 1], [-1, 2], [-2, 1],
            [1, -2], [2, -1], [-1, -2], [-2, -1],
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
        moves = []
        for i in range(1, 8):
            moves.extend([[i, i], [-i, -i], [i, -i], [-i, i]])

        valid_moves = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if IsPathClear(x, y, dx, dy):
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
        moves = []
        for i in range(1, 8):
            moves.extend([[i, 0], [-i, 0], [0, i], [0, -i]])
        valid_moves = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if IsPathClear(x, y, dx, dy):
                    target = board[ny][nx]
                    if target is None or target.color != self.color:
                        valid_moves.append([dx, dy])
        return valid_moves
    
class Queen:
    def __init__(self, color):
        self.color = color
        self.type = "queen"

    def GetValidMoves(self, x, y, board):
        moves = []
        for i in range(1, 8):
            moves.extend([[i, 0], [-i, 0], [0, i], [0, -i]])
            moves.extend([[i, i], [-i, -i], [i, -i], [-i, i]])

        valid_moves = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if IsPathClear(x, y, dx, dy):
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
            [0, 1], [1, 0], [0, -1], [-1, 0],
            [1, 1], [1, -1], [-1, 1], [-1, -1],
        ]
        valid_moves = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if IsPathClear(x, y, dx, dy):
                    target = board[ny][nx]
                    if target is None or target.color != self.color:
                        valid_moves.append([dx, dy])

        # Castling
        if not self.has_moved:

            y = 0 if self.color == "white" else 7

            if board[y][0] == Rook:
                if board[y][0].has_moved == False and self.has_moved == False and board[y][0].color == self.color:
                    if IsPathClear(x, y, 2, 0):
                        valid_moves.append([2, 0])
            if board[y][7] == Rook:
                if board[y][7].has_moved == False and self.has_moved == False and board[y][0].color == self.color:
                    if IsPathClear(x, y, -2, 0):
                        valid_moves.append([-2, 0])

        return valid_moves
    
    


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
        board.clear()  # <-- Add this line!
        BoardTurt.ht()
        PieceTurt.ht()
        PieceTurt.penup()
        PieceTurt.pensize(10)
        BoardTurt.pensize(5)

        for y in range(8):
            y_list = []
            for x in range(8):
                y_list.append(None)
            board.append(y_list)

        board[1] = [Pawn('black') for i in range(8)]
        board[-2] = [Pawn('white') for i in range(8)]

        board[0] = [
            Rook('black'),
            Knight('black'),
            Bishop('black'),
            Queen('black'),
            King('black'),
            Bishop('black'),
            Knight('black'),
            Rook('black'),
        ]
        board[-1] = [
            Rook('white'),
            Knight('white'),
            Bishop('white'),
            Queen('white'),
            King('white'),
            Bishop('white'),
            Knight('white'),
            Rook('white'),
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
            if piece != None:

                for move in piece.GetValidMoves(x0, y0, board):
                        # Draw red square for valid move
                        PieceTurt.goto(x0 + move[0]+0.1, y0 + move[1]+0.1)
                        PieceTurt.pendown()
                        for i in range(4):
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
            if board[y][x] != None:
                selected_piece = [x, y]
        else:
            x0, y0 = selected_piece
            piece = board[y0][x0]
            if piece:
                valid_moves = piece.GetValidMoves(x0, y0, board)
                if [x - x0, y - y0] in valid_moves:
                    # Move the piece
                    board[y][x] = piece
                    board[y0][x0] = None
                    selected_piece = None
                    UpdateBoard()
                    global cur_turn
                    cur_turn = 'black' if cur_turn == 'white' else 'white'
                else:
                    selected_piece = None

            selected_piece = None
            

    turtle.onscreenclick(ScreenClicked)
    UpdateBoard()
    window.mainloop()


main()
