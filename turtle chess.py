import turtle
import math

# creates the turtle window
window = None
WINX, WINY = 1200, 960
# sets the tracer to false so the screen only updates when we want it to
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

# The game board (filled in main)
board = []

# defines a function to check if the path from a given square to another given square is clear
def IsPathClear(x0, y0, dx, dy):
    # returns false if one of the given two points is outside of the board
    if x0 + dx < 0 or x0 + dx >= 8 or y0 + dy < 0 or y0 + dy >= 8:
        return False

    # creates a steps varable that holds the max distance between the two points
    steps = max(abs(dx), abs(dy))

    # if the distance is 0 return true (same square)
    if steps == 0:
        return True

    # creates step variables for x and y which store how many squares we should move each time we check a square
    step_x = (dx // steps) if dx != 0 else 0
    step_y = (dy // steps) if dy != 0 else 0

    # goes through every square in that direction to the final square and checks if a piece is in that square
    for step in range(1, steps):
        nx = x0 + step_x * step
        ny = y0 + step_y * step

        # if a piece is in the way at any time it returns false
        if board[ny][nx] is not None:
            return False

    # otherwise it returns true
    return True


# ----------------------------
# Piece classes
# (GetValidMoves returns relative vectors [dx, dy]; GetAttackedSquares returns relative vectors too)
# ----------------------------

# defines the pawn class
class Pawn:
    def __init__(self, color):
        # stores the pawns color, the fact that it is a pawn, and what row it starts on
        self.color = color
        self.type = "pawn"
        self.start_row = 6 if color == "white" else 1
        # en-passant tracking not implemented here

    # defines a function to get all of the valid moves that the piece can make (relative vectors)
    def GetValidMoves(self, x, y, board):
        moves = []

        # sets the direction for the pawns because they can only move forward
        direction = -1 if self.color == "white" else 1

        # if moving forward isn't off the board and no piece is obstructing that space
        if 0 <= y + direction < 8 and board[y + direction][x] is None:
            # moving forward is a valid move
            moves.append([0, direction])

            # if we are at the starting row, and no piece is blocking the way
            if y == self.start_row and board[y + 2 * direction][x] is None:
                # we can move 2
                moves.append([0, 2 * direction])

        # this checks the diagonals to see if a piece is there (captures)
        for dx in [-1, 1]:
            nx, ny = x + dx, y + direction
            # if the diagonals are not off of the board
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[ny][nx]
                # if there is a piece there than the pawn can take diagonally
                if target is not None and target.color != self.color:
                    moves.append([dx, direction])

        return moves

    # returns relative vectors for squares this pawn attacks (used in check detection)
    def GetAttackedSquares(self, x, y, board):
        attacked = []
        direction = -1 if self.color == "white" else 1
        for dx in [-1, 1]:
            nx, ny = x + dx, y + direction
            if 0 <= nx < 8 and 0 <= ny < 8:
                attacked.append([dx, direction])
        return attacked


# defines the knight class
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
            # checks if the target square is on the board
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[ny][nx]
                # if the square is empty or it is a piece of another color
                if target is None or target.color != self.color:
                    valid_moves.append([dx, dy])
        return valid_moves

    def GetAttackedSquares(self, x, y, board):
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
        attacked = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                attacked.append([dx, dy])
        return attacked


# defines the bishop class
class Bishop:
    def __init__(self, color):
        self.color = color
        self.type = "bishop"

    def GetValidMoves(self, x, y, board):
        valid_moves = []
        # iterate distances in diagonal directions
        for i in range(1, 8):
            for dx, dy in [[i, i], [-i, -i], [i, -i], [-i, i]]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8 and IsPathClear(x, y, dx, dy):
                    target = board[ny][nx]
                    if target is None or target.color != self.color:
                        valid_moves.append([dx, dy])
        return valid_moves

    def GetAttackedSquares(self, x, y, board):
        attacked = []
        # For each direction, add squares until blocked (relative vectors)
        directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx_dir, dy_dir in directions:
            for i in range(1, 8):
                dx, dy = dx_dir * i, dy_dir * i
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    attacked.append([dx, dy])
                    if board[ny][nx] is not None:
                        break
        return attacked


# defines the rook class
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

    def GetAttackedSquares(self, x, y, board):
        attacked = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx_dir, dy_dir in directions:
            for i in range(1, 8):
                dx, dy = dx_dir * i, dy_dir * i
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    attacked.append([dx, dy])
                    if board[ny][nx] is not None:
                        break
        return attacked


# defines the queen class
class Queen:
    def __init__(self, color):
        self.color = color
        self.type = "queen"

    def GetValidMoves(self, x, y, board):
        valid_moves = []
        # combine rook and bishop style moves
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

    def GetAttackedSquares(self, x, y, board):
        attacked = []
        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (-1, -1),
            (1, -1),
            (-1, 1),
        ]
        for dx_dir, dy_dir in directions:
            for i in range(1, 8):
                dx, dy = dx_dir * i, dy_dir * i
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    attacked.append([dx, dy])
                    if board[ny][nx] is not None:
                        break
        return attacked


# defines the king class
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

        # castling checks (simplified but functional: check rook existence, hasn't moved, and path clear)
        if not self.has_moved:
            row = 7 if self.color == "white" else 0
            # kingside
            if (
                isinstance(board[row][7], Rook)
                and board[row][7].color == self.color
                and not board[row][7].has_moved
                and IsPathClear(x, row, 3, 0)
            ):
                valid_moves.append([2, 0])
            # queenside
            if (
                isinstance(board[row][0], Rook)
                and board[row][0].color == self.color
                and not board[row][0].has_moved
                and IsPathClear(x, row, -4, 0)
            ):
                valid_moves.append([-2, 0])

        return valid_moves

    def GetAttackedSquares(self, x, y, board):
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
        attacked = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                attacked.append([dx, dy])
        return attacked


# ----------------------------
# Utility functions: finding king, checking check, legal moves
# ----------------------------

# Defines a standalone function to find the king's position
def find_king(board_state, color):
    for row_idx, row in enumerate(board_state):
        for col_idx, piece in enumerate(row):
            if (
                piece is not None
                and isinstance(piece, King)
                and piece.color == color
            ):
                return (col_idx, row_idx)
    return None  # King not found


# Defines a standalone function to check if a king of a given color is in check
def is_king_in_check(board_state, color_to_check):
    king_pos = find_king(board_state, color_to_check)
    if king_pos is None:
        # This means the king is not on the board for some reason.
        return False

    kx, ky = king_pos
    # Iterate through all pieces on the board
    for y, row in enumerate(board_state):
        for x, piece in enumerate(row):
            # If the piece belongs to the opponent
            if piece is not None and piece.color != color_to_check:
                attacked_squares = piece.GetAttackedSquares(x, y, board_state)
                for dx, dy in attacked_squares:
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

                    # ensure destination inside board (should be by construction)
                    if not (0 <= x_dest < 8 and 0 <= y_dest < 8):
                        continue

                    # --- Simulate the move ---
                    # Create a shallow copy of the board rows (pieces are objects; careful with has_moved)
                    temp_board = [row[:] for row in current_board]

                    # capture original target (to restore if needed)
                    original_piece_at_target = temp_board[y_dest][x_dest]
                    original_piece_has_moved = None
                    if isinstance(piece, (King, Rook)):
                        # capture the has_moved state from the actual piece object on the real board
                        original_piece_has_moved = piece.has_moved

                    original_rook_at_castling_pos = None
                    original_rook_has_moved_state = None

                    # perform the move on temp_board
                    temp_board[y_dest][x_dest] = temp_board[y_orig][x_orig]
                    temp_board[y_orig][x_orig] = None

                    # handle castling rook movement on temp_board
                    if isinstance(temp_board[y_dest][x_dest], King):
                        if [dx, dy] == [2, 0]:  # kingside
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
                        elif [dx, dy] == [-2, 0]:  # queenside
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

                    # Temporarily update has_moved for the simulated piece if it's King or Rook
                    simulated_piece = temp_board[y_dest][x_dest]
                    if isinstance(simulated_piece, (King, Rook)):
                        simulated_piece.has_moved = True

                    # Check if the king is still in check after this move
                    if not is_king_in_check(temp_board, color_to_check):
                        return True  # Found at least one legal move

                    # --- Rollback is implicit since we used a temp_board copy ---
                    # No need to restore original states on the actual board
    return False  # No legal moves found


# ----------------------------
# Main & UI (Turtle)
# ----------------------------

def main():
    global selected_piece, board, piece_images, piece_turtles, cur_turn, view_orientation, window
    selected_piece = None

    # set up turtle window
    def setupWin():
        global window
        window = turtle.Screen()
        window.setup(WINX, WINY)
        window.bgcolor("white")

    setupWin()

    # piece image names
    piece_names = ["pawn", "knight", "bishop", "rook", "queen", "king"]
    colors = ["white", "black"]

    # register shapes (you must have pieces/<color>-<name>.gif files)
    for color in colors:
        for name in piece_names:
            filename = f"pieces/{color}-{name}.gif"
            try:
                turtle.register_shape(filename)
                piece_images[(name, color)] = filename
            except turtle.TurtleGraphicsError:
                # If the image isn't found, we simply do not register it. The code will still run.
                piece_images[(name, color)] = None

    # create two turtles for board and pieces
    BoardTurt = turtle.Turtle()
    PieceTurt = turtle.Turtle()
    turtle.setworldcoordinates(0, 8, 10, 0)

    # initialize board variable
    board.clear()

    def CreateBoard():
        board.clear()
        BoardTurt.ht()
        PieceTurt.ht()
        PieceTurt.penup()
        PieceTurt.pensize(10)
        BoardTurt.pensize(5)

        # empty 8x8
        for y in range(8):
            board.append([None for _ in range(8)])

        # pawns
        board[1] = [Pawn("black") for _ in range(8)]
        board[-2] = [Pawn("white") for _ in range(8)]

        # other pieces
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

    CreateBoard()

    def DrawBoard():
        BoardTurt.clear()
        for y in range(8):
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

    DrawBoard()
    turtle.update()

    def UpdateBoard():
        PieceTurt.clear()
        for t in piece_turtles:
            t.hideturtle()
            t.clear()
        piece_turtles.clear()

        # draw pieces
        for y in range(8):
            for x in range(8):
                piece = board[y][x]
                if piece:
                    img = piece_images.get((piece.type, piece.color))
                    t = turtle.Turtle()
                    t.hideturtle()
                    t.penup()
                    if img:
                        try:
                            t.shape(img)
                        except turtle.TurtleGraphicsError:
                            pass
                    # Adjust piece display coordinates based on view_orientation
                    display_x = x + 0.5
                    display_y = y + 0.5 if view_orientation == "white" else (7 - y) + 0.5
                    t.goto(display_x, display_y)
                    t.turtlesize(1)
                    t.showturtle()
                    piece_turtles.append(t)

        # highlight selected piece & moves
        if selected_piece is not None:
            PieceTurt.pencolor("green")
            display_x0 = selected_piece[0] + 0.1
            display_y0 = (
                (selected_piece[1] + 0.1) if view_orientation == "white" else (7 - selected_piece[1]) + 0.1
            )
            PieceTurt.penup()
            PieceTurt.goto(display_x0, display_y0)
            PieceTurt.pendown()
            for i in range(4):
                PieceTurt.forward(0.8)
                PieceTurt.right(-90)
            PieceTurt.penup()

            # highlight valid moves in red
            PieceTurt.pencolor("red")
            x0, y0 = selected_piece
            piece = board[y0][x0]
            if piece:
                for dx, dy in piece.GetValidMoves(x0, y0, board):
                    display_nx = x0 + dx + 0.1
                    display_ny = (y0 + dy + 0.1) if view_orientation == "white" else (7 - (y0 + dy)) + 0.1
                    PieceTurt.goto(display_nx, display_ny)
                    PieceTurt.pendown()
                    for i in range(4):
                        PieceTurt.forward(0.8)
                        PieceTurt.right(-90)
                    PieceTurt.penup()

            PieceTurt.pencolor("black")

        # simple pawn promotion (auto-queen) at back ranks
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
        PieceTurt.write(cur_turn.capitalize() + "'s", align="center", font=("Arial", 60, "normal"))
        PieceTurt.goto(9, 1.6)
        PieceTurt.write("Turn", align="center", font=("Arial", 60, "normal"))

        # Check for game end conditions
        if is_king_in_check(board, cur_turn):
            if not has_legal_moves(board, cur_turn):
                PieceTurt.penup()
                PieceTurt.goto(9, 3)
                PieceTurt.write("CHECKMATE!", align="center", font=("Arial", 25, "bold"))
            else:
                PieceTurt.penup()
                PieceTurt.goto(9, 3)
                PieceTurt.write("CHECK!", align="center", font=("Arial", 40, "bold"))
        elif not has_legal_moves(board, cur_turn):
            PieceTurt.penup()
            PieceTurt.goto(9, 3)
            PieceTurt.write("STALEMATE!", align="center", font=("Arial", 40, "bold"))

        # update the screen and schedule next update
        turtle.update()
        turtle.ontimer(UpdateBoard, 100)

    # defines the screen clicked function
    def ScreenClicked(x, y):
        global selected_piece, cur_turn, board, view_orientation

        # Prevent clicks if the game is over (checkmate or stalemate)
        game_over = (is_king_in_check(board, cur_turn) and not has_legal_moves(board, cur_turn)) or (not is_king_in_check(board, cur_turn) and not has_legal_moves(board, cur_turn))
        if game_over:
            return  # Do nothing if game is over

        # Convert screen coordinates to board coordinates based on current view_orientation
        board_x = int(math.floor(x))
        board_y = int(math.floor(y))

        if view_orientation == "black":
            board_y = 7 - board_y  # Invert y-coordinate for black's view

        # if the place clicked is outside the board
        if not (0 <= board_x < 8 and 0 <= board_y < 8):
            selected_piece = None  # Deselect if clicked outside the board
            return

        # if we currently have no piece selected
        if selected_piece is None:
            # and there is a piece in the place that we click, and it is that color's turn
            if board[board_y][board_x] is not None and board[board_y][board_x].color == cur_turn:
                selected_piece = [board_x, board_y]
        else:
            x0, y0 = selected_piece
            piece = board[y0][x0]
            if piece:
                valid_moves = piece.GetValidMoves(x0, y0, board)
                move = [board_x - x0, board_y - y0]

                # if the move is one of the valid moves that the piece can make
                if move in valid_moves:
                    # simulate on a temporary copy to check for king safety
                    temp_board = [row[:] for row in board]

                    original_piece_at_target = temp_board[board_y][board_x]
                    original_piece_has_moved = piece.has_moved if isinstance(piece, (King, Rook)) else None
                    original_rook_at_castling_pos = None
                    original_rook_has_moved_state = None

                    # perform move on the temp board
                    temp_board[board_y][board_x] = temp_board[y0][x0]
                    temp_board[y0][x0] = None

                    # handle castling rook movement on temp_board
                    simulated_piece_on_temp_board = temp_board[board_y][board_x]
                    if isinstance(simulated_piece_on_temp_board, King):
                        if move == [2, 0]:  # kingside
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
                        elif move == [-2, 0]:  # queenside
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

                    # temporarily update has_moved for the simulated piece if it's King or Rook
                    if isinstance(simulated_piece_on_temp_board, (King, Rook)):
                        simulated_piece_on_temp_board.has_moved = True

                    # Check if this simulated move puts the current player's king in check
                    if is_king_in_check(temp_board, cur_turn):
                        print("That move puts your king in check! Try again.")
                        selected_piece = None  # Deselect the piece
                    else:
                        # Apply the move to the actual game board
                        board[board_y][board_x] = board[y0][x0]
                        board[y0][x0] = None

                        # handle promotion (auto-queen)
                        if isinstance(board[board_y][board_x], Pawn):
                            if (board[board_y][board_x].color == "white" and board_y == 0) or (
                                board[board_y][board_x].color == "black" and board_y == 7
                            ):
                                board[board_y][board_x] = Queen(board[board_y][board_x].color)

                        # update has_moved property for King and Rook on the actual board
                        if isinstance(board[board_y][board_x], (King, Rook)):
                            board[board_y][board_x].has_moved = True

                        # handle castling rook movement on actual board
                        if isinstance(piece, King):
                            if move == [2, 0]:  # kingside castle
                                board[y0][x0 + 1] = board[y0][7]
                                board[y0][7] = None
                                if isinstance(board[y0][x0 + 1], Rook):
                                    board[y0][x0 + 1].has_moved = True
                            elif move == [-2, 0]:  # queenside castle
                                board[y0][x0 - 1] = board[y0][0]
                                board[y0][0] = None
                                if isinstance(board[y0][x0 - 1], Rook):
                                    board[y0][x0 - 1].has_moved = True

                        selected_piece = None
                        cur_turn = "black" if cur_turn == "white" else "white"
                        view_orientation = cur_turn  # flip the board for the next player

                        DrawBoard()  # Redraw the board after flipping orientation
                else:
                    selected_piece = None  # Deselect the piece if the move wasn't valid

    # bind click handler and start update loop
    turtle.onscreenclick(ScreenClicked)
    UpdateBoard()
    window.mainloop()


if __name__ == "__main__":
    main()
