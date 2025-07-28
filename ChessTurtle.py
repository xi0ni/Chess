import turtle
import math

window  = None
WINX, WINY = 800, 800
turtle.tracer(False)  # Disable animation for faster drawing

def main():

    global selected_piece
    selected_piece = None

    def setupWin():
        global window
        # making turtle object
        window = turtle.Screen()
        # set screen size
        window.setup(WINX,WINY)
        # set background color
        window.bgcolor("white")
    
    
    setupWin()

    BoardTurt=turtle.Turtle()
    PieceTurt=turtle.Turtle()


    turtle.setworldcoordinates(0, 0, 8, 8)

    # creates the board object for our data structure
    board = []

    # defines a create board method
    def CreateBoard():

        BoardTurt.ht()
        PieceTurt.ht()
        PieceTurt.penup()
        PieceTurt.pensize(10)
        BoardTurt.pensize(5)
        # creates a blank board
        for y in range(8):
            y_list = []
            for x in range(8):
                y_list.append([])

            board.append(y_list)

        # sets the second and second to last rows to pawns
        # the first part in the list signifies the piece and the second part signifies the color of the piece so you cant take your own pieces
        board[1] = [['pawn','black'],['pawn','black'],['pawn','black'],['pawn','black'],['pawn','black'],['pawn','black'],['pawn','black'],['pawn','black']]
        board[-2] = [['pawn','white'],['pawn','white'],['pawn','white'],['pawn','white'],['pawn','white'],['pawn','white'],['pawn','white'],['pawn','white']]

        board[0] = [['rook','black'],['knight','black'],['bishop','black'],['queen','black'],['king','black'],['bishop','black'],['knight','black'],['rook','black']]
        board[-1] = [['rook','white'],['knight','white'],['bishope','white'],['queen','white'],['king','white'],['bishop','white'],['knight','white'],['rook','white']]

    CreateBoard()

    def DrawBoard():
        # draws the board
        for y in range(8):
            for x in range(8):
                BoardTurt.penup()
                BoardTurt.goto(x, y)
                BoardTurt.pendown()
                if (x + y) % 2 == 0:
                    BoardTurt.fillcolor("white")
                else:
                    BoardTurt.fillcolor("brown")
                BoardTurt.begin_fill()
                for i in range(4):
                    BoardTurt.forward(1)
                    BoardTurt.right(-90)
                BoardTurt.end_fill()

    DrawBoard()

    turtle.update()  # Update the screen to show the drawn board

    def CreateMovesList():

        # defines the valid moves for each piece
        # this is used to determine if a move is legal or not
        global valid_moves
        valid_moves = {}

        # each of the lists in the valid moves signifies the x+ and y+ that is a legal move
        valid_moves['pawn'] = [[0,1]]
        valid_moves['knight'] = [[1,2], [2,1], [-1,2], [-2,1], [1,-2], [2,-1], [-1,-2], [-2,-1]]
        valid_moves['king'] = [[0,1], [1,0], [0,-1], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]
        valid_moves['rook'] = []
        # adds the rook moves in all 4 directions
        for i in range(8):
            valid_moves['rook'].append([i, 0])
            valid_moves['rook'].append([-i, 0])
            valid_moves['rook'].append([0, i])
            valid_moves['rook'].append([0, -i])

        valid_moves['bishop'] = []
        # adds the bishop moves in all 4 diagonal directions
        for i in range(8):
            valid_moves['bishop'].append([i, i])
            valid_moves['bishop'].append([-i, -i])
            valid_moves['bishop'].append([i, -i])
            valid_moves['bishop'].append([-i, i])

        valid_moves['queen'] = []
        # adds the queen moves in all 4 directions and all 4 diagonal directions
        for i in range(8):
            valid_moves['queen'].append([i, 0])
            valid_moves['queen'].append([-i, 0])
            valid_moves['queen'].append([0, i])
            valid_moves['queen'].append([0, -i])
            valid_moves['queen'].append([i, i])
            valid_moves['queen'].append([-i, -i])
            valid_moves['queen'].append([i, -i])
            valid_moves['queen'].append([-i, i])

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


        if selected_piece != None:

            # highlights the selected piece in green
            PieceTurt.pencolor("green")
            PieceTurt.penup()
            PieceTurt.goto(selected_piece[0]+0.1, selected_piece[1]+0.1)
            PieceTurt.pendown()
            for i in range(4):
                PieceTurt.forward(0.8)
                PieceTurt.right(-90)
            PieceTurt.penup()
            
            # highlights the valid moves for the selected piece in red
            PieceTurt.pencolor("red")
            for move in valid_moves[board[selected_piece[1]][selected_piece[0]][0]]:
                x = selected_piece[0] + move[0]
                y = selected_piece[1] + move[1]
                if x >= 0 and x < 8 and y >= 0 and y < 8:
                    if board[y][x] == [] or board[y][x][1] != board[selected_piece[1]][selected_piece[0]][1]:
                        PieceTurt.goto(x + 0.1, y + 0.1)
                        PieceTurt.pendown()
                        for i in range(4):
                            PieceTurt.forward(0.8)
                            PieceTurt.right(-90)
                        PieceTurt.penup()

            PieceTurt.pencolor("black")

        PieceTurt.goto(0, 0)
        turtle.update()  # Update the screen to show the pieces
        turtle.ontimer(UpdateBoard, 10)


    def ScreenClicked(x, y):
        global selected_piece
        x = int(math.floor(x))
        y = int(math.floor(y))
        if x >= 0 and x <= 8 and y >= 0 and y <= 8:
            if selected_piece == None:
                selected_piece = [x, y]
                print(selected_piece)
            else:
                board[y][x] = board[selected_piece[1]][selected_piece[0]]
                board[selected_piece[1]][selected_piece[0]] = []
                selected_piece = None
        print(selected_piece)

        

    turtle.onscreenclick(ScreenClicked)

    UpdateBoard()


    # Do not edit
    window.mainloop()


main()
