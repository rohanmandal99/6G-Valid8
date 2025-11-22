# 6G-Valid8
AI-assisted Wireless Validation Tool for 5G/6G Systems.

## Structure
- backend/ : FastAPI server, log parsers, AI triage modules
- contributing.md : How to contribute
- docs/ : project notes and references
- frontend/ : React-based UI

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
   pip install -r requirements.txt

4. **Run the backend**
   ```bash
   uvicorn backend.main:app --reload

5. **Ollama Setup**
   ```bash
   ollama pull llama3.2:3b  
   ollama serve 
   
6.  **Frontend Setup**
   ```bash
   cd frontend
   npm install 
   npm run dev 
    

