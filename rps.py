"""
Rock · Paper · Scissors
========================
A terminal-based game with score tracking, streaks, and replay support.
Pure Python standard library — no external dependencies.
"""

import random
import sys
import os
from typing import Literal

# ── Types ─────────────────────────────────────────────────────────────────────
Choice  = Literal["rock", "paper", "scissors"]
Outcome = Literal["win", "lose", "tie"]

# ── Constants ─────────────────────────────────────────────────────────────────
CHOICES: list[Choice] = ["rock", "paper", "scissors"]

BEATS: dict[Choice, Choice] = {
    "rock":     "scissors",
    "scissors": "paper",
    "paper":    "rock",
}

EMOJI: dict[str, str] = {
    "rock":     "🪨",
    "paper":    "📄",
    "scissors": "✂️",
    "win":      "🏆",
    "lose":     "💀",
    "tie":      "🤝",
}

BANNER = r"""
 ____  ____  ____  _  _     ____  __   ____  ____  ____
(  _ \(  _ \/ ___)( )/ )   (  _ \/ _\ (  _ \(  __)(  _ \
 )   / ) __/\___ \ )  (     ) __//    \ ) __/ ) _)  )   /
(__\_)(__)  (____/(_)\_)   (__)  \_/\_/(__)  (____)(__\_)
  ____  ____  ____  ____  __  __  ____  ____  ____  ____
 / ___)/ ___)(  _ \/ ___)(  )(  )/ ___)/ ___)(  __)(  _ \
 \___ \\___ \ )   /\___ \ )( )( (\___ \\___ \ ) _)  )   /
 (____/(____/(__\_)(____/(__)(__)  (____/(____/(____)(__\_)
"""


# ── Core game logic ───────────────────────────────────────────────────────────

def get_computer_choice() -> Choice:
    return random.choice(CHOICES)


def determine_outcome(player: Choice, computer: Choice) -> Outcome:
    if player == computer:
        return "tie"
    if BEATS[player] == computer:
        return "win"
    return "lose"


# ── Display helpers ───────────────────────────────────────────────────────────

def clear_screen() -> None:
    os.system("cls" if sys.platform == "win32" else "clear")


def separator(char: str = "─", width: int = 52) -> str:
    return char * width


def print_header() -> None:
    print(BANNER)
    print(separator("═"))
    print("  Best of any number of rounds — type 'q' to quit")
    print(separator("═"))


def print_scoreboard(scores: dict[str, int], rounds: int, streak: int, streak_owner: str) -> None:
    w, d, l = scores["player"], scores["tie"], scores["computer"]
    print(f"\n  Round {rounds}  |  You {w}  –  Ties {d}  –  CPU {l}")
    if streak >= 2:
        owner = "Your" if streak_owner == "player" else "CPU's"
        print(f"  🔥 {owner} {streak}-round streak!")
    print(separator())


def print_round_result(player: Choice, computer: Choice, outcome: Outcome) -> None:
    p_em = EMOJI[player]
    c_em = EMOJI[computer]
    o_em = EMOJI[outcome]

    print(f"\n  You chose   : {p_em}  {player.capitalize()}")
    print(f"  CPU chose   : {c_em}  {computer.capitalize()}")
    print()

    if outcome == "win":
        print(f"  {o_em}  {BEATS[player].capitalize()} loses to {player.capitalize()} — YOU WIN!")
    elif outcome == "lose":
        print(f"  {o_em}  {player.capitalize()} loses to {computer.capitalize()} — YOU LOSE!")
    else:
        print(f"  {o_em}  It's a TIE!")


def print_final_summary(scores: dict[str, int], rounds: int) -> None:
    w, d, l = scores["player"], scores["tie"], scores["computer"]
    print("\n" + separator("═"))
    print("  GAME OVER — Final Summary")
    print(separator("═"))
    print(f"  Rounds played : {rounds}")
    print(f"  You won       : {w}")
    print(f"  CPU won       : {l}")
    print(f"  Ties          : {d}")
    print()
    if w > l:
        pct = round(w / rounds * 100)
        print(f"  🏆  You win the series! ({pct}% win rate)")
    elif l > w:
        pct = round(l / rounds * 100)
        print(f"  💻  CPU wins the series! (Your win rate: {round(w/rounds*100)}%)")
    else:
        print("  🤝  The series is tied!")
    print(separator("═") + "\n")


# ── Input helpers ─────────────────────────────────────────────────────────────

def prompt_choice() -> Choice | None:
    mapping = {
        "r": "rock",    "1": "rock",    "rock":     "rock",
        "p": "paper",   "2": "paper",   "paper":    "paper",
        "s": "scissors","3": "scissors","scissors": "scissors",
    }
    print("\n  Choose your weapon:")
    print("  [1] 🪨  Rock      [2] 📄  Paper      [3] ✂️  Scissors")
    print("  (or type 'q' to quit)\n")

    while True:
        raw = input("  Your choice: ").strip().lower()
        if raw in ("q", "quit", "exit"):
            return None
        if raw in mapping:
            return mapping[raw]  # type: ignore[return-value]
        print("  ⚠  Invalid input. Enter rock/paper/scissors, r/p/s, or 1/2/3.")


def prompt_play_again() -> bool:
    while True:
        ans = input("\n  Play again? [Y/n]: ").strip().lower()
        if ans in ("", "y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("  ⚠  Please enter 'y' or 'n'.")


# ── Main game loop ────────────────────────────────────────────────────────────

def play() -> None:
    clear_screen()
    print_header()

    scores: dict[str, int] = {"player": 0, "computer": 0, "tie": 0}
    rounds     = 0
    streak     = 0
    streak_owner = ""

    while True:
        print_scoreboard(scores, rounds, streak, streak_owner)

        player = prompt_choice()
        if player is None:
            break

        computer = get_computer_choice()
        outcome  = determine_outcome(player, computer)
        rounds  += 1

        if outcome == "win":
            scores["player"] += 1
            streak = streak + 1 if streak_owner == "player" else 1
            streak_owner = "player"
        elif outcome == "lose":
            scores["computer"] += 1
            streak = streak + 1 if streak_owner == "computer" else 1
            streak_owner = "computer"
        else:
            scores["tie"] += 1
            streak = 0
            streak_owner = ""

        print_round_result(player, computer, outcome)

        if not prompt_play_again():
            break

    if rounds:
        print_final_summary(scores, rounds)
    else:
        print("\n  No rounds played. Goodbye! 👋\n")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        play()
    except KeyboardInterrupt:
        print("\n\n  Interrupted. Goodbye! 👋\n")
        sys.exit(0)
