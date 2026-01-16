from models.state import State
from models.rules import Rules
from enums.player import Player
from enums.mode import Mode
from algorithms.expectiminimax import Exminimax
from algorithms.nodes import *
from colorama import Fore

class ConsoleUI:
    @staticmethod
    def game_name() -> None:
        print("\033[1m")
        print("=" * 51)
        print(" " * 22 + "SENET")
        print("=" * 51 + "\n")

    @staticmethod
    def choose_mode() -> Mode:
        for mode in (Mode):
            print(f"{mode.value+1}. Human vs {mode.name()}")

        choose = int(input("\nSelect Mode: "))
        return Mode.get_by_value(choose-1)
    
    @staticmethod
    def with_debug_ai() -> bool:
        choose = input("Do you want make debug to AI (Y/N): ")
        return choose.lower() == "y"
    
    @staticmethod
    def show_state(state: State) -> None:
        print("=" * 51)
        for row in range(3):
            for col in range(10):
                pos = row * 10 + (9 - col if row == 1 else col)

                player = state.grid.get_player(pos)
                type = state.grid.get_type(pos).symbol()

                p_color = Fore.RESET if player is None else Fore.BLUE if player == Player.Blue else Fore.RED
                print(Fore.RESET + "| ", end="")
                print(p_color + f"{pos:02d}" + type, end="")

            print(Fore.RESET + "|")

        print(f"{Fore.BLUE}{state.player.name()}   : {Rules.pieces_finished(state, Player.Blue)}")
        print(f"{Fore.RED}{state.player.name()}    : {Rules.pieces_finished(state, Player.Red)}")
        print(f"{Fore.RESET}Player : {state.player.color()}{state.player.name()}")
        print(f"{Fore.RESET}Step   : {state.step}")
        print("=" * 51)

    @staticmethod
    def show_winner(winner: Player) -> None:
        print(f"Game Over! {winner.color()}{winner.name()}{Fore.RESET} wins.")

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
    def ai_move(state: State, mode: Mode, debug) -> int | None:
        moves = Rules.legal_moves(state)
        if not moves:
            print("No legal moves. Turn skipped.")
            return None

        print(f"Legal moves: {moves}")
        print("AI is thinking...")

        move_node, visited_nodes = Exminimax.choose_move(state, mode)

        if debug:
            print(Fore.YELLOW)
            ConsoleUI._debug_ai(move_node)
            print(f"Visited nodes: {visited_nodes}")
            print(f"Move evaluation: {move_node.value}")
            print(Fore.RESET)

        print(f"AI choose: {move_node.move}")

        return move_node.move
    
    def _debug_ai(node: MoveNode | ChanceNode, indent=1):
        if isinstance(node, MoveNode):
            node_type = "MAX" if node.maximize else "MIN"
            print(f"{node_type} chose move {node.move} → value = {node.value:.2f}")
            chosen = next(n for n in node.children if n.value == node.value)
            ConsoleUI._debug_ai(chosen, indent)
            return

        prefix = "  " * indent
    
        if node.children is None:
            print(f"{prefix}LEAF value = {node.value:.2f}")
            return

        print(f"{prefix}CHANCE expected = {node.value:.2f}")

        for i, child in enumerate(node.children, 1):
            print(f"{prefix}  step {i}: ", end="")
            ConsoleUI._debug_ai(child, indent+2)

    def _debug_ai2(node: MoveNode | ChanceNode, indent=1):
        prefix = "  " * indent
        
        if node.children is None:
            print(f"{prefix}LEAF value = {node.value:.2f}")

        elif isinstance(node, MoveNode):
            node_type = "MAX" if node.maximize else "MIN"
            print(f"{node_type} chose move {node.move} → value = {node.value:.2f}")

        else:
            print(f"{prefix}CHANCE expected = {node.value:.2f}")
            indent += 2

        if node.children is not None:
            for i, child in enumerate(node.children, 1):
                if isinstance(node, ChanceNode):
                    print(f"{prefix}  step {i}: ", end="")
                ConsoleUI._debug_ai2(child, indent)