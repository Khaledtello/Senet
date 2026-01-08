from models.grid import Grid
from enums.player import Player

class State:
    def __init__(self, grid: Grid, player: Player, step: int):
        self._grid = grid
        self._player = player
        self._step = step

    @property
    def grid(self) -> Grid:
        return self._grid

    @property
    def player(self) -> Player:
        return self._player

    @property
    def step(self) -> int:
        return self._step
    
    def copy_with(self, grid: Grid | None = None, player: Player | None = None, step: int | None = None):
        return State(
            self.grid if grid is None else grid,
            self.player if player is None else player,
            self.step if step is None else step,
        )
    
    def __eq__(self, value):
        if not isinstance(value, State): return False
        
        return (
            self.grid == value.grid and
            self.player == value.player and
            self.step == value.step
        )
    
    def __hash__(self):
        return hash((self.grid, self.player, self.step))