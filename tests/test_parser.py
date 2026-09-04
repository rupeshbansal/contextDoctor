import json

import pytest

from context_profiler.parser import load_conversation, parse_conversation


def test_parse_generic_list():
    data = [
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello!"},
    ]
    convo = parse_conversation(data)
    assert [m.role for m in convo.messages] == ["system", "user", "assistant"]
    assert convo.messages[1].content == "Hi"


def test_parse_generic_wrapped_in_messages_key():
    data = {"messages": [{"role": "user", "content": "Hi"}]}
    convo = parse_conversation(data)
    assert len(convo.messages) == 1


def test_parse_content_blocks():
    data = [{"role": "user", "content": [{"type": "text", "text": "part one"}, {"type": "text", "text": "part two"}]}]
    convo = parse_conversation(data)
    assert convo.messages[0].content == "part one\npart two"


def test_parse_claude_export():
    data = {
        "name": "Some chat",
        "chat_messages": [
            {"sender": "human", "text": "Hi"},
            {"sender": "assistant", "text": "Hello!"},
        ],
    }
    convo = parse_conversation(data)
    assert [m.role for m in convo.messages] == ["user", "assistant"]


def test_unrecognized_format_raises():
    with pytest.raises(ValueError):
        parse_conversation({"foo": "bar"})


def test_load_conversation_from_file(tmp_path):
    path = tmp_path / "convo.json"
    path.write_text(json.dumps([{"role": "user", "content": "Hi"}]))
    convo = load_conversation(path)
    assert convo.source_path == str(path)
    assert len(convo.messages) == 1
