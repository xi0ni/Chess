from ursina import *


class Piece:
    def __init__(self, color, name):
        self.name = name
        self.color = color
        self.texture = f'pieces/{color}-{name}.png'

    def on_place(self):
        if self.color == 'white':
            self.color = 'black'
        else:
            self.color = 'white'
        self.texture = f'pieces/{self.color}-{self.name}.png'
