from models.state import State
from models.rules import Rules
from enums.player import Player
from enums.mode import Mode

class ConsoleUI:
    @staticmethod
    def choose_mode() -> Mode:
        print("=" * 40)
        print(" " * 17, "SENET")
        print("=" * 40)
        print("1. Human vs Human")
        print("2. Human vs AI")

        mode = int(input("\nSelect Mode: "))
        return Mode.AI if mode == 2 else Mode.Human
    
    @staticmethod
    def show_state(state: State) -> None:
        print("=" * 40)
        print(state.grid)
        print(f"Black  : {Rules.pieces_finished(state, Player.Black)}")
        print(f"White  : {Rules.pieces_finished(state, Player.White)}")
        print(f"Player : {state.player.name()}")
        print(f"Step   : {state.step}")
        print("=" * 40)

    @staticmethod
    def choose_move(legal_moves: list[int]) -> int | None:
        if not legal_moves:
            print("No legal moves. Turn skipped.")
            input("Press Enter...")
            return None

        print(f"Legal moves: {legal_moves}")

        while True:
            try:
                choice = int(input("Choose move: "))
                if legal_moves.__contains__(choice):
                    return choice
            except ValueError:
                pass

            print("Invalid choice.")

    @staticmethod
    def show_winner(winner: Player) -> None:
        print(f"Game Over! {winner.name()} wins.")