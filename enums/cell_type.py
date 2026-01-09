from enum import Enum

class CellType(Enum):
    NORMAL = " "
    REBIRTH = "R"
    HAPPINESS = "H"
    WATER = "~"
    THREE_TRUTHS = "T"
    RE_ATOUM = "A"
    HORUS = "*"

    def symbol(self):
        return self.value