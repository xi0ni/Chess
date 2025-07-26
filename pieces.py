class Piece:
    def __init__(self, color, name):
        self.name = name
        self.color = color
        self.texture = f'pieces/{color}-{name}.png'

    def on_place(self):
        self.color = 'black' if self.color == 'white' else 'white'
        self.texture = f'pieces/{self.color}-{self.name}.png'
