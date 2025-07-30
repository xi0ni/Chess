import turtle
import math

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

# Global variable to track board orientation
# 'white' means White's pieces are at the bottom (rows 7, 6), 'black' means Black's pieces are at the bottom (rows 0, 1)
view_orientation = "white"


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

            # Kingside Castling
            if (
                isinstance(board[row][7], Rook)
                and board[row][7].color == self.color
                and not board[row][7].has_moved
                and IsPathClear(x, row, 3, 0)
            ):
                # Ensure squares king moves through/to are not attacked (simplified here, but important for full implementation)
                # For basic functionality, this IsPathClear is sufficient.
                valid_moves.append([2, 0])

            # Queenside Castling
            if (
                isinstance(board[row][0], Rook)
                and board[row][0].color == self.color
                and not board[row][0].has_moved
                and IsPathClear(x, row, -4, 0)
            ):
                # Ensure squares king moves through/to are not attacked
                valid_moves.append([-2, 0])

        # returns the list of valid moves
        return valid_moves


# Defines a standalone function to find the king's position
def find_king(board, color):
    for row_idx, row in enumerate(board):
        for col_idx, piece in enumerate(row):
            if (
                piece is not None
                and isinstance(piece, King)  # Use isinstance for type checking
                and piece.color == color
            ):
                return (col_idx, row_idx)
    return None  # King not found


# Defines a standalone function to check if a king of a given color is in check
def is_king_in_check(board_state, color_to_check):
    king_pos = find_king(board_state, color_to_check)
    if king_pos is None:
        # This means the king is not on the board for some reason, which should not happen.
        # This could indicate a king was captured in an invalid way.
        return False

    kx, ky = king_pos
    # Iterate through all pieces on the board
    for y, row in enumerate(board_state):
        for x, piece in enumerate(row):
            # If the piece belongs to the opponent
            if piece is not None and piece.color != color_to_check:
                potential_moves = piece.GetValidMoves(x, y, board_state)
                for dx, dy in potential_moves:
                    # If this potential move lands on the king's square
                    if x + dx == kx and y + dy == ky:
                        return True  # King is under attack
    return False  # King is not in check


# Function to check if there are any legal moves for the current player
def has_legal_moves(current_board, color_to_check):
    for y_orig in range(8):
        for x_orig in range(8):
            piece = current_board[y_orig][x_orig]
            if piece is not None and piece.color == color_to_check:
                possible_moves = piece.GetValidMoves(x_orig, y_orig, current_board)
                for dx, dy in possible_moves:
                    x_dest, y_dest = x_orig + dx, y_orig + dy

                    # --- Simulate the move ---
                    # Create a deep copy of the board to simulate the move without affecting the actual game board
                    temp_board = [
                        row[:] for row in current_board
                    ]  # Simple copy for 2D list of immutables/references

                    # Store original states for potential rollback
                    original_piece_at_target = temp_board[y_dest][x_dest]
                    original_piece_has_moved = None
                    if isinstance(piece, (King, Rook)):
                        original_piece_has_moved = (
                            piece.has_moved
                        )  # Capture the state of *this specific piece instance*

                    original_rook_at_castling_pos = None
                    original_rook_has_moved_state = None

                    # Perform the move on the temporary board
                    temp_board[y_dest][x_dest] = temp_board[y_orig][x_orig]
                    temp_board[y_orig][x_orig] = None

                    # Handle castling specific move (rook movement) on temp_board
                    if isinstance(temp_board[y_dest][x_dest], King):
                        if [dx, dy] == [2, 0]:  # Kingside castle
                            original_rook_at_castling_pos = temp_board[y_orig][7]
                            original_rook_has_moved_state = (
                                original_rook_at_castling_pos.has_moved
                                if isinstance(original_rook_at_castling_pos, Rook)
                                else None
                            )
                            temp_board[y_orig][x_orig + 1] = temp_board[y_orig][7]
                            temp_board[y_orig][7] = None
                            if isinstance(temp_board[y_orig][x_orig + 1], Rook):
                                temp_board[y_orig][x_orig + 1].has_moved = True
                        elif [dx, dy] == [-2, 0]:  # Queenside castle
                            original_rook_at_castling_pos = temp_board[y_orig][0]
                            original_rook_has_moved_state = (
                                original_rook_at_castling_pos.has_moved
                                if isinstance(original_rook_at_castling_pos, Rook)
                                else None
                            )
                            temp_board[y_orig][x_orig - 1] = temp_board[y_orig][0]
                            temp_board[y_orig][0] = None
                            if isinstance(temp_board[y_orig][x_orig - 1], Rook):
                                temp_board[y_orig][x_orig - 1].has_moved = True
                        # For simulation, don't change has_moved on original piece directly

                    # Temporarily update has_moved for the simulated piece if it's a King or Rook
                    simulated_piece = temp_board[y_dest][x_dest]
                    if isinstance(simulated_piece, (King, Rook)):
                        simulated_piece.has_moved = (
                            True  # Assume it moved for this check
                        )

                    # Check if the king is still in check after this move
                    if not is_king_in_check(temp_board, color_to_check):
                        return True  # Found at least one legal move

                    # --- Rollback the simulated move ---
                    # Restore piece position
                    temp_board[y_orig][x_orig] = temp_board[y_dest][x_dest]
                    temp_board[y_dest][x_dest] = original_piece_at_target

                    # Restore has_moved state for original piece
                    if (
                        isinstance(temp_board[y_orig][x_orig], (King, Rook))
                        and original_piece_has_moved is not None
                    ):
                        temp_board[y_orig][x_orig].has_moved = original_piece_has_moved

                    # Rollback castling rook movement
                    if isinstance(temp_board[y_orig][x_orig], King):
                        if [dx, dy] == [2, 0]:
                            temp_board[y_orig][7] = original_rook_at_castling_pos
                            temp_board[y_orig][x_orig + 1] = None
                            if (
                                isinstance(temp_board[y_orig][7], Rook)
                                and original_rook_has_moved_state is not None
                            ):
                                temp_board[y_orig][
                                    7
                                ].has_moved = original_rook_has_moved_state
                        elif [dx, dy] == [-2, 0]:
                            temp_board[y_orig][0] = original_rook_at_castling_pos
                            temp_board[y_orig][x_orig - 1] = None
                            if (
                                isinstance(temp_board[y_orig][0], Rook)
                                and original_rook_has_moved_state is not None
                            ):
                                temp_board[y_orig][
                                    0
                                ].has_moved = original_rook_has_moved_state
    return False  # No legal moves found


# the main funciton that loops
def main():
    # sets up some global variables
    global \
        selected_piece, \
        board, \
        piece_images, \
        piece_turtles, \
        cur_turn, \
        view_orientation
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
        BoardTurt.clear()
        # repeats for all of the rows
        for y in range(8):
            # goes across and draws the squares with a checkered pattern
            for x in range(8):
                BoardTurt.penup()
                # Adjust drawing coordinates based on view_orientation
                display_x = x
                display_y = y if view_orientation == "white" else 7 - y

                BoardTurt.goto(display_x, display_y)
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

                        # Adjust piece display coordinates based on view_orientation
                        display_x = x + 0.5
                        display_y = (
                            y + 0.5 if view_orientation == "white" else (7 - y) + 0.5
                        )

                        t.goto(display_x, display_y)
                        t.turtlesize(1)
                        t.showturtle()
                        piece_turtles.append(t)

        # if a piece is selected
        if selected_piece is not None:
            # we highlight the pieces place on the board in green
            PieceTurt.pencolor("green")
            # Adjust drawing coordinates for selected piece based on view_orientation
            display_x0 = selected_piece[0] + 0.1
            display_y0 = (
                (selected_piece[1] + 0.1)
                if view_orientation == "white"
                else (7 - selected_piece[1]) + 0.1
            )

            PieceTurt.penup()
            PieceTurt.goto(display_x0, display_y0)
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
                    # Adjust display coordinates for valid moves based on view_orientation
                    display_nx = x0 + dx + 0.1
                    display_ny = (
                        (y0 + dy + 0.1)
                        if view_orientation == "white"
                        else (7 - (y0 + dy)) + 0.1
                    )

                    # we go to them
                    PieceTurt.goto(display_nx, display_ny)
                    PieceTurt.pendown()

                    # and highlight them in red
                    for i in range(4):
                        PieceTurt.forward(0.8)
                        PieceTurt.right(-90)
                    PieceTurt.penup()

            # then we set the pencolor back to black for writing the turn
            PieceTurt.pencolor("black")

        # However, if you promote multiple pawns in one go for some reason, this might be okay.
        # But generally, promotion should happen immediately upon a pawn reaching the back rank.
        for x in range(8):
            if board[7][x] is not None:
                if board[7][x].type == "pawn" and board[7][x].color == "white":
                    board[7][x] = Queen("white")

        for x in range(8):
            if board[0][x] is not None:
                if board[0][x].type == "pawn" and board[0][x].color == "black":
                    board[0][x] = Queen("black")

        # Display turn
        PieceTurt.penup()
        PieceTurt.goto(9, 1)
        PieceTurt.write(
            cur_turn.capitalize() + "'s", align="center", font=("Arial", 60, "normal")
        )
        PieceTurt.goto(9, 1.6)
        PieceTurt.write("Turn", align="center", font=("Arial", 60, "normal"))

        # Check for game end conditions
        if is_king_in_check(board, cur_turn):
            if not has_legal_moves(board, cur_turn):
                PieceTurt.penup()
                PieceTurt.goto(9, 3)
                PieceTurt.write(
                    "CHECKMATE!", align="center", font=("Arial", 25, "bold")
                )

            else:
                PieceTurt.penup()
                PieceTurt.goto(9, 3)
                PieceTurt.write("CHECK!", align="center", font=("Arial", 40, "bold"))
        elif not has_legal_moves(board, cur_turn):
            PieceTurt.penup()
            PieceTurt.goto(9, 3)
            PieceTurt.write("STALEMATE!", align="center", font=("Arial", 40, "bold"))
        

        # we update the screen
        turtle.update()
        # and we call ourselves again so functionally we update the screen 10 times every second
        turtle.ontimer(UpdateBoard, 100)

    # defines the screen clicked function
    def ScreenClicked(x, y):
        global selected_piece, cur_turn, board, view_orientation  # Ensure board is global if modified here

        # Prevent clicks if the game is over (checkmate or stalemate)
        if (
            is_king_in_check(board, cur_turn) and not has_legal_moves(board, cur_turn)
        ) or (
            not is_king_in_check(board, cur_turn)
            and not has_legal_moves(board, cur_turn)
        ):
            return  # Do nothing if game is over

        # Convert screen coordinates to board coordinates based on current view_orientation
        board_x = int(math.floor(x))
        board_y = int(math.floor(y))

        if view_orientation == "black":
            board_y = 7 - board_y  # Invert y-coordinate for black's view

        # if the place clicked is outside the board
        if not (0 <= board_x < 8 and 0 <= board_y < 8):
            # we do nothing and end the function
            selected_piece = None  # Deselect if clicked outside the board
            return

        # if we currently have no piece selected
        if selected_piece is None:
            # and there is a piece in the place that we click, and it is that colors turn
            if (
                board[board_y][board_x] is not None
                and board[board_y][board_x].color == cur_turn
            ):
                # we set that piece as our selected piece
                selected_piece = [board_x, board_y]

        # otherwise (a piece is already selected)
        else:
            # we store the coordinates of our currently selected piece
            x0, y0 = selected_piece
            # and we store the piece itself
            piece = board[y0][x0]

            # if it is a piece (should always be if selected_piece is not None)
            if piece:
                # we store the list of all of the valid moves it could make
                valid_moves = piece.GetValidMoves(x0, y0, board)

                # we store what the move the user is trying to make currently
                move = [board_x - x0, board_y - y0]

                # if the move is one of the valid moves that the piece can make
                if move in valid_moves:
                    temp_board = [row[:] for row in board]

                    original_piece_at_target = temp_board[board_y][board_x]
                    original_piece_has_moved = (
                        piece.has_moved if isinstance(piece, (King, Rook)) else None
                    )
                    original_rook_at_castling_pos = None
                    original_rook_has_moved_state = None

                    # Perform the move on the temporary board
                    temp_board[board_y][board_x] = temp_board[y0][x0]
                    temp_board[y0][x0] = None

                    # Temporarily update has_moved for the simulated piece if it's a King or Rook
                    simulated_piece_on_temp_board = temp_board[board_y][board_x]
                    if isinstance(simulated_piece_on_temp_board, (King, Rook)):
                        simulated_piece_on_temp_board.has_moved = (
                            True  # Mark as moved for this check
                        )

                    # Handle castling specific move (rook movement) on temp_board
                    if isinstance(simulated_piece_on_temp_board, King):
                        if move == [2, 0]:  # Kingside castle
                            original_rook_at_castling_pos = temp_board[y0][7]
                            original_rook_has_moved_state = (
                                original_rook_at_castling_pos.has_moved
                                if isinstance(original_rook_at_castling_pos, Rook)
                                else None
                            )
                            temp_board[y0][x0 + 1] = temp_board[y0][7]
                            temp_board[y0][7] = None
                            if isinstance(temp_board[y0][x0 + 1], Rook):
                                temp_board[y0][x0 + 1].has_moved = True
                        elif move == [-2, 0]:  # Queenside castle
                            original_rook_at_castling_pos = temp_board[y0][0]
                            original_rook_has_moved_state = (
                                original_rook_at_castling_pos.has_moved
                                if isinstance(original_rook_at_castling_pos, Rook)
                                else None
                            )
                            temp_board[y0][x0 - 1] = temp_board[y0][0]
                            temp_board[y0][0] = None
                            if isinstance(temp_board[y0][x0 - 1], Rook):
                                temp_board[y0][x0 - 1].has_moved = True

                    # Check if this simulated move puts the current player's king in check
                    if is_king_in_check(temp_board, cur_turn):
                        print("That move puts your king in check! Try again.")
                        selected_piece = None  # Deselect the piece
                    else:
                        # If the move is legal (doesn't put own king in check)
                        # Apply the move to the actual game board
                        board[board_y][board_x] = board[y0][x0]
                        board[y0][x0] = None

                        if isinstance(piece, Pawn):
                            if (piece.color == "white" and board_y == 0) or (
                                piece.color == "black" and board_y == 7
                            ):
                                board[board_y][board_x] = Queen(piece.color)

                        # Update has_moved property for King and Rook on the actual board
                        if isinstance(board[board_y][board_x], (King, Rook)):
                            board[board_y][board_x].has_moved = True

                        # Handle castling (actual rook movement)
                        if isinstance(piece, King):
                            if move == [2, 0]:  # Kingside castle
                                board[y0][x0 + 1] = board[y0][7]
                                board[y0][7] = None
                                if isinstance(board[y0][x0 + 1], Rook):
                                    board[y0][x0 + 1].has_moved = True
                            elif move == [-2, 0]:  # Queenside castle
                                board[y0][x0 - 1] = board[y0][0]
                                board[y0][0] = None
                                if isinstance(board[y0][x0 - 1], Rook):
                                    board[y0][x0 - 1].has_moved = True

                        selected_piece = None
                        cur_turn = "black" if cur_turn == "white" else "white"
                        view_orientation = (
                            cur_turn  # Flip the board for the next player
                        )

                        DrawBoard()  # Redraw the board after flipping orientation
                else:
                    selected_piece = None  # Deselect the piece if the move wasn't valid

    # when the screen is clicked we run the on screen clicked function
    turtle.onscreenclick(ScreenClicked)
    # calls update board for the first time
    UpdateBoard()

    # tells this window to stay open and loop
    window.mainloop()


# calls main
main()
