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

    # goes through every square in that direction to the final square and checks if a piece is in that square
    for step in range(1, steps):
        nx = x0 + step_x * step
        ny = y0 + step_y * step

        # if a piece is in the way at any time it returns false
        if board[ny][nx] is not None:
            return False
        
    # otherwise it returns true
    return True

# defines the pawn class
class Pawn:
    def __init__(self, color):

        # stores the pawns color, the fact that it is a pawn, and what row it starts on
        self.color = color
        self.type = "pawn"
        self.start_row = 6 if color == "white" else 1

    # defines a function to get all of the valid moves that the piece can make
    def GetValidMoves(self, x, y, board):

        # creates a list to store the valid moves
        moves = []

        # sets the direction for the pawns because they can only move forward
        direction = -1 if self.color == "white" else 1

        # if moving forward isnt off the board and no piece is obstructing that space
        if 0 <= y + direction < 8 and board[y + direction][x] is None:
            # moving forward is a valid move
            moves.append([0, direction])
            
            # if we are at the starting row, and no piece is blocking the way
            if y == self.start_row and board[y + 2 * direction][x] is None:
                # we can move 2
                moves.append([0, 2 * direction])

        # this checks the diagonals to see if a piece is there 
        for dx in [-1, 1]:
            
            # creates the coordinates to store the diagonals
            nx, ny = x + dx, y + direction

            # if the diagonals are not off of the board
            if 0 <= nx < 8 and 0 <= ny < 8:

                # stores what the target would be for those diagonals
                target = board[ny][nx]

                # if there is a piece there than the pawn can take diagonally
                if target is not None and target.color != self.color:
                    moves.append([dx, direction])
        
        # return the list of valid moves
        return moves

# defines the knight class
class Knight:

    # store the knights color and the fact is it s knight
    def __init__(self, color):
        self.color = color
        self.type = "knight"

    # defines a function to return a list of all of the legal moves the knight can make
    def GetValidMoves(self, x, y, board):

        # a list of all of the theoretical moves the knight could make
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

        # stores the list of valid moves after modifications
        valid_moves = []

        # itterates through the possible moves
        for dx, dy in moves:

            # stores the target square
            nx, ny = x + dx, y + dy

            # checks if the target square is in the board
            if 0 <= nx < 8 and 0 <= ny < 8:
                # we store what is in the target square
                target = board[ny][nx]
                # if the square is empty or it is a piece of another color
                if target is None or target.color != self.color:
                    # it is a valid move
                    valid_moves.append([dx, dy])

        # returns the list of valid moves
        return valid_moves

# defines the bishop class
class Bishop:

    # stores the bishops color and the fact that it is a bishop
    def __init__(self, color):
        self.color = color
        self.type = "bishop"

    # defines a function to get all of the valid moves the bishop can make
    def GetValidMoves(self, x, y, board):

        # creates a list to store the valid moves
        valid_moves = []

        # itterates 7 times for the theoretical diagonal 7 squares in each direction
        for i in range(1, 8):

            # itterates through the possible diagonal squares the bishop could move
            for dx, dy in [[i, i], [-i, -i], [i, -i], [-i, i]]:

                # stores the target coordinates
                nx, ny = x + dx, y + dy

                # checks if the target is inside the board and if the path is clear
                if 0 <= nx < 8 and 0 <= ny < 8 and IsPathClear(x, y, dx, dy):

                    # stores what is in the board at the target coords
                    target = board[ny][nx]

                    # if the square is empty or has a piece of another color in it
                    if target is None or target.color != self.color:
                        # it is a valid move and is added to the list
                        valid_moves.append([dx, dy])
        
        # returns the list of valid moves
        return valid_moves

# defines the rook class
class Rook:

    # stores the rooks color, the fact that it is a rook, and whether it has moved or not for castling
    def __init__(self, color):
        self.color = color
        self.type = "rook"
        self.has_moved = False

    # defines a function to get all of the valid moves the rook can make
    def GetValidMoves(self, x, y, board):

        # creates a list to store the valid moves
        valid_moves = []

        # itterates 7 time for each of the 7 tiles in each direction that the rook could move
        for i in range(1, 8):

            # itterates through all 4 possible directions
            for dx, dy in [[i, 0], [-i, 0], [0, i], [0, -i]]:

                # stores the target coords
                nx, ny = x + dx, y + dy

                # if it is on the board and the path is clear
                if 0 <= nx < 8 and 0 <= ny < 8 and IsPathClear(x, y, dx, dy):

                    # we store what is in the board at the target coords
                    target = board[ny][nx]

                    # if the thing on the board at the target coords is nothing or is a piece of another color
                    if target is None or target.color != self.color:

                        # it is a valid move and we add it to the list of valid moves
                        valid_moves.append([dx, dy])
        
        # returns the list of valid moves
        return valid_moves

# defines the queen class
class Queen:

    # stores the queens color, and the fact that it is a queen
    def __init__(self, color):
        self.color = color
        self.type = "queen"

    # defines a function to get all of the valid moves the piece could make
    def GetValidMoves(self, x, y, board):

        # creates a list to store the valid moves
        valid_moves = []

        # itterates 7 times for the 7 squares that the queen could theoretically travel
        for i in range(1, 8):

            # itterates through each of the possible squares the queen could go to that is the given distance away
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
                
                # stores the target coords
                nx, ny = x + dx, y + dy

                # if it is inside the board and the path is clear
                if 0 <= nx < 8 and 0 <= ny < 8 and IsPathClear(x, y, dx, dy):

                    # store the object that is on the board at the target coords
                    target = board[ny][nx]

                    # if nothing is in the target coords or it is a piece of a different color
                    if target is None or target.color != self.color:

                        # it is a valid move and add it to the list of valid moves
                        valid_moves.append([dx, dy])

        # returns the list of valid moves
        return valid_moves

# defines the king class
class King:

    # stores the color of the king, the fact that it is a king, and whether it has moved or not
    def __init__(self, color):
        self.color = color
        self.type = "king"
        self.has_moved = False

    # defines a function to get the valid moves of the piece
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

        # creates a new list to add all of the valid moves too
        valid_moves = []

        # itterates through the theoretical moves
        for dx, dy in moves:

            # stores the target coords
            nx, ny = x + dx, y + dy

            # if the target coord is on the board
            if 0 <= nx < 8 and 0 <= ny < 8:

                # store what is in the board at the target coords
                target = board[ny][nx]

                # if the square is empty or has a piece of another color in it
                if target is None or target.color != self.color:

                    # it is a valid move and add it to the list of valid moves
                    valid_moves.append([dx, dy])


        # this is to check if you can castle

        # if the king has not moved
        if not self.has_moved:

            # sets which row we are checking depending on the color of the king
            row = 7 if self.color == "white" else 0

            if (

                # checks if the object on the right of the board is a rook
                isinstance(board[row][7], Rook)
                # with the same color as the king
                and board[row][7].color == self.color
                # that has not moved
                and not board[row][7].has_moved
                # and the path is clear
                and IsPathClear(x, row, 3, 0)
            ):
                # castling is a valid move
                valid_moves.append([2, 0])

            if (
                 # checks if the object on the left of the board is a rook
                isinstance(board[row][0], Rook)
                # with the same color as the king
                and board[row][0].color == self.color
                # that has not moved
                and not board[row][0].has_moved
                # and the path is clear
                and IsPathClear(x, row, -4, 0)
            ):
                # castling is a valid move
                valid_moves.append([-2, 0])

        # returns the list of valid moves
        return valid_moves


# the main funciton that loops
def main():
    # sets up some global variables
    global selected_piece, board, piece_images, piece_turtles, cur_turn
    # creates a variable to stores the current piece that is picked up
    selected_piece = None

    # a function that sets up the window for turtle
    def setupWin():
        global window
        window = turtle.Screen()
        window.setup(WINX, WINY)
        window.bgcolor("white")
    # calls the function to set up the window
    setupWin()

    # creates a list of the piece names
    piece_names = ["pawn", "knight", "bishop", "rook", "queen", "king"]
    # creates a list of the colors
    colors = ["white", "black"]

    # for every color in the list of colors
    for color in colors:
        # for every piece in the list of pieces
        for name in piece_names:

            # creates a variable the stores the image of the piece with that color
            filename = f"pieces/{color}-{name}.gif"
            # registers thay file with turtle
            turtle.register_shape(filename)
            # adds it to the list of piece images
            piece_images[(name, color)] = filename

    # creates the 2 turtles that we use and sets up the world coordinates
    BoardTurt = turtle.Turtle()
    PieceTurt = turtle.Turtle()
    turtle.setworldcoordinates(0, 8, 10, 0)

    # creates the variable that stores the board
    board = []

    # defines a function to create the board data structure
    def CreateBoard():

        # empties the board
        board.clear()

        # initializes the turtles
        BoardTurt.ht()
        PieceTurt.ht()
        PieceTurt.penup()
        PieceTurt.pensize(10)
        BoardTurt.pensize(5)

        # creates an 8 by 8 square of nothing
        for y in range(8):
            board.append([None for _ in range(8)])

        # sets the second and second to last row to pawns
        board[1] = [Pawn("black") for _ in range(8)]
        board[-2] = [Pawn("white") for _ in range(8)]

        # sets the first row and last row to the correct pieces
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
        board[-1] = [
            Rook("white"),
            Knight("white"),
            Bishop("white"),
            Queen("white"),
            King("white"),
            Bishop("white"),
            Knight("white"),
            Rook("white"),
        ]

    # calls the function
    CreateBoard()

    # defines a function to draw the board
    def DrawBoard():

        # repeats for all of the rows
        for y in range(8):

            # goes across and draws the squares with a checkered pattern
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

    # calls the function
    DrawBoard()
    # updates the screen
    turtle.update()


    # defines a function that runs periodically to update the board
    def UpdateBoard():

        # clears the piece turtle
        PieceTurt.clear()


        for t in piece_turtles:
            t.hideturtle()
            t.clear()
        piece_turtles.clear()
        
        # itterates through every square in the board
        for y in range(8):
            for x in range(8):
                piece = board[y][x]

                # if there is a piece in that square
                if piece:

                    # gets the image
                    img = piece_images.get((piece.type, piece.color))
                    if img:
                        # the turtle goes to where it should be and unhides itself
                        t = turtle.Turtle()
                        t.penup()
                        t.shape(img)
                        t.goto(x + 0.5, y + 0.5)
                        t.turtlesize(1)
                        t.showturtle()
                        piece_turtles.append(t)

        # if a piece is selected
        if selected_piece is not None:

            # we highlight the pieces place on the board in green
            PieceTurt.pencolor("green")
            PieceTurt.penup()
            PieceTurt.goto(selected_piece[0] + 0.1, selected_piece[1] + 0.1)
            PieceTurt.pendown()
            for i in range(4):
                PieceTurt.forward(0.8)
                PieceTurt.right(-90)
            PieceTurt.penup()

            # then we highlight every square that the piece could move to in red
            PieceTurt.pencolor("red")

            # stores where the selected piece is 
            x0, y0 = selected_piece
            # stores what the selected piece is 
            piece = board[y0][x0]

            # if it is a piece
            if piece:

                # we iterate through all of the valid moves that the piece could make
                for dx, dy in piece.GetValidMoves(x0, y0, board):

                    # we go to them 
                    PieceTurt.goto(x0 + dx + 0.1, y0 + dy + 0.1)
                    PieceTurt.pendown()

                    # and highlight them in red
                    for i in range(4):
                        PieceTurt.forward(0.8)
                        PieceTurt.right(-90)
                    PieceTurt.penup()
            
            # then we set the pencolor back to black for writing the turn
            PieceTurt.pencolor("black")


        # some nonfunctional code for promoting
        for x in range(8):
            if board[7][x] is not None:
                if board[7][x].type == 'pawn' and board[7][x].color == 'white':
                    board[7][x] = Queen('white')
        
        for x in range(8):
            if board[0][x] is not None:
                if board[0][x].type == 'pawn' and board[0][x].color == 'black':
                    board[0][x] = Queen('black')

        # this bit of code writes whos turn it is in the top right hand corner
        PieceTurt.penup()
        PieceTurt.goto(9,1)
        PieceTurt.write(cur_turn.capitalize()+"'s",align='center',font=('Arial',60,'normal'))
        PieceTurt.goto(9,1.6)
        PieceTurt.write("Turn",align='center',font=('Arial',60,'normal'))


        # we update the screen
        turtle.update()
        # and we call ourselves again so functionally we update the screen 10 times every second
        turtle.ontimer(UpdateBoard, 100)

    # defines the screen clicked function
    def ScreenClicked(x, y):
        global selected_piece, cur_turn

        # takes the floor of the passed values which converts it into the coordinates on our board
        x = int(math.floor(x))
        y = int(math.floor(y))

        # if the place clicked is outside the board
        if not (0 <= x < 8 and 0 <= y < 8):

            # we do nothing and end the function
            return
        
        # if we currently have no piece selected
        if selected_piece is None:
            # and there is a piece in the place that we click, and it is that colors turn
            if board[y][x] is not None and board[y][x].color == cur_turn:

                # we set that piece as our selected piece
                selected_piece = [x, y]

        # otherwise
        else:

            # we store the coordinates of our currently selected piece
            x0, y0 = selected_piece
            # and we store the piece itself
            piece = board[y0][x0]

            # if it is a piece 
            if piece:

                # we store the list of all of the valid moves it could make
                valid_moves = piece.GetValidMoves(x0, y0, board)

                # we store what the move the user is trying to make currently
                move = [x - x0, y - y0]

                # if the move is one of the valid moves that the piece can make
                if move in valid_moves:

                    # if it is a king
                    if isinstance(piece, King):
                        # if castling, move the rook
                        if move == [2, 0]:
                            board[y][x - 1] = board[y][7]
                            board[y][7] = None
                        elif move == [-2, 0]:
                            board[y][x + 1] = board[y][0]
                            board[y][0] = None
                        piece.has_moved = True

                    # if the piece is a rook we store that it has moved so we can't castle with it
                    if isinstance(piece, Rook):
                        piece.has_moved = True

                    # sets the clicked place to the currently selected piece
                    board[y][x] = piece

                    # sets where the currently selected piece was to none
                    board[y0][x0] = None

                    # pawn promotion to queen if reaching the back rank
                    if isinstance(piece, Pawn):
                        if (piece.color == "white" and y == 0) or (piece.color == "black" and y == 7):
                            board[y][x] = Queen(piece.color)

                    # sets the selected piece to none
                    selected_piece = None

                    # switches which players turn it is
                    cur_turn = "black" if cur_turn == "white" else "white"


                # if the move is not a valid move we just unselect the currently selected piece
                else:
                    selected_piece = None

    # when the screen is clicked we run the on screen clicked function
    turtle.onscreenclick(ScreenClicked)
    # calls update board for the first time
    UpdateBoard()

    # tells this window to stay open and loop
    window.mainloop()


# calls main
main()
