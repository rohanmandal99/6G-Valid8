# 6G-Valid8
AI-driven validation and CI/CD framework for wireless system testing.

## Structure
- backend/ : FastAPI server, log parsers, AI triage modules
- contributing.md: How to contribute
- docs/ : project notes and references
- frontend/ : (planned to be added later)

## Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/rohanmandal99/6G-Valid8.git
   cd 6G-Valid8

2. **Create and activate a virtual environment**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate

3. **Install dependencies**
    ```bash
    pip install -r backend/requirements.txt

4. **Run the backend**
    ```bash
    uvicorn backend.main:app --reload
