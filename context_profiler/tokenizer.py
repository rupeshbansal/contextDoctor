"""Token counting.

Claude and other non-OpenAI models don't have a public tiktoken encoding, so we
use tiktoken's cl100k_base as a consistent estimator across providers. It's not
exact for every model, but it's stable and close enough to compare where tokens
are going within a single conversation.
"""

from __future__ import annotations

from functools import lru_cache

import tiktoken

DEFAULT_ENCODING = "cl100k_base"


@lru_cache(maxsize=None)
def _get_encoding(name: str = DEFAULT_ENCODING) -> tiktoken.Encoding:
    return tiktoken.get_encoding(name)


def count_tokens(text: str, encoding: str = DEFAULT_ENCODING) -> int:
    if not text:
        return 0
    return len(_get_encoding(encoding).encode(text, disallowed_special=()))
