"""Prompt templates for Career Brain agent."""


def build_roadmap_prompt(resume_text: str, dream_role: str, role_skills: str, github_context: str = "") -> str:
    """Call 1: Skills, gaps, and 30-day roadmap (no project)."""
    github_section = ""
    if github_context.strip():
        github_section = f"\nGITHUB PROFILE:\n{github_context}\n"

    return f"""You are Career Brain. Analyze this student for the "{dream_role}" role.

RESUME:
{resume_text}

ROLE SKILLS:
{role_skills}
{github_section}
Return JSON with reasoning, skill analysis, gap analysis, and a 30-day roadmap.

RULES:
1. roadmap.days must have EXACTLY 30 objects (day 1 to day 30).
2. weekly_milestones must have EXACTLY 4 objects (week 1 to week 4).
3. Every field must have real content. No empty strings.
4. Return ONLY valid JSON.

{{
  "reasoning": "2-3 sentences about this student's situation and roadmap strategy.",
  "skill_map": {{
    "skills": [{{"name": "SKILL", "level": "beginner|intermediate|advanced", "category": "technical|soft|tool"}}],
    "strengths": ["STRENGTH"],
    "weaknesses": ["WEAKNESS"]
  }},
  "role_requirements": {{
    "core_technical": ["SKILL"],
    "supporting_skills": ["SKILL"],
    "theory_math": ["TOPIC"],
    "tools": ["TOOL"],
    "soft_skills": ["SKILL"],
    "portfolio_expectations": ["EXPECTATION"]
  }},
  "gap_analysis": {{
    "critical": [{{"skill": "SKILL", "reason": "WHY"}}],
    "important": [{{"skill": "SKILL", "reason": "WHY"}}],
    "nice_to_have": [{{"skill": "SKILL", "reason": "WHY"}}]
  }},
  "roadmap": {{
    "days": [
      {{"day": 1, "objective": "WHAT", "resource": "WHERE", "task": "DO_WHAT", "hours": 2}},
      {{"day": 2, "objective": "...", "resource": "...", "task": "...", "hours": 3}},
      {{"day": 30, "objective": "...", "resource": "...", "task": "...", "hours": 2}}
    ],
    "weekly_milestones": [
      {{"week": 1, "milestone": "ACHIEVED", "skills_gained": ["SKILL"]}},
      {{"week": 2, "milestone": "...", "skills_gained": ["..."]}},
      {{"week": 3, "milestone": "...", "skills_gained": ["..."]}},
      {{"week": 4, "milestone": "...", "skills_gained": ["..."]}}
    ]
  }}
}}

Generate all 30 days with real content based on the resume."""


def build_project_prompt(dream_role: str, skills: list, gaps: list) -> str:
    """Call 2: Flagship project based on the gap analysis from Call 1."""
    skills_text = ", ".join(skills[:10]) if skills else "general skills"
    gaps_text = ", ".join(gaps[:8]) if gaps else "core role skills"

    return f"""You are Career Brain. Design a portfolio project for a student targeting the "{dream_role}" role.

STUDENT'S CURRENT SKILLS: {skills_text}
KEY GAPS TO ADDRESS: {gaps_text}

Create a flagship project that helps this student fill their skill gaps and build a strong portfolio.

Return JSON only:
{{
  "flagship_project": {{
    "title": "PROJECT_NAME",
    "problem_statement": "WHAT_THE_PROJECT_DOES_AND_WHY",
    "tech_stack": ["TECH_1", "TECH_2", "TECH_3"],
    "weekly_features": [
      {{"week": 1, "feature": "FEATURE_NAME", "description": "WHAT_TO_BUILD_THIS_WEEK"}},
      {{"week": 2, "feature": "FEATURE_NAME", "description": "WHAT_TO_BUILD_THIS_WEEK"}},
      {{"week": 3, "feature": "FEATURE_NAME", "description": "WHAT_TO_BUILD_THIS_WEEK"}},
      {{"week": 4, "feature": "FEATURE_NAME", "description": "WHAT_TO_BUILD_THIS_WEEK"}}
    ],
    "portfolio_quality": "WHY_THIS_PROJECT_IMPRESSES_HIRING_MANAGERS"
  }}
}}

Make the project realistic, achievable in 4 weeks, and relevant to {dream_role}. Return ONLY valid JSON."""


def build_adapt_prompt(
    original_roadmap_json: str,
    days_completed: int,
    days_missed: int,
    reason: str,
    confidence: int,
) -> str:
    return f"""You are Career Brain. A student's situation has changed.

ORIGINAL ROADMAP:
{original_roadmap_json}

PROGRESS UPDATE:
- Days completed: {days_completed}
- Days missed: {days_missed}
- Reason: {reason}
- Current confidence: {confidence}/10

Adapt the remaining roadmap. Return JSON with EXACTLY this structure:
{{
  "adaptation_reasoning": "2-3 sentences explaining what changed and why.",
  "adapted_roadmap": {{
    "days": [
      {{"day": N, "objective": "...", "resource": "...", "task": "...", "output": "...", "hours": 2}}
    ],
    "weekly_milestones": [
      {{"week": N, "milestone": "...", "skills_gained": ["..."]}}
    ]
  }},
  "adapted_project": {{
    "changes": "What changed in the flagship project scope",
    "weekly_features": [
      {{"week": N, "feature": "...", "description": "..."}}
    ]
  }},
  "motivation": "One encouraging sentence for the student."
}}

RULES:
- Only include remaining days (from day {days_completed + days_missed + 1} to day 30).
- Compress skipped content into remaining time.
- Prioritize critical gaps over nice-to-haves.
- Be realistic about reduced time.
- Return ONLY valid JSON. No markdown, no code fences, no extra text."""
