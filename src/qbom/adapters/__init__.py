"""
QBOM Framework Adapters

Each adapter hooks into a specific quantum framework to capture
operations invisibly. The adapter pattern keeps QBOM framework-agnostic.
"""

from qbom.adapters.base import Adapter

__all__ = ["Adapter"]
