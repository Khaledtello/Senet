from models.state import State
from models.rules import Rules
from enums.player import Player
import sys

class Exminimax:
    _cache = {}
    _root_cache = {}

    @staticmethod
    def _evaluation_of(state: State, player: Player) -> int:
        result = 0
        for pos in state.grid.cells_of_player(player):
            result += (22*22 if pos == 24 else pos*pos)
            
        result += Rules.pieces_finished(state, player) * 2000
        return result

    @staticmethod
    def _evaluation(state: State, player: Player) -> int:
        return Exminimax._evaluation_of(state, player) - Exminimax._evaluation_of(state, player.opposite())

    @staticmethod
    def choose_move(state: State, depth: int) -> int:
        key = (state.grid, state.player, depth)
        cache = Exminimax._root_cache
        best_score = -sys.maxsize

        if key in cache: return cache[key][1]

        best_move = None

        for child, move in Rules.successors(state):
            score = Exminimax._exminimax(child, depth-1, state.player)
            if best_score < score:
                best_move = move
                best_score = score

        cache[key] = (best_score, best_move)
        return best_move

    @staticmethod 
    def _exminimax(state: State, depth: int, root_player: Player) -> int | float:
        key = (state.grid, state.player, depth, root_player)
        cache = Exminimax._cache

        if key in cache: return cache[key]

        if Rules.is_terminal(state) or depth <= 0:
            cache[key] = Exminimax._evaluation(state, root_player)
            return cache[key]
        
        maximize = state.player == root_player
        cache[key] = 0

        for step, probability in Rules.all_steps():
            best_score = sys.maxsize * -1 if maximize else 1
            fun = max if maximize else min

            for child, _ in Rules.successors(state.copy_with(step=step)):
                score = Exminimax._exminimax(child, depth-1, root_player)
                best_score = fun(best_score, score)

            cache[key] += probability * best_score

        return cache[key]