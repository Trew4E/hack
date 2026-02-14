"""Pydantic models for The Personal Career Navigator.
Made flexible to handle variations in LLM output (local Ollama).
"""
from pydantic import BaseModel, Field


# ── Request Models ──────────────────────────────────────────────

class RoadmapRequest(BaseModel):
    resume_text: str = Field(..., description="Plain text resume content")
    dream_role: str = Field(..., description="Target career role")
    github_username: str = Field(default="", description="Optional GitHub username for profile enrichment")


class AdaptRequest(BaseModel):
    days_completed: int = Field(..., ge=0, le=30)
    days_missed: int = Field(..., ge=0, le=30)
    reason: str = Field(default="busy with other commitments")
    confidence: int = Field(default=5, ge=1, le=10)


# ── Response Sub-Models (flexible for local LLMs) ──────────────

class Skill(BaseModel):
    name: str = ""
    level: str = "beginner"
    category: str = "technical"


class SkillMap(BaseModel):
    skills: list[Skill] = []
    strengths: list[str] = []
    weaknesses: list[str] = []


class RoleRequirements(BaseModel):
    core_technical: list[str] = []
    supporting_skills: list[str] = []
    theory_math: list[str] = []
    tools: list[str] = []
    soft_skills: list[str] = []
    portfolio_expectations: list[str] = []


class GapItem(BaseModel):
    skill: str = ""
    reason: str = ""


class GapAnalysis(BaseModel):
    critical: list[GapItem] = []
    important: list[GapItem] = []
    nice_to_have: list[GapItem] = []


class DayPlan(BaseModel):
    day: int = 0
    objective: str = ""
    resource: str = ""
    task: str = ""
    output: str = ""
    hours: float = 2.0


class WeeklyMilestone(BaseModel):
    week: int = 0
    milestone: str = ""
    skills_gained: list[str] = []


class Roadmap(BaseModel):
    days: list[DayPlan] = []
    weekly_milestones: list[WeeklyMilestone] = []


class WeeklyFeature(BaseModel):
    week: int = 0
    feature: str = ""
    description: str = ""


class FlagshipProject(BaseModel):
    title: str = ""
    problem_statement: str = ""
    tech_stack: list[str] = []
    weekly_features: list[WeeklyFeature] = []
    portfolio_quality: str = ""


# ── Full Response Models ────────────────────────────────────────

class RoadmapResponse(BaseModel):
    skill_map: SkillMap = SkillMap()
    role_requirements: RoleRequirements = RoleRequirements()
    gap_analysis: GapAnalysis = GapAnalysis()
    roadmap: Roadmap = Roadmap()
    flagship_project: FlagshipProject = FlagshipProject()
    reasoning: str = ""


class AdaptedProject(BaseModel):
    changes: str = ""
    weekly_features: list[WeeklyFeature] = []


class AdaptResponse(BaseModel):
    adaptation_reasoning: str = ""
    adapted_roadmap: Roadmap = Roadmap()
    adapted_project: AdaptedProject = AdaptedProject()
    motivation: str = ""
