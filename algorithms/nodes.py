from dataclasses import dataclass

@dataclass
class MoveNode:
    isMax: bool
    move: int | None
    value: float
    children: list["ChanceNode"]

@dataclass
class ChanceNode:
    value: float
    children: list["MoveNode"] | None = None