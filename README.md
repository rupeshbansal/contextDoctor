# context-profiler

Profile token usage across a conversation to see what's eating your context window.

Point it at a chat export (Claude/OpenAI-style JSON) and it breaks down token
usage per message, per role, and flags what's consuming the most space.

## Install

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
```

## Usage

```bash
context-profiler path/to/conversation.json --model claude-sonnet-5 --top 10
```

Prints a total token count and percent of the model's context window used,
a per-role breakdown table, and the N heaviest individual messages.

Supported input shapes (auto-detected):
- a bare list of `{"role": ..., "content": ...}` messages (Anthropic/OpenAI
  API style), including list-of-block `content`
- `{"messages": [...]}` wrapping the same
- a claude.ai conversation export (`{"chat_messages": [{"sender": ..., "text": ...}]}`)

Run `context-profiler --help` for all options, including `--model` (see
`context_profiler/model_specs.py` for the known model list).

## Development

```bash
.venv/bin/pip install -e .
.venv/bin/pip install pytest
.venv/bin/python -m pytest tests/ -q
```

## Status

Early development — building incrementally.
