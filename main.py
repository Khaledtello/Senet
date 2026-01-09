from models.game import Game
from models.grid import Grid
from models.state import State
from enums.player import Player
from ui.console_ui import ConsoleUI

ConsoleUI.init()
init_state = State(Grid.initial(), Player.Blue, 0)
mode = ConsoleUI.choose_mode()

Game.run(mode, init_state)