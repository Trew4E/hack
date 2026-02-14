"""
The Personal Career Navigator — FastAPI Backend
Single "Career Brain" agent with 2 endpoints.
"""
import json
import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from models import RoadmapRequest, AdaptRequest, RoadmapResponse, AdaptResponse
from llm_service import call_llm
from prompts import build_roadmap_prompt, build_project_prompt, build_adapt_prompt
from mock_data import MOCK_ROADMAP_RESPONSE, MOCK_ADAPT_RESPONSE
from github_service import fetch_github_profile, format_github_context
from pdf_service import extract_text_from_pdf


# ── In-memory state ─────────────────────────────────────────────
# Stores the last generated roadmap so /adapt can reference it
state = {
    "last_roadmap": None,
    "last_request": None,
    "roles": {},
}


# ── Load roles on startup ──────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    roles_path = Path(__file__).parent / "data" / "roles.json"
    if roles_path.exists():
        with open(roles_path, "r", encoding="utf-8") as f:
            state["roles"] = json.load(f)
        print(f"[Career Brain] Loaded {len(state['roles'])} roles")
    else:
        print("[Career Brain] WARNING: roles.json not found")
    yield


# ── App setup ───────────────────────────────────────────────────
app = FastAPI(
    title="Career Navigator",
    description="AI Career Co-pilot — Single Agent, Two Calls",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Endpoint: Upload PDF Resume ────────────────────────────────
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Accept a PDF upload, extract text, return it."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    try:
        contents = await file.read()
        text = extract_text_from_pdf(contents)
        return {"resume_text": text}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[Career Brain] PDF upload error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process PDF file.")


# ── Post-process LLM output ────────────────────────────────────
def post_process_roadmap(data: dict, dream_role: str) -> dict:
    """Fill in missing/empty fields so the frontend always gets complete data."""
    if not isinstance(data, dict):
        return data

    # Fix common key mismatches from LLM
    key_aliases = {
        "project": "flagship_project",
        "skills": "skill_map",
        "gaps": "gap_analysis",
        "requirements": "role_requirements",
    }
    for wrong_key, correct_key in key_aliases.items():
        if wrong_key in data and correct_key not in data:
            data[correct_key] = data.pop(wrong_key)
            print(f"[Career Brain] Fixed key: '{wrong_key}' → '{correct_key}'")

    # Ensure reasoning exists
    if not data.get("reasoning"):
        data["reasoning"] = f"Career analysis generated for {dream_role} role based on the provided resume."

    # Ensure skill_map
    if "skill_map" not in data:
        data["skill_map"] = {"skills": [], "strengths": [], "weaknesses": []}

    # Ensure role_requirements
    if "role_requirements" not in data:
        data["role_requirements"] = {
            "core_technical": [], "supporting_skills": [], "theory_math": [],
            "tools": [], "soft_skills": [], "portfolio_expectations": []
        }

    # Ensure gap_analysis
    if "gap_analysis" not in data:
        data["gap_analysis"] = {"critical": [], "important": [], "nice_to_have": []}

    # Ensure roadmap with 30 days
    if "roadmap" not in data:
        data["roadmap"] = {"days": [], "weekly_milestones": []}

    days = data["roadmap"].get("days", [])
    existing_day_nums = {d.get("day", 0) for d in days}
    for d in range(1, 31):
        if d not in existing_day_nums:
            days.append({
                "day": d,
                "objective": f"Self-study: {dream_role} skills (Day {d})",
                "resource": "Online tutorials & documentation",
                "task": "Practice and build portfolio",
                "hours": 2,
            })
    data["roadmap"]["days"] = sorted(days, key=lambda x: x.get("day", 0))

    # Ensure 4 weekly milestones
    milestones = data["roadmap"].get("weekly_milestones", [])
    existing_weeks = {m.get("week", 0) for m in milestones}
    for w in range(1, 5):
        if w not in existing_weeks:
            milestones.append({
                "week": w,
                "milestone": f"Week {w} progress checkpoint",
                "skills_gained": [f"{dream_role} foundations"],
            })
    data["roadmap"]["weekly_milestones"] = sorted(milestones, key=lambda x: x.get("week", 0))[:4]

    # Ensure flagship_project
    if "flagship_project" not in data:
        data["flagship_project"] = {
            "title": f"{dream_role} Portfolio Project",
            "problem_statement": f"Build a project demonstrating {dream_role} skills",
            "tech_stack": [],
            "weekly_features": [],
            "portfolio_quality": "Demonstrates core competencies",
        }

    fp = data["flagship_project"]
    print(f"[Career Brain] Project sub-keys: {list(fp.keys())}")

    # Normalize project sub-keys (LLM often uses short names)
    proj_aliases = {
        "name": "title",
        "project_name": "title",
        "stack": "tech_stack",
        "technologies": "tech_stack",
        "technology": "tech_stack",
        "features": "weekly_features",
        "problem": "problem_statement",
        "description": "problem_statement",
        "quality": "portfolio_quality",
    }
    for wrong, correct in proj_aliases.items():
        if wrong in fp and correct not in fp:
            fp[correct] = fp.pop(wrong)
            print(f"[Career Brain] Fixed project key: '{wrong}' → '{correct}'")

    # Ensure required fields have values
    if not fp.get("title"):
        fp["title"] = f"{dream_role} Portfolio Project"
    if not fp.get("problem_statement"):
        fp["problem_statement"] = f"Build a project demonstrating {dream_role} skills"
    if not fp.get("tech_stack"):
        fp["tech_stack"] = []
    if not fp.get("portfolio_quality"):
        fp["portfolio_quality"] = "Demonstrates core competencies"

    # Ensure 4 weekly_features
    features = data["flagship_project"].get("weekly_features", [])
    existing_fw = {f.get("week", 0) for f in features}
    feature_defaults = ["Core setup & architecture", "Feature development", "Integration & testing", "Polish & deployment"]
    for w in range(1, 5):
        if w not in existing_fw:
            features.append({
                "week": w,
                "feature": feature_defaults[w - 1],
                "description": f"Week {w}: {feature_defaults[w - 1]}",
            })
        else:
            # Fill empty feature/description
            for f in features:
                if f.get("week") == w:
                    if not f.get("feature"):
                        f["feature"] = feature_defaults[w - 1]
                    if not f.get("description"):
                        f["description"] = f"Week {w}: {feature_defaults[w - 1]}"
    data["flagship_project"]["weekly_features"] = sorted(features, key=lambda x: x.get("week", 0))[:4]

    return data


# ── Endpoint 1: Generate Roadmap ────────────────────────────────
@app.post("/generate-roadmap", response_model=RoadmapResponse)
async def generate_roadmap(req: RoadmapRequest):
    """
    Two sequential LLM calls.
    Takes resume text + dream role → returns full analysis + 30-day plan.
    Falls back to mock data if LLM fails.
    """
    # Look up role context from local JSON
    role_skills = state["roles"].get(req.dream_role)
    if role_skills:
        role_context = json.dumps(role_skills, indent=2)
    else:
        role_context = f"General skills for a {req.dream_role} role."

    # Fetch GitHub profile if username provided
    github_context = ""
    if req.github_username.strip():
        print(f"[Career Brain] Fetching GitHub profile: {req.github_username}")
        gh_summary = fetch_github_profile(req.github_username.strip())
        if gh_summary:
            github_context = format_github_context(gh_summary)
        else:
            print("[Career Brain] GitHub fetch failed, continuing without it")

    # Build prompt for Call 1: skills, gaps, roadmap
    prompt = build_roadmap_prompt(req.resume_text, req.dream_role, role_context, github_context)

    # Call 1: LLM for roadmap
    print("[Career Brain] === Call 1: Skills/Gaps/Roadmap ===")
    result = call_llm(prompt)

    # Fallback to mock data if LLM fails
    if result is None:
        print("[Career Brain] Using mock data fallback")
        result = MOCK_ROADMAP_RESPONSE

    # Post-process Call 1 result
    result = post_process_roadmap(result, req.dream_role)

    # Call 2: Flagship project (using gap data from Call 1)
    print("[Career Brain] === Call 2: Flagship Project ===")
    skills_list = [s.get("name", "") for s in result.get("skill_map", {}).get("skills", [])]
    gaps_list = [g.get("skill", "") for g in result.get("gap_analysis", {}).get("critical", [])]
    gaps_list += [g.get("skill", "") for g in result.get("gap_analysis", {}).get("important", [])]

    project_prompt = build_project_prompt(req.dream_role, skills_list, gaps_list)
    project_result = call_llm(project_prompt)

    if project_result and isinstance(project_result, dict):
        # Extract flagship_project from response (may be nested or at top level)
        fp = project_result.get("flagship_project") or project_result.get("project") or project_result
        if isinstance(fp, dict) and "title" in fp or "name" in fp:
            result["flagship_project"] = fp
            # Re-run project sub-key normalization
            result = post_process_roadmap(result, req.dream_role)
            print("[Career Brain] Project merged from Call 2")
        else:
            print("[Career Brain] Call 2 returned unexpected format, using defaults")
    else:
        print("[Career Brain] Call 2 failed, using default project")

    # Store in state for adaptation
    state["last_roadmap"] = result
    state["last_request"] = {"resume_text": req.resume_text, "dream_role": req.dream_role}

    try:
        return RoadmapResponse(**result)
    except Exception as e:
        print(f"[Career Brain] Validation error: {e}, using mock")
        state["last_roadmap"] = MOCK_ROADMAP_RESPONSE
        return RoadmapResponse(**MOCK_ROADMAP_RESPONSE)


# ── Endpoint 2: Adapt Roadmap ──────────────────────────────────
@app.post("/adapt-roadmap", response_model=AdaptResponse)
async def adapt_roadmap(req: AdaptRequest):
    """
    The SECOND Gemini call.
    Takes progress update → returns adapted remaining roadmap.
    Falls back to mock data if Gemini fails.
    """
    if state["last_roadmap"] is None:
        raise HTTPException(
            status_code=400,
            detail="No roadmap generated yet. Call /generate-roadmap first.",
        )

    # Send adaptation data directly
    original_json = json.dumps(state["last_roadmap"], indent=2)
    prompt = f"ORIGINAL ROADMAP:\n{original_json}\n\nPROGRESS: {req.days_completed} days completed, {req.days_missed} days missed.\nReason: {req.reason}\nConfidence: {req.confidence}/10"

    # Call LLM
    result = call_llm(prompt)

    # Fallback to mock data if LLM fails
    if result is None:
        print("[Career Brain] Using mock adaptation fallback")
        result = MOCK_ADAPT_RESPONSE

    try:
        return AdaptResponse(**result)
    except Exception as e:
        print(f"[Career Brain] Validation error: {e}, using mock")
        return AdaptResponse(**MOCK_ADAPT_RESPONSE)


# ── Utility endpoints ──────────────────────────────────────────
@app.get("/roles")
async def get_roles():
    """Return available dream roles for the frontend dropdown."""
    return {"roles": list(state["roles"].keys())}


@app.get("/sample-resume")
async def get_sample_resume():
    """Return sample resume text for demo convenience."""
    resume_path = Path(__file__).parent / "data" / "sample_resume.txt"
    if resume_path.exists():
        return {"resume_text": resume_path.read_text(encoding="utf-8")}
    return {"resume_text": ""}


@app.get("/health")
async def health():
    return {"status": "ok", "agent": "Career Brain", "version": "1.0.0"}
