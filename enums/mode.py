from enum import Enum

class Mode(Enum):
    Human = 0
    AI_1 = 1
    AI_2 = 2
    AI_3 = 3
    AI_4 = 4

    def name(self):
        return {
            Mode.Human: "Human",
            Mode.AI_1: "Easy AI",
            Mode.AI_2: "Medium AI",
            Mode.AI_3: "Hard AI",
            Mode.AI_4: "Expert AI",
        }.get(self, Mode.Human)
    
    def get_by_value(value: int) -> "Mode":
        modes = [mode for mode in Mode if mode.value == value]
        return Mode.Human if modes is None else modes[0]