"""LLM integration — Ollama (local) with mock data fallback."""
import json
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral:7b")


def call_gemini(prompt: str, max_retries: int = 1) -> dict:
    """
    Call LLM and return parsed JSON.

    Priority:
    1. Ollama (local) — if running
    2. None — caller falls back to mock data
    """
    try:
        from ollama import chat

        print(f"[Career Brain] Calling Ollama ({OLLAMA_MODEL})...")

        response = chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
            format="json",
            options={
                "temperature": 0.4,
                "num_predict": 16384,
            },
        )

        text = response.message.content.strip()
        print(f"[Career Brain] Raw response length: {len(text)} chars")
        result = json.loads(text)

        # Log which top-level keys are present
        keys = list(result.keys()) if isinstance(result, dict) else []
        print(f"[Career Brain] Response keys: {keys}")

        # Log roadmap day count
        days = result.get("roadmap", {}).get("days", [])
        print(f"[Career Brain] Roadmap days: {len(days)}")

        print("[Career Brain] Ollama response parsed successfully")
        return result

    except ImportError:
        print("[Career Brain] ollama package not installed")
        return None
    except json.JSONDecodeError as e:
        print(f"[Career Brain] Ollama JSON parse error: {e}")
        return None
    except Exception as e:
        print(f"[Career Brain] Ollama error: {e}")
        return None
