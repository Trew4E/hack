# The Personal Career Navigator

> **One agent. Two LLM calls. A complete career planning system.**

An AI-powered career co-pilot that analyzes a student's profile, identifies skill gaps against their dream role, generates a personalized 30-day learning roadmap with a flagship project, and adapts it in real-time when life happens.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.ai) (runs locally, free & unlimited)

### Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Pull the local model (one-time ~4.7GB download)
ollama pull mistral:7b

# Start the server
python -m uvicorn main:app --reload --port 8000
```

### Frontend
No build step needed! Just open in your browser:
```
frontend/index.html
```

---

## 🧠 How It Works

```
Resume (text or PDF) + Dream Role  →  Career Brain Agent

  Call 1: Skills + Gaps + 30-Day Roadmap
  Call 2: Flagship Project (uses gaps from Call 1)

  Optional: GitHub profile enrichment

Progress Update  →  Adaptation Call  →  Re-planned Roadmap
```

**LLM Fallback Chain:**
1. **Ollama** (local, free) — `mistral:7b` on GPU
2. **Mock data** (pre-built responses) — demo never crashes

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **PDF Resume Upload** | Upload a PDF resume — text is extracted automatically |
| **Custom Roles** | Type any dream role, not limited to presets |
| **GitHub Integration** | Optional GitHub username enriches the analysis with real coding data |
| **Two-Call Architecture** | Splits generation for reliable output from smaller models |
| **Post-Processing** | Backend fills missing fields so results are always complete |
| **Adaptive Re-Planning** | Simulate missed days — AI re-plans the remaining roadmap |

---

## 📂 Project Structure

```
hack/
├── backend/
│   ├── main.py              # FastAPI app, endpoints + post-processing
│   ├── gemini_service.py    # Ollama LLM integration + fallback
│   ├── prompts.py           # 3 prompt templates (roadmap, project, adapt)
│   ├── models.py            # Pydantic request/response schemas
│   ├── pdf_service.py       # PDF text extraction (PyPDF2)
│   ├── github_service.py    # GitHub API integration + caching
│   ├── mock_data.py         # Pre-built demo fallback data
│   ├── requirements.txt
│   ├── .env.example
│   ├── tests/
│   │   └── test_github_service.py
│   └── data/
│       ├── roles.json       # 8 pre-defined dream roles
│       └── sample_resume.txt
├── frontend/
│   └── index.html           # Single-file UI (HTML + CSS + JS)
├── ARCHITECTURE.md
├── DEMO_SCRIPT.md
└── README.md
```

---

## 🏗 Tech Stack

| Layer | Tool | Why |
|-------|------|-----|
| LLM | Ollama + Mistral 7B (local) | Free, unlimited, no API key needed |
| Backend | FastAPI | Async, auto-docs, Pydantic validation |
| PDF Parsing | PyPDF2 | Extract text from uploaded resumes |
| GitHub API | REST + caching | Optional profile enrichment |
| Frontend | Single HTML file | Zero dependencies, no build step |
| Styling | Vanilla CSS | Dark mode, glassmorphism |

---

## ⚙️ Configuration

Set environment variables in `backend/.env`:
```bash
# Optional: Change Ollama model (default: mistral:7b)
OLLAMA_MODEL=mistral:7b

# Optional: GitHub token for higher API rate limits
GITHUB_TOKEN=ghp_your_token_here
```

---

## 🎯 Demo Flow (5 minutes)

1. Paste resume text **or upload a PDF**
2. Select a dream role **or type a custom one**
3. Optionally enter a GitHub username
4. Click generate → animated agent reasoning steps
5. Results: Skills → Gaps → 30-day Roadmap → Flagship Project
6. Click "Simulate: Missed 7 Days" → AI re-plans in real-time

---

## 📄 License

MIT — Built for hackathon demonstration.
