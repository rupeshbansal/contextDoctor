from context_profiler.analyzer import analyze
from context_profiler.models import Conversation, Message


def _convo():
    return Conversation(
        messages=[
            Message(role="system", content="You are helpful.", index=0),
            Message(role="user", content="Hi", index=1),
            Message(role="assistant", content="Hello there, how can I help you today?", index=2),
        ]
    )


def test_analyze_sets_token_counts():
    result = analyze(_convo(), model="claude-sonnet-5")
    assert all(m.token_count > 0 for m in result.conversation.messages)
    assert result.total_tokens == sum(m.token_count for m in result.conversation.messages)


def test_percent_of_window():
    result = analyze(_convo(), model="claude-sonnet-5")
    assert 0 < result.percent_of_window < 1


def test_role_totals_sorted_descending():
    result = analyze(_convo(), model="claude-sonnet-5")
    totals = result.role_totals()
    tokens = [t.tokens for t in totals]
    assert tokens == sorted(tokens, reverse=True)
    assert sum(t.message_count for t in totals) == 3


def test_top_messages_limits_and_sorts():
    result = analyze(_convo(), model="claude-sonnet-5")
    top = result.top_messages(n=1)
    assert len(top) == 1
    assert top[0].role == "assistant"
