"""
Cirq Adapter (Planned)

Captures Cirq operations for Google quantum hardware.
"""

from __future__ import annotations

from qbom.adapters.base import Adapter


class CirqAdapter(Adapter):
    """Cirq framework adapter (coming soon)."""

    name = "cirq"

    def install(self) -> None:
        """Install Cirq hooks."""
        # TODO: Implement Cirq capture
        pass

    def uninstall(self) -> None:
        """Remove Cirq hooks."""
        self._unwrap_all()
