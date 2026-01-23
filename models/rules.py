from enums.player import Player
from enums.cell_type import CellType
from models.state import State
from models.grid import Grid

class Rules:
    _step_probability = {
        1: 4/16,
        2: 6/16,
        3: 4/16,
        4: 1/16,
        5: 1/16,
    }

    @staticmethod
    def all_steps():
        return Rules._step_probability.copy().items()
    
    @staticmethod
    def pieces_on_board(state: State, player: Player) -> int:
        return len(state.grid.cells_of_player(player))
    
    @staticmethod
    def pieces_finished(state: State, player: Player) -> int:
        return 7 - Rules.pieces_on_board(state, player)

    @staticmethod
    def is_win(state: State, player: Player) -> bool:
        return Rules.pieces_on_board(state, player) == 0
    
    @staticmethod
    def winner(state: State) -> Player | None:
        if Rules.is_win(state, Player.Blue): return Player.Blue
        if Rules.is_win(state, Player.Red): return Player.Red
    
    @staticmethod
    def is_terminal(state: State) -> bool:
        return Rules.winner(state) is not None
        
    @staticmethod
    def _can_leave(state: State, position: int) -> bool:
        cell_type = state.grid.get_type(position)

        if cell_type == CellType.HAPPINESS:
            return state.step == 5
        
        if cell_type == CellType.THREE_TRUTHS:
            return state.step == 3

        if cell_type == CellType.RE_ATOUM:
            return state.step == 2

        return cell_type == CellType.HORUS
    
    @staticmethod
    def _is_legal_move(state: State, position: int) -> bool:
        hap_pos = state.grid.cells_of_type(CellType.HAPPINESS)[0]
        to_pos = position + state.step

        if position == hap_pos: return True

        if position > hap_pos: return Rules._can_leave(state, position)

        if position < hap_pos and to_pos > hap_pos: return False

        return state.grid.get_player(to_pos) != state.player  

    @staticmethod
    def legal_moves(state: State) -> list[int]:
        return [pos for pos in state.grid.cells_of_player(state.player) if Rules._is_legal_move(state, pos)]
                
    @staticmethod
    def _rebirth_illegal_pieces(grid: Grid, player: Player, last_move: int | None = None) -> Grid:
        for pos in grid.cells_of_player(player):
            if grid.get_type(pos) == CellType.WATER:
                return grid.rebirth_piece(pos)

            if pos != last_move and grid.get_type(pos) in (
                CellType.THREE_TRUTHS,
                CellType.RE_ATOUM,
                CellType.HORUS):
                return grid.rebirth_piece(pos)

        return grid

    @staticmethod
    def apply_move(state: State, position: int) -> State:
        if Rules._can_leave(state, position):
            new_grid = state.grid.move_piece(position, None)
        else:
            to_pos = position + state.step
            new_grid = state.grid.move_piece(position, to_pos)
            new_grid = Rules._rebirth_illegal_pieces(new_grid, state.player, to_pos)

        return state.copy_with(grid=new_grid)
    
    @staticmethod
    def skip_move(state: State):
        new_gird = Rules._rebirth_illegal_pieces(state.grid, state.player)
        return state.copy_with(grid=new_gird)
    
    @staticmethod
    def successors(state: State):
        moves = Rules.legal_moves(state)
        player = state.player.opposite()
        
        if not moves:
            return [(Rules.skip_move(state).copy_with(player=player), None)]
        
        return [(Rules.apply_move(state, move).copy_with(player=player), move) for move in moves]
