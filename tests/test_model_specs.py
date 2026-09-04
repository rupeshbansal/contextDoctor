import pytest

from context_profiler.model_specs import get_context_window


def test_known_model():
    assert get_context_window("claude-sonnet-5") == 500_000


def test_unknown_model_raises():
    with pytest.raises(KeyError):
        get_context_window("not-a-real-model")
