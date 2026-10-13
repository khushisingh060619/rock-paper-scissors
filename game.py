"""
Core Rock · Paper · Scissors game logic.
Pure functions — no I/O, easily testable.
"""

import random
from typing import Literal

# ── Types ──────────────────────────────────────────────────────────────────────
Choice  = Literal["rock", "paper", "scissors"]
Outcome = Literal["win", "lose", "tie"]

# ── Constants ──────────────────────────────────────────────────────────────────
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


def get_computer_choice() -> Choice:
    """Return a random choice for the computer."""
    return random.choice(CHOICES)


def determine_outcome(player: Choice, computer: Choice) -> Outcome:
    """Return 'win', 'lose', or 'tie' from the player's perspective."""
    if player == computer:
        return "tie"
    if BEATS[player] == computer:
        return "win"
    return "lose"


def describe_outcome(player: Choice, computer: Choice, outcome: Outcome) -> str:
    """Return a human-readable one-line description of the round result."""
    if outcome == "tie":
        return "It's a tie!"
    if outcome == "win":
        return f"{BEATS[player].capitalize()} loses to {player.capitalize()} — You win!"
    return f"{player.capitalize()} loses to {computer.capitalize()} — You lose!"
