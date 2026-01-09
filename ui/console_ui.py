from models.state import State
from models.rules import Rules
from enums.player import Player
from enums.mode import Mode
from algorithms.expectiminimax import Exminimax
from colorama import Fore, Back, Style

class ConsoleUI:
    @staticmethod
    def init() -> None:
        print("\033[1m")
        print("=" * 50)
        print(" " * 22 + "SENET")
        print("=" * 50 + "\n")

    @staticmethod
    def choose_mode() -> Mode:
        for mode in (Mode):
            print(f"{mode.value+1}. Human vs {mode.name()}")

        choose = int(input("\nSelect Mode: "))
        return [mode for mode in Mode if mode.value == choose-1][0]
    
    @staticmethod
    def show_state(state: State) -> None:
        print("=" * 50)
        for row in range(3):
            for col in range(10):
                pos = row * 10 + (9 - col if row == 1 else col)

                player = state.grid.get_player(pos)
                type = state.grid.get_type(pos).symbol()

                p_color = Fore.RESET if player is None else Fore.BLUE if player == Player.Blue else Fore.RED
                print(Fore.RESET + "| ", end="")
                print(p_color + f"{pos:02d}" + type, end="")

            print(Fore.RESET + "|")

        print(f"{Fore.BLUE}BLUE   : {Rules.pieces_finished(state, Player.Blue)}")
        print(f"{Fore.RED}RED    : {Rules.pieces_finished(state, Player.Red)}")
        print(f"{Fore.RESET}Player : {state.player.name()}")
        print(f"Step   : {state.step}")
        print("=" * 50)

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
    def ai_move(state: State, depth: int) -> int | None:
        moves = Rules.legal_moves(state)
        if not moves:
            print("No legal moves. Turn skipped.")
            return None

        print(f"Legal moves: {moves}")
        print("AI is thinking...")

        move = Exminimax.choose_move(state, depth)

        print(f"AI choose: {move}")

        return move

    @staticmethod
    def show_winner(winner: Player) -> None:
        print(f"Game Over! {winner.color()}{winner.name()}{Fore.RESET} wins.")