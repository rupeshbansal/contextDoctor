"""Data structures for a parsed conversation."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Message:
    """A single message in a conversation."""

    role: str
    content: str
    index: int
    name: str | None = None
    token_count: int = 0


@dataclass
class Conversation:
    """A parsed conversation ready for token analysis."""

    messages: list[Message] = field(default_factory=list)
    source_path: str | None = None

    @property
    def total_tokens(self) -> int:
        return sum(m.token_count for m in self.messages)
