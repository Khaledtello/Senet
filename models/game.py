from models.state import State
from enums.player import Player
from enums.mode import Mode
from models.rules import Rules
from ui.console_ui import ConsoleUI
import random

class Game:
    @staticmethod
    def _generate_step(state: State) -> State:
        step = sum(random.choice((0, 1)) for _ in range(4))
        return state.copy_with(step=5 if step == 0 else step)
    
    @staticmethod
    def _switch_player(state: State) -> State:
        return state.copy_with(player=state.player.opposite())
    
    @staticmethod
    def run(mode: Mode, state: State):
        while not Rules.is_terminal(state):
            state = Game._generate_step(state)

            ConsoleUI.show_state(state)
            if state.player == Player.Blue or mode == Mode.Human:
                move = ConsoleUI.choose_move(Rules.legal_moves(state))
            else:
                move = ConsoleUI.ai_move(state, 4)

            if move is None:
                state = Rules.skip_move(state)
            else:
                state = Rules.apply_move(state, move)

            state = Game._switch_player(state)

        ConsoleUI.show_winner(Rules.winner(state))