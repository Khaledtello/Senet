from models.state import State
from models.rules import Rules
from enums.player import Player
import sys

class Expectiminimax:
    @staticmethod
    def _evaluation(state: State, player: Player) -> int:
        result = sum(pos * pos for pos in state.grid.cells_of_player(player))
        result -= sum(pos * pos for pos in state.grid.cells_of_player(player.opposite()))

        return result

    @staticmethod
    def choose_move(state: State, depth: int) -> int:
        best_move = None
        best_score = -sys.maxsize

        for child, move in Rules.successors(state):
            score = Expectiminimax._expectiminimax(child, depth-1, state.player)
            if best_score < score:
                best_move = move
                best_score = score
        
        return best_move


    @staticmethod 
    def _expectiminimax(state: State, depth: int, root_player: Player) -> int | float:        
        if Rules.is_terminal(state) or depth <= 0:
            return Expectiminimax._evaluation(state, root_player)
        
        maximize = state.player == root_player

        for step, probability in Rules.all_steps():
            best_score = sys.maxsize * 1 if maximize else -1
            fun = max if maximize else min

            for child, _ in Rules.successors(state.copy_with(step=step)):
                score = Expectiminimax._expectiminimax(child, depth-1, root_player)
                best_score = fun(best_score, score)

            result += probability * best_score

        return result