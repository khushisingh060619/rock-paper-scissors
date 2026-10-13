"""
Unit tests for backend/app/game.py
Run with:  pytest tests/ -v
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.game import (
    get_computer_choice,
    determine_outcome,
    describe_outcome,
    CHOICES,
    BEATS,
)


# ── get_computer_choice ───────────────────────────────────────────────────────

class TestGetComputerChoice:
    def test_returns_valid_choice(self):
        for _ in range(30):
            assert get_computer_choice() in CHOICES

    def test_all_options_eventually_chosen(self):
        results = {get_computer_choice() for _ in range(200)}
        assert results == set(CHOICES)


# ── determine_outcome ─────────────────────────────────────────────────────────

class TestDetermineOutcome:

    @pytest.mark.parametrize("choice", CHOICES)
    def test_tie_same_choice(self, choice):
        assert determine_outcome(choice, choice) == "tie"

    def test_rock_beats_scissors(self):
        assert determine_outcome("rock", "scissors") == "win"

    def test_scissors_beats_paper(self):
        assert determine_outcome("scissors", "paper") == "win"

    def test_paper_beats_rock(self):
        assert determine_outcome("paper", "rock") == "win"

    def test_scissors_loses_to_rock(self):
        assert determine_outcome("scissors", "rock") == "lose"

    def test_paper_loses_to_scissors(self):
        assert determine_outcome("paper", "scissors") == "lose"

    def test_rock_loses_to_paper(self):
        assert determine_outcome("rock", "paper") == "lose"

    @pytest.mark.parametrize("player,computer,expected", [
        ("rock",     "rock",     "tie"),
        ("rock",     "paper",    "lose"),
        ("rock",     "scissors", "win"),
        ("paper",    "rock",     "win"),
        ("paper",    "paper",    "tie"),
        ("paper",    "scissors", "lose"),
        ("scissors", "rock",     "lose"),
        ("scissors", "paper",    "win"),
        ("scissors", "scissors", "tie"),
    ])
    def test_all_combinations(self, player, computer, expected):
        assert determine_outcome(player, computer) == expected


# ── BEATS dict consistency ────────────────────────────────────────────────────

class TestBeatsDict:
    def test_every_choice_has_a_victim(self):
        for choice in CHOICES:
            assert choice in BEATS
            assert BEATS[choice] in CHOICES

    def test_no_choice_beats_itself(self):
        for choice in CHOICES:
            assert BEATS[choice] != choice

    def test_cyclic_dominance(self):
        assert BEATS["rock"]     == "scissors"
        assert BEATS["scissors"] == "paper"
        assert BEATS["paper"]    == "rock"

    def test_exactly_three_entries(self):
        assert len(BEATS) == 3


# ── describe_outcome ──────────────────────────────────────────────────────────

class TestDescribeOutcome:
    def test_win_message(self):
        msg = describe_outcome("rock", "scissors", "win")
        assert "win" in msg.lower()

    def test_lose_message(self):
        msg = describe_outcome("rock", "paper", "lose")
        assert "lose" in msg.lower()

    def test_tie_message(self):
        msg = describe_outcome("rock", "rock", "tie")
        assert "tie" in msg.lower()
