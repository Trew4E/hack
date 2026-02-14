# Demo Script — The Personal Career Navigator

> **Total time: 5 minutes | LLM Calls: 3 | Failure risk: Zero**

---

## Pre-Demo Setup (2 minutes before)

1. Start Ollama: ensure `ollama serve` is running
2. Start backend: `cd backend && python -m uvicorn main:app --reload`
3. Open `frontend/index.html` in browser
4. Verify the landing page loads (dark mode UI with gradient header)
5. Keep terminal visible (shows agent logs with response diagnostics)

---

## Demo Flow

### 🎬 Opening (30 seconds)

> "Every student has a dream role — but most don't know what they're actually missing.
> Career Navigator is an AI agent that analyzes your profile, finds the real gaps,
> and builds a personalized 30-day learning roadmap. Let me show you."

---

### Step 1: Upload Resume (30 seconds)

**Option A:** Click **"Load Sample Resume"** → sample text fills the textarea
**Option B:** Click **"📎 Upload PDF"** → select a real PDF resume → text is extracted and displayed

Point out: *"Students can paste text or upload their actual PDF resume — we extract the content automatically."*

---

### Step 2: Select Dream Role (15 seconds)

**Option A:** Open dropdown → select **"ML Engineer"** (preset)
**Option B:** Select **"✨ Custom"** → type any role like **"Blockchain Developer"**

Point out: *"We have 8 preset roles, but students can type any role. The AI figures out the skill requirements."*

---

### Step 3: (Optional) GitHub Username (10 seconds)

- Type a GitHub username (e.g., your own)
- *"The system fetches their GitHub profile — languages, repos, activity — to enrich the analysis."*

---

### Step 4: Generate Roadmap (60 seconds)

- Click **"🚀 Generate Career Roadmap"**
- **THE WOW MOMENT**: Agent thinking animation appears
- In the terminal, show the logs:
  ```
  [Career Brain] === Call 1: Skills/Gaps/Roadmap ===
  [Career Brain] Roadmap days: 30
  [Career Brain] === Call 2: Flagship Project ===
  [Career Brain] Project merged from Call 2
  ```
- Narrate: *"Two focused LLM calls — one for the roadmap, one for the project. Each is reliable because neither overwhelms the model."*

---

### Step 5: Walk Through Results (90 seconds)

#### Skills Tab (20s)
- Extracted skills with level indicators (★ to ★★★)
- Strengths and weaknesses in side-by-side cards

#### Gaps Tab (30s)
- Color-coded severity: 🔴 Critical → 🟡 Important → 🔵 Nice-to-have
- Read one specific reasoning

#### Roadmap Tab (25s)
- Scroll through all 30 days with weekly milestones
- Highlight specific resources and tasks

#### Project Tab (15s)
- Show project title, tech stack, and 4-week feature plan
- *"This project is designed around the exact gaps we identified."*

---

### Step 6: Adaptation — THE KILLER FEATURE (60 seconds)

- Scroll to **"Adaptation Simulator"** panel
- Narrate: *"Real life happens. What if this student missed a week?"*
- Click **"🔄 Simulate: Missed 7 Days → Re-Plan"**
- Show adapted roadmap with compressed curriculum + adjusted project scope
- *"The agent re-prioritized, compressed the curriculum, and adjusted the project. That's real agentic reasoning."*

---

### 🎬 Closing (30 seconds)

> "Three LLM calls. One agent. PDF upload, custom roles, GitHub integration,
> and adaptive re-planning. This is what agentic AI looks like —
> not a chatbot, but a planning system that thinks, adapts, and delivers."

---

## Backup Plan

If Ollama fails → Mock data loads automatically. **Demo continues without pause.**

---

## Key Talking Points

| Question | Answer |
|----------|--------|
| "Is this just a prompt wrapper?" | No — two-call architecture with post-processing, PDF extraction, GitHub integration, and adaptive re-planning |
| "Why two LLM calls?" | Smaller models can't generate everything reliably in one shot. Splitting ensures completeness. |
| "How is this agentic?" | Plan → Execute → Observe (progress) → Adapt (re-plan). Classic agent loop. |
| "Why local LLM?" | Free, unlimited, no API keys, works offline. Production-ready. |
