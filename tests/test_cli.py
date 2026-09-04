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
