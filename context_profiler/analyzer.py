"""Compute token usage breakdowns for a parsed conversation."""

from __future__ import annotations

from dataclasses import dataclass

from context_profiler.model_specs import get_context_window
from context_profiler.models import Conversation, Message
from context_profiler.tokenizer import count_tokens


@dataclass
class RoleTotal:
    role: str
    tokens: int
    message_count: int


@dataclass
class AnalysisResult:
    conversation: Conversation
    model: str
    context_window: int

    @property
    def total_tokens(self) -> int:
        return self.conversation.total_tokens

    @property
    def percent_of_window(self) -> float:
        if self.context_window == 0:
            return 0.0
        return 100 * self.total_tokens / self.context_window

    def role_totals(self) -> list[RoleTotal]:
        totals: dict[str, RoleTotal] = {}
        for m in self.conversation.messages:
            if m.role not in totals:
                totals[m.role] = RoleTotal(role=m.role, tokens=0, message_count=0)
            totals[m.role].tokens += m.token_count
            totals[m.role].message_count += 1
        return sorted(totals.values(), key=lambda r: r.tokens, reverse=True)

    def top_messages(self, n: int = 10) -> list[Message]:
        return sorted(
            self.conversation.messages, key=lambda m: m.token_count, reverse=True
        )[:n]


def analyze(conversation: Conversation, model: str) -> AnalysisResult:
    for m in conversation.messages:
        m.token_count = count_tokens(m.content)
    return AnalysisResult(
        conversation=conversation,
        model=model,
        context_window=get_context_window(model),
    )
