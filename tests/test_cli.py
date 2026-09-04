import json

from click.testing import CliRunner

from context_profiler.cli import main


def test_cli_runs_and_prints_summary(tmp_path):
    convo_path = tmp_path / "convo.json"
    convo_path.write_text(
        json.dumps(
            [
                {"role": "user", "content": "Hi"},
                {"role": "assistant", "content": "Hello there!"},
            ]
        )
    )
    runner = CliRunner()
    result = runner.invoke(main, [str(convo_path), "--model", "claude-sonnet-5"])
    assert result.exit_code == 0
    assert "By role" in result.output
    assert "Total:" in result.output


def test_cli_rejects_unknown_model(tmp_path):
    convo_path = tmp_path / "convo.json"
    convo_path.write_text(json.dumps([{"role": "user", "content": "Hi"}]))
    runner = CliRunner()
    result = runner.invoke(main, [str(convo_path), "--model", "not-a-model"])
    assert result.exit_code != 0


def test_cli_fail_at_exits_nonzero_when_exceeded(tmp_path):
    convo_path = tmp_path / "convo.json"
    convo_path.write_text(json.dumps([{"role": "user", "content": "Hi"}]))
    runner = CliRunner()
    # Any nonzero usage exceeds a 0% threshold.
    result = runner.invoke(main, [str(convo_path), "--fail-at", "0"])
    assert result.exit_code == 1
    assert "FAIL" in result.output


def test_cli_warn_at_does_not_change_exit_code(tmp_path):
    convo_path = tmp_path / "convo.json"
    convo_path.write_text(json.dumps([{"role": "user", "content": "Hi"}]))
    runner = CliRunner()
    result = runner.invoke(main, [str(convo_path), "--warn-at", "0"])
    assert result.exit_code == 0
    assert "WARNING" in result.output


def test_cli_no_threshold_flags_exits_zero(tmp_path):
    convo_path = tmp_path / "convo.json"
    convo_path.write_text(json.dumps([{"role": "user", "content": "Hi"}]))
    runner = CliRunner()
    result = runner.invoke(main, [str(convo_path)])
    assert result.exit_code == 0
    assert "WARNING" not in result.output
    assert "FAIL" not in result.output
