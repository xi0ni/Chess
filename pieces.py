from ursina import *


class Piece(Entity):
    def __init__(self, team, name, **kwargs):
        super().__init__(model="quad", texture=f"pieces/{team}-{name}.png", **kwargs)
        self.team = team  # was `color`, now renamed
        self.name = name

    def on_place(self):
        self.team = "black" if self.team == "white" else "white"
        self.texture = f"pieces/{self.team}-{self.name}.png"

    def place(self, x, y, z):
        self.position = (x, y, z)

    def place_check(self):
        print(self.position)

    def setup(self, color, side):
        for x in range(8):
            if color == 'white':
                
            