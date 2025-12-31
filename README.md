# QBOM

## Quantum Bill of Materials

<div align="center">

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)
[![QRAMM](https://img.shields.io/badge/QRAMM-Tool-purple.svg)](https://qramm.org)

**Invisible provenance capture for quantum computing experiments.**

One import. Complete reproducibility.

[Specification](#specification) · [Quick Start](#quick-start) · [Documentation](#documentation) · [Contributing](#contributing)

</div>

---

## The Problem

Quantum experiments are unreproducible.

```
Paper says: "We achieved 73% fidelity on Grover's algorithm"

Reviewer: "I got 41%. What qubits? What transpiler? What calibration?"
```

To reproduce a quantum experiment, you need to know:

- **Software**: Qiskit version, all dependencies, Python version
- **Circuit**: Exact gate sequence, how it was constructed
- **Transpilation**: Optimization level, routing algorithm, qubit mapping
- **Hardware**: Which backend, which physical qubits, calibration at that moment
- **Execution**: Number of shots, error mitigation method

What papers typically report: *"We used Qiskit 1.0 on IBM Brisbane, 4096 shots"*

Everything else? **Lost.**

## The Solution

```python
import qbom  # That's it. Everything is now captured.

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")
transpiled = transpile(qc, backend)
job = backend.run(transpiled, shots=4096)
result = job.result()

# Everything automatically captured!
trace = qbom.current()
trace.export("experiment.qbom.json")
```

**The magic:** Import a library. Change nothing else. Get complete provenance.

---

## What QBOM Captures

```
┌─────────────────────────────────────────────────────────────────────┐
│ QBOM TRACE                                                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ENVIRONMENT          CIRCUIT              TRANSPILATION            │
│  ─────────────        ───────              ─────────────            │
│  Python 3.11.5        Bell State           Optimization: 3          │
│  qiskit 1.0.2         2 qubits             Layout: SABRE            │
│  numpy 1.24.0         depth 2              Routing: SABRE           │
│                       2 gates              Depth: 2 → 5             │
│                                                                     │
│  HARDWARE             EXECUTION            RESULTS                  │
│  ────────             ─────────            ───────                  │
│  ibm_brisbane         4,096 shots          |00⟩: 49.2%              │
│  Qubits: [12, 15]     Job: cq8x7k2j9f      |11⟩: 48.7%              │
│  CX error: 0.82%      Time: 2.3s           other: 2.1%              │
│  T1: 145μs, 132μs                                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Calibration Snapshots

QBOM captures hardware calibration **at the moment of execution**—critical data that changes daily and is otherwise lost forever.

```
Calibration: 2025-01-15T06:00:00Z
├── Qubit 12: T1=145μs, T2=98μs, readout_error=1.8%
├── Qubit 15: T1=132μs, T2=89μs, readout_error=2.1%
└── CX(12,15): error=0.82%, duration=340ns
```

---

## Quick Start

### Installation

```bash
pip install qbom

# With Qiskit support (recommended)
pip install qbom[qiskit]

# With all frameworks
pip install qbom[all]
```

### Usage

```python
import qbom  # Add this line to your script

# Your existing quantum code works exactly as before
# QBOM captures everything invisibly

# View current trace
qbom.show()

# Export for paper/reproducibility
qbom.export("experiment.qbom.json")
```

### CLI

```bash
# List recent traces
qbom list

# View a trace
qbom show qbom_7x8k2mf9

# Compare two traces
qbom diff qbom_7x8k2mf9 qbom_3j9x1kp2

# Generate paper statement
qbom paper qbom_7x8k2mf9

# Export as CycloneDX SBOM
qbom export qbom_7x8k2mf9 experiment.cdx.json -f cyclonedx
```

---

## Specification

QBOM defines an open specification for quantum experiment provenance.

**[QBOM Specification v1.0](docs/specs/qbom-spec-1.0.json)** — JSON Schema

### Design Principles

1. **Framework-agnostic** — Works with Qiskit, Cirq, PennyLane, and more
2. **Invisible capture** — Scientists don't change their workflow
3. **CycloneDX compatible** — Extends the SBOM standard for quantum
4. **Content-addressable** — Every trace has a verifiable hash
5. **Calibration-as-dependency** — Hardware state is a captured dependency

### Export Formats

| Format | Use Case |
|--------|----------|
| `json` | Default QBOM format for storage and sharing |
| `cyclonedx` | CycloneDX SBOM with QBOM extension for compliance |
| `yaml` | Human-readable alternative |

---

## Framework Support

| Framework | Status | Adapter |
|-----------|--------|---------|
| **Qiskit** | ✅ Supported | Full capture including IBM calibration |
| **Cirq** | 🚧 Planned | Coming soon |
| **PennyLane** | 🚧 Planned | Coming soon |
| **Braket** | 🚧 Planned | Coming soon |

---

## Use Cases

### Academic Reproducibility

Generate reproducibility statements for your papers:

```bash
$ qbom paper qbom_7x8k2mf9

Reproducibility Statement
(For Methods section)

Experiments were performed using qiskit==1.0.2 on the IBM Quantum
ibm_brisbane quantum processor (127 qubits). Circuits were transpiled
with optimization level 3. Each experiment used 4,096 shots. Hardware
calibration data from 2025-01-15T06:00:00Z was used.

Complete QBOM trace: qbom_7x8k2mf9
Content hash: 3c7a2b1f9e8d4a5b
```

### Experiment Comparison

Understand why results differ:

```bash
$ qbom diff qbom_7x8k2mf9 qbom_3j9x1kp2

╭─────────────────────────────────────────────────────────────────────╮
│ Property              │ qbom_7x8k2mf9    │ qbom_3j9x1kp2    │ Match │
├───────────────────────┼──────────────────┼──────────────────┼───────┤
│ Backend               │ ibm_brisbane     │ ibm_kyoto        │ ✗     │
│ Physical qubits       │ [12, 15]         │ [0, 1]           │ ✗     │
│ Optimization level    │ 3                │ 2                │ ✗     │
│ Shots                 │ 4096             │ 4096             │ ✓     │
╰─────────────────────────────────────────────────────────────────────╯

⚠ Different backends may explain result differences
```

### Jupyter Notebooks

Rich display in notebooks:

```python
import qbom
qbom.current()  # Beautiful inline visualization
```

---

## Architecture

```
qbom/
├── core/           # Framework-agnostic models and session
│   ├── models.py   # Pydantic data models
│   ├── trace.py    # QBOM trace object
│   └── session.py  # Global session management
│
├── adapters/       # Framework-specific capture
│   ├── qiskit.py   # Qiskit hooks
│   ├── cirq.py     # Cirq hooks (planned)
│   └── pennylane.py # PennyLane hooks (planned)
│
├── cli/            # Command-line interface
└── notebook/       # Jupyter integration
```

### How It Works

1. **On import**: QBOM detects installed quantum frameworks
2. **Hook installation**: Transparent hooks capture operations
3. **Invisible capture**: Circuit, transpilation, execution captured
4. **Auto-finalize**: Trace saved when job completes
5. **Local storage**: Traces stored in `~/.qbom/traces/`

---

## Part of QRAMM

QBOM is part of the [QRAMM](https://qramm.org) (Quantum Readiness Assurance Maturity Model) toolkit by [CSNP](https://csnp.org).

| Tool | Purpose |
|------|---------|
| **QBOM** | Quantum experiment reproducibility |
| [CryptoScan](https://github.com/csnp/qramm-cryptoscan) | Cryptographic vulnerability discovery |
| [TLS Analyzer](https://github.com/csnp/qramm-tls-analyzer) | TLS/SSL configuration analysis |
| [CryptoDeps](https://github.com/csnp/qramm-cryptodeps) | Dependency cryptography analysis |

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development

```bash
# Clone
git clone https://github.com/csnp/qbom.git
cd qbom

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type check
mypy src/qbom

# Lint
ruff check src/qbom
```

---

## License

Apache License 2.0

---

## Citation

```bibtex
@software{qbom2025,
  title = {QBOM: Quantum Bill of Materials},
  author = {CyberSecurity NonProfit (CSNP)},
  year = {2025},
  url = {https://github.com/csnp/qbom},
  note = {Part of the QRAMM toolkit}
}
```

---

<div align="center">

**QBOM** — Because quantum experiments should be reproducible.

Made with ❤️ by [CSNP](https://csnp.org)

</div>
