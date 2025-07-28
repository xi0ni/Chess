from ursina import *

# Create the game window
app = Ursina()

board = []


class Piece(Entity):
    def __init__(self, team, name, **kwargs):
        super().__init__(model="quad", texture=f"pieces/{team}-{name}.png", scale=1, **kwargs)
        self.team = team
        self.name = name
        self.collider = 'box'  # Enables mouse collision

    def on_place(self):
        self.team = "black" if self.team == "white" else "white"
        self.texture = f"pieces/{self.team}-{self.name}.png"

    def place(self, x, y, z=-0.5):
        self.position = (x, y, z)

    def place_check(self):
        print(self.position)

    def move_piece(self):
        pass


def CreateBoard():
    global board
    board = [[None for _ in range(8)] for _ in range(8)]

    # White pieces (bottom row)
    white_back_row = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    for x, name in enumerate(white_back_row):
        piece = Piece("white", name)
        piece.place(x, 0)
        board[0][x] = piece

    for x in range(8):
        pawn = Piece("white", "pawn")
        pawn.place(x, 1)
        board[1][x] = pawn

    # Black pieces (top row)
    black_back_row = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    for x, name in enumerate(black_back_row):
        piece = Piece("black", name)
        piece.place(x, 7)
        board[7][x] = piece

    for x in range(8):
        pawn = Piece("black", "pawn")
        pawn.place(x, 6)
        board[6][x] = pawn


# Initialize the board
CreateBoard()

# Cursor and selection
player = Piece("white", "rook")
cursor = Entity(model="quad", texture=player.texture, color=color.rgba(255, 255, 255, 150), scale=1.05, z=-0.4)
clicked = False


def clear_square(x, y):
    global board
    piece = board[y][x]
    if piece:
        print(f"Clearing piece at ({x}, {y}) - {piece.name}")
        piece.disable()
        board[y][x] = None


def update():
    global clicked, player

    if mouse.left and not clicked:
        clicked = True

        # Convert mouse pos (-1 to 1) into board coordinates (0 to 7)
        board_x = int((mouse.position.x + 1) * 4)
        board_y = int((mouse.position.y + 1) * 4)

        if 0 <= board_x < 8 and 0 <= board_y < 8:
            if mouse.hovered_entity:
                clear_square(board_x, board_y)
                player = mouse.hovered_entity
                if player.texture:
                    cursor.texture = player.texture
            else:
                print(f"No hovered entity at ({board_x}, {board_y})")

    elif not mouse.left:
        clicked = False

    # Update cursor position
    cursor.position = mouse.position * 10 + Vec3(4, 4, 0)


# Create a board background (optional for visual clarity)
for y in range(8):
    for x in range(8):
        Entity(model='quad',
               color=color.white if (x + y) % 2 == 0 else color.gray,
               position=(x, y, -1),
               scale=1)

# Camera setup
camera.orthographic = True
camera.fov = 10
camera.position = (3.5, 3.5, -10)

app.run()
