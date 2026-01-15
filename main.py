from models.game import Game
from models.grid import Grid
from models.state import State
from enums.player import Player
from enums.mode import Mode
from ui.console_ui import ConsoleUI

ConsoleUI.game_name()
init_state = State(Grid.initial(), Player.Blue, 0)
mode = ConsoleUI.choose_mode()
debug = False if mode == Mode.Human else ConsoleUI.with_debug_ai()

Game.run(init_state, mode, debug)