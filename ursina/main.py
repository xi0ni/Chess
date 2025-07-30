from ursina import *
from ursinaBoard import *

def main():
    app = Ursina()  
    CreateBoard()

    # Now it's safe to modify the camera
    camera.orthographic = True
    camera.fov = 10
    camera.position = (3, 3.5)
    Text.default_resolution *= 2
    mouse.visible = False


    # Background
    bg = Entity(
        parent=scene,
        model="quad",
        texture="sky_default",
        scale=(160, 80),
        z=10,
        color=color.light_gray,
    )

    # Board layout in 8x8
    b_board = [[None for x in range(8)] for y in range(8)]
    for y in range(8):
        for x in range(8):
            color_tile = rgb(1, 1, 1) if x % 2 == 1 - y % 2 else rgb(0.28, 0.28, 0.27)
            b = Button(parent=scene, position=(x, y), color=color_tile)
            b_board[x][y] = b

    app.run()

if __name__ == "__main__":
    main()


