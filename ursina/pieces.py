from ursina import *


class Piece(Entity):
    def __init__(self, team, name, **kwargs):
        super().__init__(model="quad", texture=f"pieces/{team}-{name}.png", **kwargs)
        self.team = team 
        self.name = name
        self.collider = 'box'

    def on_place(self):
        self.team = "black" if self.team == "white" else "white"
        self.texture = f"pieces/{self.team}-{self.name}.png"

    def place(self, x, y):
        self.position = (x, y, -1)

    def place_check(self):
        print(self.position)

    def move_piece(self):
        pass

    

#siefjwoeifj