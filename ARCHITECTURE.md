# Architecture — The Personal Career Navigator

> System design covering all 10 required sections.

---

## 1. User Skill Map

Extracts and structures skills from resume text using Ollama (local LLM).

| Field | Type | Example |
|-------|------|---------|
| `skills[].name` | string | "Python" |
| `skills[].level` | enum | beginner / intermediate / advanced |
| `skills[].category` | enum | technical / soft / tool |
| `strengths` | string[] | "Solid Python foundation" |
| `weaknesses` | string[] | "No ML/DL project experience" |

**Input sources:** Pasted text, uploaded PDF (PyPDF2 extraction), or sample resume.

---

## 2. Dream Role Requirement Graph

Each role is decomposed into 6 categories:

```
Dream Role (e.g., ML Engineer)
├── Core Technical: PyTorch, Scikit-learn
├── Supporting Skills: SQL, Docker, Git
├── Theory/Math: Linear algebra, Probability
├── Industry Tools: Jupyter, MLflow, Pandas
├── Soft Skills: Problem decomposition, Technical writing
└── Portfolio Expectations: E2E ML project, Deployed model
```

**Source:** `data/roles.json` (8 pre-defined roles) + **custom role support** where the LLM infers requirements for any role typed by the user.

---

## 3. Skill Gap Analysis

| Severity | Color | Meaning |
|----------|-------|---------|
| **Critical** | 🔴 Red | Blocks entry to the role |
| **Important** | 🟡 Amber | Weakens candidacy significantly |
| **Nice-to-have** | 🔵 Cyan | Strengthens profile but not blocking |

Each gap includes a `reason` with specific, honest reasoning.

---

## 4. 30-Day Adaptive Roadmap

**Day-by-day plan with 4 fields per day:**

| Field | Purpose |
|-------|---------|
| `day` | Day number (1-30) |
| `objective` | What the student will learn |
| `resource` | Specific course, tutorial, or documentation |
| `task` | Hands-on exercise or build step |
| `hours` | Time estimate |

**Weekly milestones** group days into 4 phases with skills gained.

**Post-processing** ensures exactly 30 days and 4 weekly milestones, padding with sensible defaults if the LLM truncates.

---

## 5. Flagship Project Plan

Generated in a **separate LLM call** using gap analysis data from Call 1:

- Uses the student's existing skills + identified gaps to design a relevant project
- 4-week feature plan with progressive complexity
- Portfolio-quality: solves a real problem, uses role-relevant tech

---

## 6. Agent Architecture

### Two-Call Career Brain Agent

```
┌──────────────────────────────────────────────────┐
│              Career Brain Agent                  │
│                                                  │
│  Input Layer                                     │
│  ├── Resume parser (text paste or PDF upload)    │
│  ├── GitHub profile enrichment (optional)        │
│  ├── Role context loader (roles.json or custom)  │
│  └── Prompt builder (2 focused prompts)          │
│                                                  │
│  LLM Layer (two sequential calls)                │
│  ├── Call 1: Skills + Gaps + 30-Day Roadmap      │
│  ├── Call 2: Flagship Project (from gap data)    │
│  └── Fallback: Mock data (demo safety)           │
│                                                  │
│  Post-Processing Layer                           │
│  ├── Key normalization (project → flagship_project) │
│  ├── Field padding (ensure 30 days, 4 weeks)     │
│  ├── Sub-key aliasing (name → title, etc.)       │
│  └── Default generation for any missing sections │
│                                                  │
│  Output Layer                                    │
│  ├── Pydantic validation                         │
│  ├── In-memory state storage                     │
│  └── JSON response to frontend                   │
└──────────────────────────────────────────────────┘
```

### Why Two Calls?

Mistral 7B cannot reliably generate all sections (skills + gaps + 30 days + project) in a single output. Splitting into two focused calls ensures each completes within the model's token budget:

| Call | Output | ~Tokens |
|------|--------|---------|
| Call 1 | reasoning, skill_map, role_requirements, gap_analysis, roadmap (30 days) | ~8-9K chars |
| Call 2 | flagship_project (title, tech_stack, weekly_features) | ~1-2K chars |

### Agent Loops

**Planning Loop** (Call 1 + Call 2):
```
Resume + Role context → Prompt 1 → Skills/Gaps/Roadmap
→ Extract skills & gaps → Prompt 2 → Flagship Project
→ Post-process → Merge → Return to frontend
```

**Adaptation Loop** (single call):
```
Progress update → Compare to original plan → Compress curriculum
→ Adjust project scope → Generate motivation → Return
```

### Tech Stack

| Component | Tool | Reason |
|-----------|------|--------|
| LLM | Ollama + Mistral 7B (local) | Free, unlimited, no API key |
| Backend | FastAPI (Python) | Async, auto-docs, Pydantic |
| PDF Parsing | PyPDF2 | Extract text from uploaded resumes |
| GitHub API | REST + 10min caching | Optional profile enrichment |
| Frontend | Single HTML file | Zero dependencies |
| Styling | Vanilla CSS | Dark mode, glassmorphism |
| State | Python dict (in-memory) | Hackathon simplicity |

---

## 7. Datasets & Training Sources

| Dataset | Type | Usage |
|---------|------|-------|
| `data/roles.json` | Hand-crafted | 8 dream roles with structured skill requirements |
| `data/sample_resume.txt` | Hand-crafted | Demo resume (CS student profile) |
| `mock_data.py` | Hand-crafted | Full fallback responses for demo safety |

**Custom roles** bypass `roles.json` — the LLM infers requirements based on its training data.

---

## 8. Evaluation Metrics

| Metric | How to Measure | Target |
|--------|---------------|--------|
| **Skill gap accuracy** | Expert review of identified gaps | >85% valid |
| **Roadmap usefulness** | Would a student follow this plan? | 4+/5 rating |
| **Completion likelihood** | Daily tasks realistically scoped? | <4 hours/day |
| **Adaptation quality** | Re-planning handles missed days? | Critical gaps still covered |
| **Output reliability** | All fields populated after post-processing? | 100% |

---

## 9. Demo Flow

> Full script in [DEMO_SCRIPT.md](DEMO_SCRIPT.md)

| Time | Action | Impact |
|------|--------|--------|
| 0:00 | Opening pitch | Sets the story |
| 0:30 | Upload PDF or load sample resume | Shows flexible input |
| 1:00 | Select role or type custom | Shows versatility |
| 1:15 | Generate → animated reasoning | **Wow moment #1** |
| 2:15 | Walk through all 4 tabs | Shows depth |
| 3:45 | Simulate missed 7 days → AI re-plans | **Wow moment #2** |
| 4:45 | Closing pitch | Land the story |

---

## 10. Code Scaffold

### Key Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `main.py` | FastAPI endpoints, post-processing, state management |
| `gemini_service.py` | Ollama LLM calls with fallback |
| `prompts.py` | 3 prompt templates (roadmap, project, adapt) |
| `pdf_service.py` | PDF → text extraction via PyPDF2 |
| `github_service.py` | GitHub API with validation, caching, sanitization |
| `models.py` | Pydantic schemas with flexible defaults |
| `mock_data.py` | Pre-built demo fallback responses |

### Endpoint Map

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/roles` | List available dream roles |
| GET | `/sample-resume` | Load demo resume text |
| POST | `/upload-resume` | Extract text from PDF upload |
| POST | `/generate-roadmap` | Generate full career analysis (2 LLM calls) |
| POST | `/adapt-roadmap` | Re-plan after progress update |
