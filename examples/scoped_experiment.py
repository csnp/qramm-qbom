#!/usr/bin/env python3
"""
QBOM Scoped Experiment Example

Use qbom.experiment() for explicit experiment boundaries with metadata.
"""

import qbom

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

backend = AerSimulator()


def run_grover_iteration(n_qubits: int, shots: int = 1024):
    """Run a simple Grover iteration."""
    qc = QuantumCircuit(n_qubits, n_qubits)

    # Initialize superposition
    qc.h(range(n_qubits))

    # Oracle (mark |11...1⟩)
    qc.x(range(n_qubits))
    qc.h(n_qubits - 1)
    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    qc.h(n_qubits - 1)
    qc.x(range(n_qubits))

    # Diffusion
    qc.h(range(n_qubits))
    qc.x(range(n_qubits))
    qc.h(n_qubits - 1)
    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    qc.h(n_qubits - 1)
    qc.x(range(n_qubits))
    qc.h(range(n_qubits))

    qc.measure_all()

    transpiled = transpile(qc, backend)
    job = backend.run(transpiled, shots=shots)
    return job.result().get_counts()


# Run experiments with explicit scoping and metadata
with qbom.experiment(
    name="Grover 3-qubit",
    description="Testing Grover's algorithm on 3 qubits",
    tags=["grover", "search", "benchmark"],
) as exp:
    counts = run_grover_iteration(3, shots=4096)
    print(f"3-qubit Grover: {counts}")


with qbom.experiment(
    name="Grover 4-qubit",
    description="Testing Grover's algorithm on 4 qubits",
    tags=["grover", "search", "benchmark"],
) as exp:
    counts = run_grover_iteration(4, shots=4096)
    print(f"4-qubit Grover: {counts}")


# List all traces from this session
from qbom.core.session import Session

session = Session.get()
print("\nAll traces from this session:")
for trace in session._traces:
    print(f"  - {trace.id}: {trace.metadata.name}")
