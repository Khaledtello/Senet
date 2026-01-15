import math
from models.state import State
from models.rules import Rules
from enums.player import Player
from enums.mode import Mode
from algorithms.nodes import *

class Exminimax:
    _minimax_cache = {}
    _expect_cache = {}
    _visited_nodes = 0

    @staticmethod
    def _evaluation_of(state: State, player: Player) -> int:
        result = 0
        for pos in state.grid.cells_of_player(player):
            result += (22*22 if pos == 24 else pos*pos)
            
        return result + Rules.pieces_finished(state, player) * 2000

    @staticmethod
    def _evaluation(state: State, player: Player) -> int:
        return Exminimax._evaluation_of(state, player) - Exminimax._evaluation_of(state, player.opposite())

    @staticmethod
    def choose_move(state: State, mode:Mode):
        Exminimax._visited_nodes = 0
        return Exminimax._minimax(state, mode.value, state.player), Exminimax._visited_nodes

    @staticmethod
    def _minimax(state: State, depth: int, root_player: Player) -> MoveNode:
        Exminimax._visited_nodes += 1
        key = (state, depth, root_player)
        cache = Exminimax._minimax_cache

        if key in cache: return cache[key]

        maximize = state.player == root_player
        best_value = -math.inf if maximize else math.inf
        best_move = None

        expect_nodes = []
        for child, move in Rules.successors(state):
            node = Exminimax._expect(child, depth-1, root_player)
            expect_nodes.append(node)
            if maximize and best_value < node.value or not maximize and best_value > node.value:
                best_move = move
                best_value = node.value
            
        cache[key] = MoveNode(maximize, best_move, best_value, expect_nodes)
        return cache[key]

    @staticmethod 
    def _expect(state: State, depth: int, root_player: Player) -> ChanceNode:
        Exminimax._visited_nodes += 1
        key = (state.grid, state.player, depth, root_player)
        cache = Exminimax._expect_cache

        if key in cache: return cache[key]

        if Rules.is_terminal(state) or depth <= 0:
            cache[key] = ChanceNode(Exminimax._evaluation(state, root_player), None)
            return cache[key]
        
        expect = 0
        minimax_nodes = []
        for step, probability in Rules.all_steps():
            node = Exminimax._minimax(state.copy_with(step=step), depth, root_player)
            minimax_nodes.append(node)
            expect += probability * node.value

        cache[key] = ChanceNode(expect, minimax_nodes)
        return cache[key]