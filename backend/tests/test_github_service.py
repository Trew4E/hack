"""
Unit tests for github_service.py

Covers:
  - Valid username fetch
  - Invalid username rejection
  - API failure handling
  - Caching behavior
  - Text sanitization
  - format_github_context output
"""
import time
import json
import unittest
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from github_service import (
    fetch_github_profile,
    format_github_context,
    clear_cache,
    _sanitize_text,
    USERNAME_RE,
)


# ── Mock data ───────────────────────────────────────────────────

MOCK_USER = {
    "login": "testuser",
    "name": "Test User",
    "bio": "Python dev. Check https://example.com for more **info**.",
    "public_repos": 15,
    "followers": 10,
}

MOCK_REPOS = [
    {
        "name": "web-app",
        "description": "A React web application with **markdown** and https://link.com",
        "language": "JavaScript",
        "stargazers_count": 25,
        "forks_count": 5,
        "fork": False,
        "updated_at": "2024-01-15",
    },
    {
        "name": "ml-pipeline",
        "description": "Machine learning pipeline",
        "language": "Python",
        "stargazers_count": 12,
        "forks_count": 2,
        "fork": False,
        "updated_at": "2024-01-10",
    },
    {
        "name": "forked-repo",
        "description": "A fork",
        "language": "Python",
        "stargazers_count": 1000,
        "forks_count": 500,
        "fork": True,
        "updated_at": "2024-01-05",
    },
]


class TestUsernameValidation(unittest.TestCase):
    """Test regex validation of GitHub usernames."""

    def test_valid_usernames(self):
        for name in ["octocat", "test-user", "a", "A1-b2-C3", "x" * 39]:
            self.assertIsNotNone(USERNAME_RE.match(name), f"{name} should be valid")

    def test_invalid_usernames(self):
        for name in ["", "a" * 40, "user@name", "user name", "user.name", "user/name"]:
            result = USERNAME_RE.match(name) if name else None
            self.assertIsNone(result, f"{name!r} should be invalid")

    def test_fetch_rejects_invalid(self):
        self.assertIsNone(fetch_github_profile(""))
        self.assertIsNone(fetch_github_profile("a" * 40))
        self.assertIsNone(fetch_github_profile("user@bad"))


class TestSanitizeText(unittest.TestCase):
    """Test text sanitization (URL/markdown removal, truncation)."""

    def test_removes_urls(self):
        result = _sanitize_text("Check https://example.com for details")
        self.assertNotIn("https://", result)
        self.assertIn("Check", result)

    def test_removes_markdown(self):
        result = _sanitize_text("This is **bold** and [link](url)")
        self.assertNotIn("**", result)
        self.assertNotIn("[", result)

    def test_truncates_long_text(self):
        long_text = "A" * 600
        result = _sanitize_text(long_text)
        self.assertLessEqual(len(result), 500)

    def test_handles_none(self):
        self.assertEqual(_sanitize_text(None), "")
        self.assertEqual(_sanitize_text(""), "")


class TestFetchGitHubProfile(unittest.TestCase):
    """Test profile fetching with mocked GitHub API."""

    def setUp(self):
        clear_cache()

    @patch("github_service._get")
    def test_valid_user_returns_summary(self, mock_get):
        mock_get.side_effect = [MOCK_USER, MOCK_REPOS]

        result = fetch_github_profile("testuser")

        self.assertIsNotNone(result)
        self.assertIn("top_languages", result)
        self.assertIn("primary_domain", result)
        self.assertIn("notable_projects", result)
        self.assertIn("experience_signal", result)
        self.assertIn("JavaScript", result["top_languages"])
        self.assertIn("Python", result["top_languages"])

    @patch("github_service._get")
    def test_excludes_forks_from_notable(self, mock_get):
        mock_get.side_effect = [MOCK_USER, MOCK_REPOS]

        result = fetch_github_profile("testuser")
        project_names = [p["name"] for p in result["notable_projects"]]
        self.assertNotIn("forked-repo", project_names)

    @patch("github_service._get")
    def test_experience_signal(self, mock_get):
        mock_get.side_effect = [MOCK_USER, MOCK_REPOS]

        result = fetch_github_profile("testuser")
        # 15 repos, 10 followers, total stars includes fork (1037) → strong
        self.assertEqual(result["experience_signal"], "strong")

    @patch("github_service._get")
    def test_api_user_not_found(self, mock_get):
        mock_get.return_value = None

        result = fetch_github_profile("nonexistent")
        self.assertIsNone(result)

    @patch("github_service._get")
    def test_api_repos_fail_still_returns(self, mock_get):
        """If repos fail but user succeeds, should return with empty projects."""
        mock_get.side_effect = [MOCK_USER, None]

        result = fetch_github_profile("testuser")
        self.assertIsNotNone(result)
        self.assertEqual(result["notable_projects"], [])

    @patch("github_service._get")
    def test_unexpected_exception_returns_none(self, mock_get):
        mock_get.side_effect = RuntimeError("network down")

        result = fetch_github_profile("testuser")
        self.assertIsNone(result)


class TestCaching(unittest.TestCase):
    """Test 10-minute in-memory cache."""

    def setUp(self):
        clear_cache()

    @patch("github_service._get")
    def test_second_call_uses_cache(self, mock_get):
        mock_get.side_effect = [MOCK_USER, MOCK_REPOS]

        result1 = fetch_github_profile("cacheuser")
        result2 = fetch_github_profile("cacheuser")

        self.assertEqual(result1, result2)
        # _get should only be called twice (user + repos), not four times
        self.assertEqual(mock_get.call_count, 2)

    @patch("github_service._get")
    @patch("github_service.time")
    def test_cache_expires_after_ttl(self, mock_time, mock_get):
        mock_get.side_effect = [MOCK_USER, MOCK_REPOS, MOCK_USER, MOCK_REPOS]
        mock_time.time.side_effect = [
            1000.0,       # first fetch: cache write timestamp
            1000.0,       # second fetch: cache check (within TTL)
            2000.0,       # third fetch: cache check (expired, 1000s > 600s TTL)
            2000.0,       # third fetch: cache write timestamp
        ]

        fetch_github_profile("expireuser")
        fetch_github_profile("expireuser")  # cache hit
        fetch_github_profile("expireuser")  # cache expired → re-fetch

        self.assertEqual(mock_get.call_count, 4)  # 2 initial + 2 re-fetch


class TestFormatGitHubContext(unittest.TestCase):
    """Test that format_github_context produces clean LLM text."""

    def test_produces_readable_text(self):
        summary = {
            "top_languages": ["Python", "JavaScript"],
            "primary_domain": "web development",
            "notable_projects": [
                {"name": "my-app", "language": "Python", "stars": 10, "about": "A cool app"}
            ],
            "experience_signal": "medium",
        }
        text = format_github_context(summary)
        self.assertIn("Python, JavaScript", text)
        self.assertIn("web development", text)
        self.assertIn("medium", text)
        self.assertIn("my-app", text)
        self.assertIn("10★", text)

    def test_handles_empty_summary(self):
        summary = {
            "top_languages": [],
            "primary_domain": "N/A",
            "notable_projects": [],
            "experience_signal": "low",
        }
        text = format_github_context(summary)
        self.assertIn("N/A", text)
        self.assertIn("low", text)


class TestBackwardCompatibility(unittest.TestCase):
    """Ensure roadmap generation works without GitHub data."""

    def test_roadmap_request_without_github(self):
        """RoadmapRequest should work without github_username."""
        from models import RoadmapRequest
        req = RoadmapRequest(resume_text="Test resume", dream_role="ML Engineer")
        self.assertEqual(req.github_username, "")

    def test_build_prompt_without_github(self):
        """build_roadmap_prompt should work without github_context."""
        from prompts import build_roadmap_prompt
        prompt = build_roadmap_prompt("resume", "role", "skills")
        self.assertNotIn("GITHUB PROFILE", prompt)
        self.assertIn("resume", prompt)

    def test_build_prompt_with_github(self):
        """build_roadmap_prompt should include GitHub section when provided."""
        from prompts import build_roadmap_prompt
        prompt = build_roadmap_prompt("resume", "role", "skills", "Languages: Python")
        self.assertIn("GITHUB PROFILE:", prompt)
        self.assertIn("Languages: Python", prompt)


if __name__ == "__main__":
    unittest.main()
