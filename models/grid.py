from enums.cell_type import CellType
from enums.player import Player

class Grid:
    def __init__(self, cells: list[Player] = None):
        self._cells = [None] * 30 if cells == None else cells
        self._special_cells = {
            14: CellType.REBIRTH,
            25: CellType.HAPPINESS,
            26: CellType.WATER,
            27: CellType.THREE_TRUTHS,
            28: CellType.RE_ATOUM,
            29: CellType.HORUS,
        }

    def get_player(self, position: int) -> Player:
        return self._cells[position]

    def _set_player(self, position: int, player: Player | None) -> None:
        self._cells[position] = player

    def is_empty(self, position: int) -> bool:
        return self._cells[position] is None
    
    def get_type(self, position: int) -> CellType:
        return self._special_cells.get(position, CellType.NORMAL)
    
    def cells_of_type(self, type: CellType) -> int:
        return [pos for pos in range(30) if self.get_type(pos) == type]
    
    def cells_of_player(self, player:Player) -> list[int]:
        return [pos for pos in range(30) if self.get_player(pos) == player]

    @staticmethod
    def initial() -> "Grid":
        grid = Grid()
        for i in range(14):
            grid._set_player(i, Player.Black if i % 2 else Player.White)

        return grid
    
    def copy(self) -> "Grid":
        return Grid(self._cells.copy())
    
    def move(self, from_pos: int, to_pos: int | None) -> "Grid":
        new_grid = self.copy()
        if to_pos is None:
            new_grid._set_player(from_pos, None)
            return new_grid

        from_player = new_grid.get_player(from_pos)
        to_player = new_grid.get_player(to_pos)
        new_grid._set_player(to_pos, from_player)
        new_grid._set_player(from_pos, to_player)
        return new_grid

    def rebirth(self, from_pos: int) -> "Grid":
        reb_pos = self.cells_of_type(CellType.REBIRTH)[0]
        for to_pos in range(reb_pos, -1, -1):
            if self.get_player(to_pos) is None:
                return self.move(from_pos, to_pos)
        return self

    def __str__(self):
        lines = []

        for row in range(3):
            line = []
            for col in range(10):
                position = row * 10 + (9 - col if row == 1 else col)

                player = self.get_player(position)
                player_char = " " if player == None else player.symbol()

                cell_type = self.get_type(position)

                line.append(f"[{position:02d}|{player_char}|{cell_type.symbol()}]")

            lines.append(" ".join(line))

        return "\n".join(lines)
