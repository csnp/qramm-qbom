"""
Base Adapter Interface

All framework adapters implement this interface, ensuring consistent
behavior across Qiskit, Cirq, PennyLane, etc.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from qbom.core.session import Session


class Adapter(ABC):
    """
    Base class for framework adapters.

    An adapter hooks into a quantum framework to capture operations.
    Subclasses must implement install() and uninstall() methods.

    Design principles:
    - Non-invasive: Never change framework behavior
    - Graceful: Silently degrade if capture fails
    - Complete: Capture everything needed for reproducibility
    """

    name: str = "base"

    def __init__(self, session: Session) -> None:
        self.session = session
        self._installed = False
        self._original_functions: dict[str, Any] = {}

    @abstractmethod
    def install(self) -> None:
        """
        Install hooks into the framework.

        Called once when QBOM is imported and the framework is detected.
        Should wrap relevant functions to capture their inputs/outputs.
        """
        pass

    @abstractmethod
    def uninstall(self) -> None:
        """
        Remove hooks from the framework.

        Called on shutdown or when explicitly requested.
        Should restore all original function behavior.
        """
        pass

    def _wrap_function(
        self,
        module: Any,
        func_name: str,
        wrapper_factory: Any,
    ) -> None:
        """
        Safely wrap a function with a capture wrapper.

        Args:
            module: The module containing the function
            func_name: Name of the function to wrap
            wrapper_factory: Callable that takes (original_func) and returns wrapper
        """
        original = getattr(module, func_name, None)
        if original is None:
            return

        # Store original for restoration
        key = f"{module.__name__}.{func_name}"
        self._original_functions[key] = (module, func_name, original)

        # Install wrapper
        wrapper = wrapper_factory(original)
        setattr(module, func_name, wrapper)

    def _unwrap_function(self, key: str) -> None:
        """Restore original function."""
        if key in self._original_functions:
            module, func_name, original = self._original_functions[key]
            setattr(module, func_name, original)
            del self._original_functions[key]

    def _unwrap_all(self) -> None:
        """Restore all wrapped functions."""
        for key in list(self._original_functions.keys()):
            self._unwrap_function(key)
