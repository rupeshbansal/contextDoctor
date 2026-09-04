"""Parsers for chat export JSON formats into a Conversation.

Supports two shapes:
  - "generic": a bare list of {"role": ..., "content": ...} messages, the
    shape used by the Anthropic/OpenAI messages API and most simple logs.
  - "claude_export": a claude.ai conversation export, with a top-level
    "chat_messages" list of {"sender": "human"|"assistant", "text": ...}.
"""

from __future__ import annotations

import json
from pathlib import Path

from context_profiler.models import Conversation, Message

_SENDER_TO_ROLE = {"human": "user", "assistant": "assistant"}


def _content_to_text(content: object) -> str:
    """Flatten a message's content into plain text.

    Content may be a plain string, or a list of content blocks (as in the
    Anthropic API), e.g. [{"type": "text", "text": "..."}].
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                if "text" in block:
                    parts.append(str(block["text"]))
                else:
                    parts.append(json.dumps(block))
        return "\n".join(parts)
    if content is None:
        return ""
    return json.dumps(content)


def _parse_generic(data: list) -> Conversation:
    messages = []
    for i, raw in enumerate(data):
        role = raw.get("role", "unknown")
        text = _content_to_text(raw.get("content"))
        messages.append(Message(role=role, content=text, index=i, name=raw.get("name")))
    return Conversation(messages=messages)


def _parse_claude_export(data: dict) -> Conversation:
    messages = []
    for i, raw in enumerate(data.get("chat_messages", [])):
        sender = raw.get("sender", "unknown")
        role = _SENDER_TO_ROLE.get(sender, sender)
        text = raw.get("text") or _content_to_text(raw.get("content"))
        messages.append(Message(role=role, content=text, index=i))
    return Conversation(messages=messages)


def parse_conversation(data: object) -> Conversation:
    """Detect the shape of `data` and parse it into a Conversation."""
    if isinstance(data, list):
        return _parse_generic(data)
    if isinstance(data, dict):
        if "chat_messages" in data:
            return _parse_claude_export(data)
        if "messages" in data and isinstance(data["messages"], list):
            return _parse_generic(data["messages"])
    raise ValueError(
        "Unrecognized conversation format: expected a list of messages, "
        "an object with a 'messages' list, or a claude.ai export with "
        "'chat_messages'."
    )


def load_conversation(path: str | Path) -> Conversation:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    conversation = parse_conversation(data)
    conversation.source_path = str(path)
    return conversation
