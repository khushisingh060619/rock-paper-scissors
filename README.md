# ✂️ Rock · Paper · Scissors

A full-stack Rock Paper Scissors game featuring a **FastAPI backend**, a **neon-arcade web frontend**, and the original **CLI game** — all in one repository.

---

## Project Structure

```
rock-paper-scissors/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application & REST routes
│   │   └── game.py          # Core game logic (pure functions)
│   ├── tests/
│   │   └── test_game.py     # Pytest test suite (21 tests)
│   ├── requirements.txt     # Production dependencies
│   └── requirements-dev.txt # Dev / test dependencies
├── frontend/
│   └── index.html           # Single-file web app (no build step)
├── rps.py                   # Original terminal game (zero dependencies)
├── .gitignore
├── LICENSE
└── README.md
```

---

## Quick Start

### Option A — Terminal (no server needed)

```bash
python rps.py
```

Requires Python 3.10+. No pip installs needed.

---

### Option B — Full-stack web app

#### 1. Start the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API is now live at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

#### 2. Open the frontend

Simply open `frontend/index.html` in any browser. No build step, no Node.js.

> **Tip:** Make sure the API URL field in the top of the page matches where your backend is running (default: `http://localhost:8000`).

---

## REST API

| Method | Endpoint  | Description               |
|--------|-----------|---------------------------|
| GET    | `/health` | Service health check      |
| POST   | `/play`   | Play one round            |

### POST `/play`

**Request body:**
```json
{ "player_choice": "rock" }
```

Accepted values: `rock`, `paper`, `scissors`

**Response:**
```json
{
  "player_choice":   "rock",
  "computer_choice": "scissors",
  "outcome":         "win",
  "message":         "Scissors loses to Rock — You win!",
  "player_emoji":    "🪨",
  "computer_emoji":  "✂️",
  "outcome_emoji":   "🏆"
}
```

---

## Running Tests

```bash
cd backend
pip install -r requirements-dev.txt
pytest tests/ -v
```

Expected output:

```
tests/test_game.py::TestGetComputerChoice::test_returns_valid_choice        PASSED
tests/test_game.py::TestGetComputerChoice::test_all_options_eventually_chosen PASSED
tests/test_game.py::TestDetermineOutcome::test_tie_same_choice[rock]        PASSED
...
tests/test_game.py::TestDescribeOutcome::test_tie_message                   PASSED

================ 21 passed in 0.10s ================
```

---

## Frontend Features

| Feature | Detail |
|---|---|
| Live score tracking | Wins, losses, ties updated after every round |
| Streak detection | 🔥 Highlights consecutive wins |
| Round history log | Scrollable log of every played round |
| Keyboard shortcuts | Press **R**, **P**, or **S** to pick instantly |
| API status indicator | Shows live connection state to the backend |
| Zero build step | Plain HTML/CSS/JS — open directly in browser |

---

## Game Rules

| Player | Beats |
|---|---|
| 🪨 Rock | ✂️ Scissors |
| ✂️ Scissors | 📄 Paper |
| 📄 Paper | 🪨 Rock |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, FastAPI, Uvicorn, Pydantic v2 |
| Frontend | HTML5, CSS3, Vanilla JS (ES2022) |
| CLI | Pure Python standard library |
| Tests | Pytest |

---

## License

MIT License — free to use, modify, and distribute.
