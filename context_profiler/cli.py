"""CLI entry point: `context-profiler <file> [--model ...] [--top N]`."""

from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

from context_profiler.analyzer import AnalysisResult, analyze
from context_profiler.model_specs import CONTEXT_WINDOWS, DEFAULT_MODEL
from context_profiler.parser import load_conversation

console = Console()


def _render(result: AnalysisResult, top_n: int) -> None:
    console.print(
        f"\n[bold]{result.conversation.source_path}[/bold]  "
        f"model=[cyan]{result.model}[/cyan]"
    )
    console.print(
        f"Total: [bold]{result.total_tokens:,}[/bold] tokens "
        f"({result.percent_of_window:.1f}% of {result.context_window:,} window)\n"
    )

    role_table = Table(title="By role")
    role_table.add_column("Role")
    role_table.add_column("Messages", justify="right")
    role_table.add_column("Tokens", justify="right")
    role_table.add_column("% of total", justify="right")
    for rt in result.role_totals():
        pct = 100 * rt.tokens / result.total_tokens if result.total_tokens else 0
        role_table.add_row(rt.role, str(rt.message_count), f"{rt.tokens:,}", f"{pct:.1f}%")
    console.print(role_table)

    top_table = Table(title=f"Top {top_n} heaviest messages")
    top_table.add_column("#", justify="right")
    top_table.add_column("Role")
    top_table.add_column("Tokens", justify="right")
    top_table.add_column("Preview")
    for m in result.top_messages(top_n):
        preview = m.content.replace("\n", " ").strip()
        if len(preview) > 60:
            preview = preview[:57] + "..."
        top_table.add_row(str(m.index), m.role, f"{m.token_count:,}", preview)
    console.print(top_table)


@click.command()
@click.argument("path", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--model",
    default=DEFAULT_MODEL,
    show_default=True,
    type=click.Choice(sorted(CONTEXT_WINDOWS)),
    help="Model to compute context window usage against.",
)
@click.option("--top", "top_n", default=10, show_default=True, help="Number of heaviest messages to show.")
def main(path: str, model: str, top_n: int) -> None:
    """Profile token usage in a conversation export at PATH."""
    conversation = load_conversation(path)
    result = analyze(conversation, model=model)
    _render(result, top_n)


if __name__ == "__main__":
    main()
