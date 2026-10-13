"""
Rock · Paper · Scissors — FastAPI Backend
=========================================
Run locally:
    uvicorn app.main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

from app.game import (
    CHOICES,
    EMOJI,
    Choice,
    determine_outcome,
    describe_outcome,
    get_computer_choice,
)

# ── App setup ──────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Rock · Paper · Scissors API",
    description="Play Rock Paper Scissors against the computer via REST.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Schemas ───────────────────────────────────────────────────────────────────
class PlayRequest(BaseModel):
    player_choice: str

    @field_validator("player_choice")
    @classmethod
    def validate_choice(cls, v: str) -> str:
        v = v.strip().lower()
        if v not in CHOICES:
            raise ValueError(f"Choice must be one of {CHOICES}")
        return v


class PlayResponse(BaseModel):
    player_choice:   str
    computer_choice: str
    outcome:         str   # "win" | "lose" | "tie"
    message:         str
    player_emoji:    str
    computer_emoji:  str
    outcome_emoji:   str


class HealthResponse(BaseModel):
    status: str
    choices: list[str]


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/health", response_model=HealthResponse, tags=["meta"])
def health() -> HealthResponse:
    """Service health check."""
    return HealthResponse(status="ok", choices=CHOICES)


@app.post("/play", response_model=PlayResponse, tags=["game"])
def play(body: PlayRequest) -> PlayResponse:
    """
    Play one round.

    - **player_choice**: `rock`, `paper`, or `scissors`
    """
    player: Choice   = body.player_choice          # type: ignore[assignment]
    computer: Choice = get_computer_choice()
    outcome          = determine_outcome(player, computer)
    message          = describe_outcome(player, computer, outcome)

    return PlayResponse(
        player_choice=player,
        computer_choice=computer,
        outcome=outcome,
        message=message,
        player_emoji=EMOJI[player],
        computer_emoji=EMOJI[computer],
        outcome_emoji=EMOJI[outcome],
    )
