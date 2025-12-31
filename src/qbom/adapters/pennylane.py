"""
PennyLane Adapter (Planned)

Captures PennyLane operations for hybrid quantum-classical workflows.
"""

from __future__ import annotations

from qbom.adapters.base import Adapter


class PennyLaneAdapter(Adapter):
    """PennyLane framework adapter (coming soon)."""

    name = "pennylane"

    def install(self) -> None:
        """Install PennyLane hooks."""
        # TODO: Implement PennyLane capture
        pass

    def uninstall(self) -> None:
        """Remove PennyLane hooks."""
        self._unwrap_all()
