#!/usr/bin/env python3
"""
QBOM with PennyLane Example

Demonstrates QBOM capture with Xanadu's PennyLane framework.
"""

import qbom  # Import first to enable capture

import pennylane as qml
import numpy as np

# Create a device
dev = qml.device("default.qubit", wires=2, shots=4096)


# Define a QNode (quantum function)
@qml.qnode(dev)
def bell_state():
    """Create and measure a Bell state."""
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.counts()


# Run the circuit
print("Running Bell state circuit...")
result = bell_state()
print(f"Results: {result}")


# Example with parameters (VQE-style)
@qml.qnode(dev)
def variational_circuit(params):
    """A simple variational circuit."""
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=1)
    qml.CNOT(wires=[0, 1])
    qml.RZ(params[2], wires=1)
    return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1))


params = np.array([0.5, 0.7, 0.3])
expval = variational_circuit(params)
print(f"\nVariational circuit expectation value: {expval}")

# Access traces
from qbom.core.session import Session

session = Session.get()
print(f"\nCaptured {len(session._traces)} traces")

for trace in session._traces:
    print(f"  - {trace.id}: {trace.summary}")
    trace.export(f"{trace.id}.qbom.json")

print("\nAll traces exported!")
