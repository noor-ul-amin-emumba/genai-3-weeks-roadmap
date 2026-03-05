"""
Centralized configuration for LLM usage.

Handles:
  - Environment variable loading (.env file)
  - Groq API client initialization
  - Shared LLM call utility with retry/backoff
  - Model and API key validation

Usage:
  from config import client, MODEL, call_llm

  response_text, prompt_tokens, completion_tokens = call_llm(
      system="You are a helpful assistant.",
      user="What is X?",
      max_tokens=400
  )
"""

import os
import time
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from httpx import HTTPStatusError

# ---------------------------------------------------------------------------
# Environment Setup
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent
DOTENV_PATH = PROJECT_ROOT / ".env"

# Load environment variables from .env
load_dotenv(dotenv_path=DOTENV_PATH)

# Retrieve credentials
MODEL = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")
API_KEY = os.environ.get("GROQ_API_KEY")

# Validate API key
if not API_KEY:
    raise SystemExit(
        f"GROQ_API_KEY is missing. Add it to {DOTENV_PATH} or set it as an environment variable."
    )

# Initialize Groq client
client = Groq(api_key=API_KEY)


# ---------------------------------------------------------------------------
# Shared LLM Call Utility
# ---------------------------------------------------------------------------
def call_llm(
    system: str = "",
    user: str = "",
    messages: list[dict] = None,
    max_tokens: int = 400,
    temperature: float | None = None,
    top_p: float | None = None,
    label: str = "",
    model: str | None = None,
) -> tuple[str, int, int]:
    """
    Call the Groq API with automatic retry and exponential backoff on rate limits.

    Args:
        system: System prompt (ignored if `messages` is provided).
        user: User message (ignored if `messages` is provided).
        messages: Full message list (if provided, system/user args are ignored).
        max_tokens: Maximum tokens in response.
        temperature: Optional sampling temperature.
        top_p: Optional nucleus sampling value.
        label: Optional label for logging (helps identify which script/prompt called this).
        model: Optional LLM model override (defaults to global MODEL).

    Returns:
        (response_text, prompt_tokens, completion_tokens)

    Raises:
        HTTPStatusError: If API returns an unrecoverable error.
        RuntimeError: If max retries exceeded on rate limit.
    """

    # print call details for debugging
    label_suffix = f" {label}" if label else ""
    print(
        f"Calling LLM{label_suffix} with model '{model or MODEL}' and max_tokens={max_tokens}...")

    # Build messages list if not provided
    if messages is None:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        if user:
            messages.append({"role": "user", "content": user})

    # Base delay before each call
    time.sleep(3)

    max_retries = 4
    for attempt in range(max_retries):
        try:
            request_kwargs = {
                "model": model or MODEL,
                "max_tokens": max_tokens,
                "messages": messages,
            }
            if temperature is not None:
                request_kwargs["temperature"] = temperature
            if top_p is not None:
                request_kwargs["top_p"] = top_p

            response = client.chat.completions.create(
                **request_kwargs,
            )
            text = response.choices[0].message.content.strip()
            usage = response.usage
            return text, usage.prompt_tokens, usage.completion_tokens

        except HTTPStatusError as exc:
            # Handle rate limiting with exponential backoff
            if exc.response.status_code == 429 and attempt < max_retries - 1:
                wait = 30 * (2 ** attempt)  # 30s, 60s, 120s, 240s
                label_suffix = f" ({label})" if label else ""
                print(
                    f"    [429] Rate limited{label_suffix}. Waiting {wait}s before retry {attempt + 1}/{max_retries - 1} ...")
                time.sleep(wait)
            else:
                # Non-rate-limit error or final retry exhausted
                raise

        except Exception as exc:
            # Unexpected error
            print(
                f"  [ERROR in call_llm{(f' {label}' if label else '')}]: {exc}")
            raise

    raise RuntimeError(
        f"Max retries ({max_retries}) exceeded for call_llm{(f' {label}' if label else '')}"
    )


# ---------------------------------------------------------------------------
# Debugging: Print configuration on import (optional)
# ---------------------------------------------------------------------------
def print_config():
    """Print current configuration (optional, for debugging)."""
    print(f"Configuration loaded from {DOTENV_PATH}")
    print(f"  Model: {MODEL}")
    print(f"  API Key: {'***' if API_KEY else 'MISSING'}")
    print(f"  Project root: {PROJECT_ROOT}")


if __name__ == "__main__":
    # If this script is run directly, print config
    print_config()
