"""Known context window sizes, for showing usage as a percentage."""

from __future__ import annotations

CONTEXT_WINDOWS: dict[str, int] = {
    "claude-opus-5": 500_000,
    "claude-sonnet-5": 500_000,
    "claude-fable-5-1": 500_000,
    "claude-haiku-4-5": 200_000,
    "claude-sonnet-4": 200_000,
    "gpt-5": 400_000,
    "gpt-4o": 128_000,
    "gpt-4-turbo": 128_000,
    "o3": 200_000,
}

DEFAULT_MODEL = "claude-sonnet-5"


def get_context_window(model: str) -> int:
    if model not in CONTEXT_WINDOWS:
        raise KeyError(
            f"Unknown model {model!r}. Known models: {', '.join(sorted(CONTEXT_WINDOWS))}"
        )
    return CONTEXT_WINDOWS[model]
