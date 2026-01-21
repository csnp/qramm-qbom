"""
QBOM Notebook Display

Beautiful HTML rendering for Jupyter notebooks.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qbom.core.trace import Trace


def enable_notebook() -> None:
    """Enable rich QBOM display in Jupyter notebooks."""
    try:
        from IPython import get_ipython

        ip = get_ipython()
        if ip is not None:
            # Register display hooks
            pass
    except ImportError:
        pass


def trace_to_html(trace: Trace) -> str:
    """Convert trace to beautiful HTML for Jupyter display."""
    css = """
    <style>
        .qbom-trace {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            border: 1px solid #e1e4e8;
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .qbom-trace-header {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .qbom-trace-id {
            font-family: 'SF Mono', Consolas, monospace;
            background: rgba(255,255,255,0.2);
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
        }
        .qbom-trace-body {
            background: white;
            color: #24292e;
            border-radius: 6px;
            padding: 12px;
        }
        .qbom-section {
            margin-bottom: 12px;
        }
        .qbom-section:last-child {
            margin-bottom: 0;
        }
        .qbom-section-title {
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            color: #6a737d;
            margin-bottom: 4px;
        }
        .qbom-row {
            display: flex;
            justify-content: space-between;
            padding: 2px 0;
            font-size: 13px;
        }
        .qbom-label {
            color: #586069;
        }
        .qbom-value {
            font-family: 'SF Mono', Consolas, monospace;
            color: #24292e;
        }
        .qbom-result-bar {
            height: 8px;
            background: #e1e4e8;
            border-radius: 4px;
            overflow: hidden;
            margin: 4px 0;
        }
        .qbom-result-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
        }
        .qbom-actions {
            margin-top: 12px;
            display: flex;
            gap: 8px;
        }
        .qbom-btn {
            padding: 4px 12px;
            font-size: 12px;
            border: 1px solid #e1e4e8;
            border-radius: 4px;
            background: white;
            cursor: pointer;
        }
        .qbom-btn:hover {
            background: #f6f8fa;
        }
    </style>
    """

    # Build content
    sections = []

    # Summary section
    summary = f"""
    <div class="qbom-section">
        <div class="qbom-row">
            <span class="qbom-label">Summary</span>
            <span class="qbom-value">{trace.summary}</span>
        </div>
    </div>
    """
    sections.append(summary)

    # Circuit section
    if trace.circuits:
        c = trace.circuits[0]
        sections.append(f"""
        <div class="qbom-section">
            <div class="qbom-section-title">Circuit</div>
            <div class="qbom-row">
                <span class="qbom-label">Qubits</span>
                <span class="qbom-value">{c.num_qubits}</span>
            </div>
            <div class="qbom-row">
                <span class="qbom-label">Depth</span>
                <span class="qbom-value">{c.depth}</span>
            </div>
            <div class="qbom-row">
                <span class="qbom-label">Gates</span>
                <span class="qbom-value">{c.gates.total} ({c.gates.two_qubit} 2q)</span>
            </div>
        </div>
        """)

    # Hardware section
    if trace.hardware:
        h = trace.hardware
        backend_info = f"{h.backend} (simulator)" if h.is_simulator else h.backend
        sections.append(f"""
        <div class="qbom-section">
            <div class="qbom-section-title">Hardware</div>
            <div class="qbom-row">
                <span class="qbom-label">Backend</span>
                <span class="qbom-value">{backend_info}</span>
            </div>
            <div class="qbom-row">
                <span class="qbom-label">Qubits Used</span>
                <span class="qbom-value">{h.qubits_used}</span>
            </div>
        </div>
        """)

    # Results section
    if trace.result:
        r = trace.result
        result_rows = []
        for bitstring, prob in r.counts.top_results[:4]:
            pct = prob * 100
            result_rows.append(f"""
            <div class="qbom-row">
                <span class="qbom-label">|{bitstring}⟩</span>
                <span class="qbom-value">{pct:.1f}%</span>
            </div>
            <div class="qbom-result-bar">
                <div class="qbom-result-fill" style="width: {pct}%"></div>
            </div>
            """)

        sections.append(f"""
        <div class="qbom-section">
            <div class="qbom-section-title">Results ({trace.execution.shots:,} shots)</div>
            {"".join(result_rows)}
        </div>
        """)

    html = f"""
    {css}
    <div class="qbom-trace">
        <div class="qbom-trace-header">
            <span>QBOM Trace</span>
            <span class="qbom-trace-id">{trace.id}</span>
        </div>
        <div class="qbom-trace-body">
            {"".join(sections)}
        </div>
    </div>
    """

    return html
