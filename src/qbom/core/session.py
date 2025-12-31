"""
QBOM Session Management

The Session is the invisible orchestrator that makes QBOM magic work.
When you `import qbom`, a session is automatically started and begins
capturing quantum operations.
"""

from __future__ import annotations

import atexit
import platform
import sys
import threading
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Iterator

from qbom.core.models import Environment, Package
from qbom.core.trace import Trace, TraceBuilder

if TYPE_CHECKING:
    from qbom.adapters.base import Adapter


class Session:
    """
    Global session manager for QBOM.

    A session captures all quantum operations from import to exit.
    Sessions can be nested for scoped experiments.
    """

    _instance: Session | None = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        self._traces: list[Trace] = []
        self._current_builder: TraceBuilder | None = None
        self._adapters: list[Adapter] = []
        self._storage_path = Path.home() / ".qbom" / "traces"
        self._auto_save = True
        self._started = False

    @classmethod
    def get(cls) -> Session:
        """Get or create the global session."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @classmethod
    def auto_start(cls) -> None:
        """Auto-start session on import (called from __init__.py)."""
        session = cls.get()
        if not session._started:
            session.start()

    def start(self) -> None:
        """Start the session and install adapters."""
        if self._started:
            return

        self._started = True
        self._storage_path.mkdir(parents=True, exist_ok=True)

        # Capture initial environment
        self._current_builder = TraceBuilder()
        self._current_builder.set_environment(self._capture_environment())

        # Install framework adapters
        self._install_adapters()

        # Save traces on exit
        atexit.register(self._on_exit)

    def _capture_environment(self) -> Environment:
        """Capture current software environment."""
        packages = []

        # Get installed packages
        try:
            from importlib.metadata import distributions

            quantum_prefixes = (
                "qiskit",
                "cirq",
                "pennylane",
                "braket",
                "pytket",
                "pyquil",
            )
            for dist in distributions():
                name = dist.metadata["Name"]
                if name and any(name.lower().startswith(p) for p in quantum_prefixes):
                    packages.append(
                        Package(
                            name=name.lower(),
                            version=dist.version,
                            purl=f"pkg:pypi/{name.lower()}@{dist.version}",
                        )
                    )

            # Always include core scientific packages
            core_packages = ["numpy", "scipy"]
            for dist in distributions():
                name = dist.metadata["Name"]
                if name and name.lower() in core_packages:
                    packages.append(
                        Package(
                            name=name.lower(),
                            version=dist.version,
                            purl=f"pkg:pypi/{name.lower()}@{dist.version}",
                        )
                    )
        except Exception:
            pass  # Graceful degradation

        return Environment(
            python=platform.python_version(),
            platform=platform.platform(),
            packages=packages,
            timestamp=datetime.utcnow(),
        )

    def _install_adapters(self) -> None:
        """Detect and install available framework adapters."""
        # Import adapters lazily based on what's installed
        adapters_to_try = [
            ("qiskit", "qbom.adapters.qiskit", "QiskitAdapter"),
            ("cirq", "qbom.adapters.cirq", "CirqAdapter"),
            ("pennylane", "qbom.adapters.pennylane", "PennyLaneAdapter"),
        ]

        for module_name, adapter_module, adapter_class in adapters_to_try:
            if module_name in sys.modules:
                try:
                    import importlib

                    mod = importlib.import_module(adapter_module)
                    adapter = getattr(mod, adapter_class)(self)
                    adapter.install()
                    self._adapters.append(adapter)
                except ImportError:
                    pass  # Adapter not available

    @property
    def current_builder(self) -> TraceBuilder:
        """Get the current trace builder."""
        if self._current_builder is None:
            self._current_builder = TraceBuilder()
            self._current_builder.set_environment(self._capture_environment())
        return self._current_builder

    def finalize_trace(self) -> Trace:
        """
        Finalize and save the current trace.

        Called when an experiment completes (e.g., after job.result()).
        """
        if self._current_builder is None:
            raise RuntimeError("No active trace to finalize")

        trace = self._current_builder.build()
        self._traces.append(trace)

        if self._auto_save:
            self._save_trace(trace)

        # Start a new builder for the next experiment
        self._current_builder = TraceBuilder()
        self._current_builder.set_environment(self._capture_environment())

        return trace

    def _save_trace(self, trace: Trace) -> Path:
        """Save trace to local storage."""
        path = self._storage_path / f"{trace.id}.json"
        trace.export(path)
        return path

    def _on_exit(self) -> None:
        """Called when Python exits."""
        # Finalize any pending trace
        if self._current_builder and self._current_builder._data.get("result"):
            try:
                self.finalize_trace()
            except Exception:
                pass  # Don't raise during shutdown

        # Uninstall adapters
        for adapter in self._adapters:
            try:
                adapter.uninstall()
            except Exception:
                pass

    # ========================================================================
    # Context Manager for Scoped Experiments
    # ========================================================================

    @contextmanager
    def experiment(
        self,
        name: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
    ) -> Iterator[TraceBuilder]:
        """
        Context manager for scoped experiments.

        Example:
            with qbom.experiment("Bell State Test") as exp:
                # Your quantum code here
                pass
            # Trace is automatically finalized and saved
        """
        # Save current builder
        parent_builder = self._current_builder

        # Create new builder for this experiment
        self._current_builder = TraceBuilder()
        self._current_builder.set_environment(self._capture_environment())
        self._current_builder.set_metadata(name=name, description=description, tags=tags)

        try:
            yield self._current_builder
        finally:
            # Finalize this experiment
            if self._current_builder._data.get("result"):
                self.finalize_trace()

            # Restore parent builder
            self._current_builder = parent_builder

    # ========================================================================
    # Public API
    # ========================================================================

    def list_traces(self, limit: int = 10) -> list[Trace]:
        """List recent traces."""
        # Combine in-memory and saved traces
        traces = list(self._traces)

        # Load from disk
        if self._storage_path.exists():
            for path in sorted(self._storage_path.glob("*.json"), reverse=True):
                if len(traces) >= limit:
                    break
                try:
                    traces.append(Trace.model_validate_json(path.read_text()))
                except Exception:
                    pass

        return traces[:limit]


# ============================================================================
# Module-level convenience functions
# ============================================================================


def current() -> Trace:
    """
    Get the current trace.

    Returns the trace being built for the current experiment.
    If no experiment is in progress, returns an empty trace.
    """
    session = Session.get()
    return session.current_builder.build()


def export(path: str | Path, format: str = "json") -> Path:
    """Export the current trace to a file."""
    trace = current()
    return trace.export(path, format=format)  # type: ignore


def show() -> None:
    """Display the current trace in the terminal."""
    trace = current()
    trace.show()


@contextmanager
def experiment(
    name: str | None = None,
    description: str | None = None,
    tags: list[str] | None = None,
) -> Iterator[TraceBuilder]:
    """
    Context manager for scoped experiments.

    Example:
        import qbom

        with qbom.experiment("My Experiment") as exp:
            # Your quantum code here
            qc = QuantumCircuit(2)
            # ...

        # Trace is automatically saved
    """
    session = Session.get()
    with session.experiment(name, description, tags) as builder:
        yield builder
