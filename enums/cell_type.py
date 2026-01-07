from enum import Enum

class CellType(Enum):
    NORMAL = " "
    REBIRTH = "R"
    HAPPINESS = "H"
    WATER = "~"
    THREE_TRUTHS = "3"
    RE_ATOUM = "2"
    HORUS = "*"

    def symbol(self):
        return self.value