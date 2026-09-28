# Senet – Expectiminimax AI

A Python implementation of the ancient Egyptian board game **Senet**, developed as a practical project for the **Intelligent Search Algorithms** course at Damascus University – Faculty of Informatics Engineering.

The project supports both **Human vs Human** and **Human vs AI** gameplay. The AI uses the **Expectiminimax** algorithm to handle the randomness introduced by the four-stick toss.

---

## Features

- Human vs Human gameplay
- Human vs AI gameplay
- Four search-depth levels (1–4)
- Expectiminimax search with Max/Min and Chance nodes
- Probability-based handling of stick tosses
- Immutable `Grid` and `State` representations
- Successor-state generation through a centralized `Rules` class
- Memoization / caching for search nodes
- Search-node counting
- Debug mode for inspecting AI decisions and search information
- Colored console interface
- Separate `MoveNode` and `ChanceNode` structures for representing the search tree

---

## Game Overview

The implementation follows the **Kendall's Rules** variant specified in the course project.

The board contains **30 cells arranged in three rows of ten cells**, with a fixed S-shaped traversal order. Each player starts with **7 pieces**, and the first 14 cells are initially occupied alternately by the two players.

Each turn, the player tosses four sticks. Each stick contributes either `0` or `1`, producing the following movement probabilities:

| Step | Probability |
|------|-------------|
| 1 | 4/16 |
| 2 | 6/16 |
| 3 | 4/16 |
| 4 | 1/16 |
| 5 | 1/16 |

A result of four dark sides is treated as **5** steps according to the project rules.

The game contains several special cells, including:

- **Rebirth**
- **Happiness**
- **Water**
- **Three Truths**
- **Re-Atoum**
- **Horus**

The detailed movement and special-cell rules are implemented in `Rules`.

---

## Project Architecture

The project separates the game representation, game rules, execution flow, user interface, and AI search.

```text
                    ┌───────────────┐
                    │     Game      │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  ConsoleUI    │
                    └───────────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       ┌──────────────┐            ┌────────────────┐
       │    Rules     │◄───────────│  Exminimax AI  │
       └──────┬───────┘            └───────┬────────┘
              │                            │
              ▼                            ▼
       ┌──────────────┐             ┌───────────────┐
       │    State     │             │   MoveNode    │
       └──────┬───────┘             └───────┬───────┘
              │                             │
              ▼                             ▼
       ┌──────────────┐             ┌───────────────┐
       │     Grid     │             │  ChanceNode   │
       └──────────────┘             └───────────────┘
```

### Main Classes

#### `Grid`
Represents the board and the positions of the pieces. It is immutable: board modifications produce a new `Grid` instead of modifying the original one.

#### `State`
Represents a snapshot of the game containing:

- the current `Grid`
- the player whose turn it is
- the current stick-toss value

It is also immutable and provides `copy_with()` for creating modified states.

#### `Rules`
Contains the stateless game logic, including:

- legal move generation
- move application
- successor generation
- special-cell handling
- rebirth operations
- terminal-state and winner detection
- stick-toss probabilities

#### `Game`
Controls the main game loop and the sequence of turns. It is independent from the details of the game rules.

#### `ConsoleUI`
Handles console input and output, including board display, player interaction, and debug information.

#### `Exminimax`
Implements the Expectiminimax search used by the AI.

#### `MoveNode`
Represents a Max/Min decision node in the search tree and stores the selected move, its value, and its Chance-node children.

#### `ChanceNode`
Represents a probabilistic node caused by a stick toss and stores the resulting expected value and its Move-node children.

### Enums

- `Player` – represents the two players.
- `CellType` – represents normal and special board cells.
- `Mode` – represents the available game modes / AI depth levels.

---

## Expectiminimax

The AI uses **Expectiminimax** because the outcome of a turn depends on a random stick toss.

The search alternates between:

```text
Move Node
   │
   ▼
Chance Node
   │
   ▼
Move Node
   │
   ▼
Chance Node
   │
   ▼
  ...
```

### Move nodes

A Move node represents a decision by a player:

- `MAX` when the current player is the AI's root player
- `MIN` when the current player is the opponent

The node selects the maximum or minimum child value accordingly.

### Chance nodes

A Chance node represents the four-stick toss. Every possible step value is considered using its probability, and the expected value is calculated as:

```text
Expected Value = Σ (Probability × Child Value)
```

This allows the AI to reason about future uncertainty instead of treating the random toss as an adversarial decision.

---

## Evaluation Function

The current evaluation function combines several strategic considerations observed during gameplay.

It primarily uses:

- squared piece positions to reward advancement
- a large bonus for pieces that have already left the board
- subtraction of the opponent's evaluation from the AI player's evaluation
- special handling for positions near the Happiness cell

The evaluation is intentionally heuristic rather than a complete mathematical model of every strategic aspect of Senet.

---

## Search Optimizations

### Caching

The implementation uses separate caches for:

- Move / Minimax nodes
- Chance / Expectation nodes

The cache keys include the information required to distinguish states at the corresponding search stage, such as the board, current player, step value when relevant, depth, and root player.

### Immutable States

`Grid` and `State` are immutable, which allows different branches of the search tree to be explored safely without modifying previously generated states. This also makes them suitable for use in cache keys.

### Move Ordering

The project structure also allows legal moves to be ordered before search expansion, although the current version may rely primarily on the search, caching, and heuristic evaluation for decision making.

---

## Debug Mode

The program can expose additional information about the AI search, including:

- number of visited nodes
- evaluation value of the selected decision
- the selected move
- the search tree represented through `MoveNode` and `ChanceNode`

This mode is intended to make the decision process of Expectiminimax inspectable during gameplay.

---

## Running the Project

Make sure Python 3 is installed.

Install the console-color dependency used by the UI:

```bash
pip install colorama
```

Then run the project's main entry point, for example:

```bash
python main.py
```

> Replace `main.py` with the actual entry-point filename if your project uses a different one.

---

## Example Search Depths

The AI supports four search depths:

| Depth | Description |
|------:|-------------|
| 1 | Considers one future player move |
| 2 | Considers two future player moves |
| 3 | Considers three future player moves |
| 4 | Considers four future player moves |

The project treats depth as the number of **player moves** considered, while Chance nodes for the stick toss do not consume a player-move depth level.

---

## Results

A self-play experiment was performed in which every search depth played against the other depths 16 times, with player colors alternated between games.

| Search Depth | Wins |
|-------------:|-----:|
| 1 | 20 |
| 2 | 31 |
| 3 | 24 |
| 4 | 21 |

Depth 2 produced the highest number of wins in this experiment. This does not imply that a deeper search is inherently weaker; the result is affected by the current heuristic evaluation, the stochastic nature of the game, and the interaction between search depth and that evaluation function.

A small number of manual games against different AI depths also produced close results, with the final difference often being approximately one piece.

---

## Course Context

This project was developed for the **Intelligent Search Algorithms** practical course at the Faculty of Informatics Engineering, Damascus University. The project specification requires modeling Senet as a search problem, implementing the game logic, using Expectiminimax, and providing search-analysis output.

---

## Project Structure

A possible organization is:

```text
project/
├── main.py
├── grid.py
├── state.py
├── rules.py
├── game.py
├── console_ui.py
├── exminimax.py
├── move_node.py
├── chance_node.py
├── player.py
├── cell_type.py
├── mode.py
└── README.md
```

The exact filenames may differ from the final implementation.

---

## Authors

Khaled Tello

Information Technology Engineering Student — Damascus University
