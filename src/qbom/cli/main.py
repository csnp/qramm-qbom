"""
QBOM CLI

Beautiful command-line interface for managing quantum experiment traces.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import click
from rich.console import Console

console = Console()


@click.group()
@click.version_option(message="QBOM %(version)s")
def main() -> None:
    """
    QBOM: Quantum Bill of Materials

    Invisible provenance capture for quantum computing experiments.

    https://github.com/csnp/qbom
    """
    pass


@main.command()
@click.option("-n", "--limit", default=10, help="Number of traces to show")
def list(limit: int) -> None:
    """List recent experiment traces."""
    from qbom.cli.display import display_trace_list
    from qbom.core.session import Session

    session = Session.get()
    traces = session.list_traces(limit=limit)

    if not traces:
        console.print("[dim]No traces found. Run a quantum experiment with QBOM imported.[/dim]")
        return

    display_trace_list(traces)


@main.command()
@click.argument("trace_id")
def show(trace_id: str) -> None:
    """Show detailed view of a trace."""
    from qbom.cli.display import display_trace
    from qbom.core.session import Session
    from qbom.core.trace import Trace

    session = Session.get()

    # Find trace
    trace = None
    trace_path = session._storage_path / f"{trace_id}.json"

    if trace_path.exists():
        trace = Trace.model_validate_json(trace_path.read_text())
    else:
        # Search by partial ID
        for path in session._storage_path.glob("*.json"):
            if trace_id in path.stem:
                trace = Trace.model_validate_json(path.read_text())
                break

    if trace is None:
        console.print(f"[red]Trace not found: {trace_id}[/red]")
        return

    display_trace(trace)


@main.command()
@click.argument("trace_id")
@click.argument("output", type=click.Path())
@click.option(
    "-f",
    "--format",
    type=click.Choice(["json", "cyclonedx", "yaml"]),
    default="json",
    help="Export format",
)
def export(trace_id: str, output: str, format: str) -> None:
    """Export a trace to a file."""
    from qbom.core.session import Session
    from qbom.core.trace import Trace

    session = Session.get()
    trace_path = session._storage_path / f"{trace_id}.json"

    if not trace_path.exists():
        # Search by partial ID
        for path in session._storage_path.glob("*.json"):
            if trace_id in path.stem:
                trace_path = path
                break

    if not trace_path.exists():
        console.print(f"[red]Trace not found: {trace_id}[/red]")
        return

    trace = Trace.model_validate_json(trace_path.read_text())
    output_path = trace.export(output, format=format)  # type: ignore
    console.print(f"[green]Exported to:[/green] {output_path}")


@main.command()
@click.argument("trace_id1")
@click.argument("trace_id2")
def diff(trace_id1: str, trace_id2: str) -> None:
    """Compare two traces side by side."""
    from qbom.cli.display import display_diff
    from qbom.core.session import Session
    from qbom.core.trace import Trace

    session = Session.get()

    def load_trace(trace_id: str) -> Trace | None:
        trace_path = session._storage_path / f"{trace_id}.json"
        if trace_path.exists():
            return Trace.model_validate_json(trace_path.read_text())
        for path in session._storage_path.glob("*.json"):
            if trace_id in path.stem:
                return Trace.model_validate_json(path.read_text())
        return None

    trace1 = load_trace(trace_id1)
    trace2 = load_trace(trace_id2)

    if trace1 is None:
        console.print(f"[red]Trace not found: {trace_id1}[/red]")
        return
    if trace2 is None:
        console.print(f"[red]Trace not found: {trace_id2}[/red]")
        return

    display_diff(trace1, trace2)


@main.command()
@click.argument("trace_id")
def paper(trace_id: str) -> None:
    """Generate reproducibility statement for a paper."""
    from qbom.cli.display import generate_paper_statement
    from qbom.core.session import Session
    from qbom.core.trace import Trace

    session = Session.get()
    trace_path = session._storage_path / f"{trace_id}.json"

    if not trace_path.exists():
        for path in session._storage_path.glob("*.json"):
            if trace_id in path.stem:
                trace_path = path
                break

    if not trace_path.exists():
        console.print(f"[red]Trace not found: {trace_id}[/red]")
        return

    trace = Trace.model_validate_json(trace_path.read_text())
    statement = generate_paper_statement(trace)
    console.print(statement)


@main.command()
@click.argument("path", type=click.Path(exists=True))
def verify(path: str) -> None:
    """Verify integrity of a QBOM file."""
    from qbom.cli.display import display_verification
    from qbom.core.trace import Trace

    trace = Trace.model_validate_json(Path(path).read_text())
    display_verification(trace, path)


@main.command()
def init() -> None:
    """Initialize QBOM in the current project."""
    console.print("[bold]QBOM Initialization[/bold]\n")
    console.print("Add this to your Python scripts or notebooks:\n")
    console.print("[cyan]import qbom  # That's it![/cyan]\n")
    console.print("Your experiments will be automatically captured.")
    console.print(f"Traces stored in: [dim]~/.qbom/traces/[/dim]")


if __name__ == "__main__":
    main()
