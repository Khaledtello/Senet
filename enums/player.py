from enum import Enum

class Player(Enum):
    Black = "B"
    White = "W"

    def symbol(self):
        return self.value
    
    def name(self):
        return "BLACK" if self == self.Black else "WHITE"