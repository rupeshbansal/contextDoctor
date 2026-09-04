from context_profiler.tokenizer import count_tokens


def test_empty_string_is_zero_tokens():
    assert count_tokens("") == 0


def test_known_short_string():
    assert count_tokens("hello world") == 2


def test_longer_text_has_more_tokens_than_shorter():
    short = count_tokens("hi")
    long = count_tokens("hi " * 50)
    assert long > short
