"""
GitHub API integration — production-ready.

Features:
  - Username regex validation (^[a-zA-Z0-9-]{1,39}$)
  - 10-minute in-memory cache to avoid rate limits
  - Text sanitization (strip URLs, markdown, truncate)
  - Compact LLM-friendly summary dict
  - Never crashes the app — returns None on any failure
"""
import os
import re
import json
import time
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from dotenv import load_dotenv

load_dotenv()

# ── Constants ───────────────────────────────────────────────────

GITHUB_API = "https://api.github.com"
USERNAME_RE = re.compile(r"^[a-zA-Z0-9\-]{1,39}$")
SANITIZE_URL_RE = re.compile(r"https?://\S+")
SANITIZE_MD_RE = re.compile(r"[#*`\[\]()>~_]")
CACHE_TTL = 600  # 10 minutes
MAX_TEXT_LEN = 500

# ── In-memory cache ─────────────────────────────────────────────

_cache: dict[str, tuple[float, dict]] = {}


# ── Public API ──────────────────────────────────────────────────

def fetch_github_profile(username: str) -> dict | None:
    """
    Fetch a GitHub user's profile and top repos.
    Returns a compact summary dict for LLM consumption, or None on any error.

    Return shape:
        {
            "top_languages": ["Python", "JavaScript"],
            "primary_domain": "web development",
            "notable_projects": [
                {"name": "repo-name", "language": "Python", "stars": 12, "about": "..."}
            ],
            "experience_signal": "low" | "medium" | "strong"
        }
    """
    # Validate username
    if not username or not USERNAME_RE.match(username):
        print(f"[GitHub] Invalid username: {username!r}")
        return None

    username = username.lower()

    # Check cache
    if username in _cache:
        ts, data = _cache[username]
        if time.time() - ts < CACHE_TTL:
            print(f"[GitHub] Cache hit: {username}")
            return data

    try:
        headers = _build_headers()

        # Fetch user profile
        user = _get(f"/users/{username}", headers)
        if user is None:
            return None

        # Fetch repos (top 30 by recent update)
        repos = _get(f"/users/{username}/repos?sort=updated&per_page=30", headers)
        if repos is None:
            repos = []

        summary = _build_summary(user, repos)

        # Cache result
        _cache[username] = (time.time(), summary)
        print(f"[GitHub] Profile fetched: {username} — signal={summary['experience_signal']}")
        return summary

    except Exception as e:
        print(f"[GitHub] Unexpected error for {username}: {e}")
        return None


def format_github_context(summary: dict) -> str:
    """
    Convert the compact summary dict into a short text block
    suitable for inserting into an LLM prompt.
    """
    lines = [
        f"Languages: {', '.join(summary.get('top_languages', [])) or 'N/A'}",
        f"Primary Domain: {summary.get('primary_domain', 'N/A')}",
        f"Experience Signal: {summary.get('experience_signal', 'low')}",
    ]
    projects = summary.get("notable_projects", [])
    if projects:
        lines.append("Notable Projects:")
        for p in projects[:6]:
            lang = p.get("language") or "N/A"
            stars = p.get("stars", 0)
            about = p.get("about", "")
            lines.append(f"  - {p['name']} ({lang}, {stars}★): {about}")
    return "\n".join(lines)


# ── Internal helpers ────────────────────────────────────────────

def _build_headers() -> dict:
    token = os.getenv("GITHUB_TOKEN", "")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def _get(path: str, headers: dict) -> dict | list | None:
    """GET request to GitHub API with timeout."""
    url = GITHUB_API + path
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        if e.code == 404:
            print(f"[GitHub] Not found: {path}")
        elif e.code == 403:
            print(f"[GitHub] Rate limited — add GITHUB_TOKEN to .env")
        else:
            print(f"[GitHub] API error {e.code}: {e.reason}")
        return None
    except (URLError, TimeoutError) as e:
        print(f"[GitHub] Connection error: {e}")
        return None


def _sanitize_text(text: str | None) -> str:
    """Remove URLs, markdown chars, and truncate to MAX_TEXT_LEN."""
    if not text:
        return ""
    text = SANITIZE_URL_RE.sub("", text)
    text = SANITIZE_MD_RE.sub("", text)
    text = " ".join(text.split())  # collapse whitespace
    return text[:MAX_TEXT_LEN].strip()


def _infer_domain(languages: list[str], repos: list[dict]) -> str:
    """Guess the user's primary domain from languages and repo topics."""
    lang_set = {l.lower() for l in languages}
    all_desc = " ".join(_sanitize_text(r.get("description")).lower() for r in repos)

    domain_signals = {
        "web development": {"javascript", "typescript", "html", "css", "react", "vue", "angular"},
        "data science / ML": {"python", "jupyter notebook", "r"},
        "mobile development": {"kotlin", "swift", "dart", "java"},
        "systems / infrastructure": {"c", "c++", "rust", "go"},
        "devops / cloud": {"shell", "hcl", "dockerfile"},
    }

    best_domain, best_score = "general software development", 0
    for domain, signals in domain_signals.items():
        score = len(lang_set & signals)
        # Bonus for keywords in descriptions
        for kw in signals:
            if kw in all_desc:
                score += 0.5
        if score > best_score:
            best_score = score
            best_domain = domain

    return best_domain


def _compute_experience_signal(user: dict, repos: list[dict]) -> str:
    """Classify GitHub activity as low/medium/strong."""
    repo_count = user.get("public_repos", 0)
    followers = user.get("followers", 0)
    total_stars = sum(r.get("stargazers_count", 0) for r in repos)

    if repo_count >= 20 or total_stars >= 50 or followers >= 30:
        return "strong"
    if repo_count >= 8 or total_stars >= 10 or followers >= 5:
        return "medium"
    return "low"


def _build_summary(user: dict, repos: list[dict]) -> dict:
    """Build the compact summary dict from raw API data."""
    # Extract unique languages
    languages = []
    seen = set()
    for repo in repos:
        lang = repo.get("language")
        if lang and lang.lower() not in seen:
            languages.append(lang)
            seen.add(lang.lower())

    # Build notable projects (top repos by stars, non-fork)
    non_forks = [r for r in repos if not r.get("fork", False)]
    sorted_repos = sorted(non_forks, key=lambda r: r.get("stargazers_count", 0), reverse=True)
    notable = []
    for r in sorted_repos[:8]:
        notable.append({
            "name": r.get("name", ""),
            "language": r.get("language", ""),
            "stars": r.get("stargazers_count", 0),
            "about": _sanitize_text(r.get("description")),
        })

    return {
        "top_languages": languages[:10],
        "primary_domain": _infer_domain(languages, repos),
        "notable_projects": notable,
        "experience_signal": _compute_experience_signal(user, repos),
    }


def clear_cache():
    """Clear the in-memory cache. Used in testing."""
    _cache.clear()
