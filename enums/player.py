from enum import Enum
from colorama import Fore

class Player(Enum):
    Blue = "B"
    Red = "R"
    
    def opposite(self) -> "Player":
        return Player.Blue if self == Player.Red else Player.Red
    
    def symbol(self):
        return self.value
    
    def name(self):
        return "BLUE" if self == self.Blue else "RED"
    
    def color(self):
        return Fore.BLUE if self == Player.Blue else Fore.RED