from dataclasses import dataclass

@dataclass
class MoveNode:
    maximize: bool
    move: int | None
    value: float
    children: list["ChanceNode"]

@dataclass
class ChanceNode:
    value: float
    children: list["MoveNode"] | None = None