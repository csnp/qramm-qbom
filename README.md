# QBOM - Quantum Bill of Materials

<div align="center">

**Invisible provenance capture for quantum computing experiments.**

*One import. Complete reproducibility.*

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/qbom.svg)](https://pypi.org/project/qbom/)
[![QRAMM](https://img.shields.io/badge/QRAMM-Tool-purple.svg)](https://qramm.org)

[Quick Start](#quick-start) · [Use Cases](docs/USE-CASES.md) · [Documentation](docs/) · [Why QBOM?](docs/WHY-QBOM.md) · [Contributing](#contributing)

</div>

---

## The Problem

Quantum computing experiments are notoriously difficult to reproduce. When a paper claims *"We achieved 73% fidelity on Grover's algorithm"*, reviewers and other researchers have no way to verify or reproduce the result because critical information is missing:

| What's Reported | What's Actually Needed |
|-----------------|------------------------|
| "Qiskit 1.0" | Exact versions of qiskit, qiskit-aer, numpy, scipy... |
| "IBM Brisbane" | Which of the 127 qubits? What were the error rates? |
| "4096 shots" | What optimization level? What routing algorithm? |

The result: **quantum research has a reproducibility crisis.**

## The Solution

```python
import qbom  # Add this single line

# Your existing quantum code - unchanged
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

backend = AerSimulator()
job = backend.run(qc, shots=4096)
result = job.result()

# Everything captured automatically
qbom.show()
```

**Output:**

```
╭──────────────────────────── QBOM: qbom_c4b17b13 ─────────────────────────────╮
│ Summary: 2 circuits | on aer_simulator | 4,096 shots                         │
│ Created: 2025-01-15 14:30:07 UTC                                             │
│ Hash: a9463e429a524897                                                       │
│                                                                              │
│ ENVIRONMENT                                                                  │
│   Python:  3.11.12                                                           │
│   SDK:     qiskit==2.2.3                                                     │
│   qiskit: 2.2.3, qiskit-aer: 0.17.2, numpy: 1.26.4, scipy: 1.15.3           │
│                                                                              │
│ CIRCUIT                                                                      │
│   Name: bell_state | Qubits: 2 | Depth: 3 | Gates: 5 (1 1q, 1 2q)           │
│                                                                              │
│ TRANSPILATION                                                                │
│   Optimization: Level 2 | Depth: 3 → 3 (1.0x)                               │
│                                                                              │
│ HARDWARE                                                                     │
│   Provider: Aer (Local) | Backend: aer_simulator | Type: Simulator          │
│                                                                              │
│ EXECUTION                                                                    │
│   Shots: 4,096 | Job ID: 12c28690-07fa-4248-9d05-34aa03d21ef1               │
│                                                                              │
│ RESULTS                                                                      │
│   |11⟩ ███████████████░░░░░░░░░░░░░░░  50.8%                                │
│   |00⟩ ██████████████░░░░░░░░░░░░░░░░  49.2%                                │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

## Quick Start

### Installation

```bash
# Basic installation
pip install qbom

# With Qiskit support (recommended)
pip install qbom[qiskit]

# With all quantum frameworks
pip install qbom[all]
```

### Basic Usage

```python
import qbom  # Add at the top of your script

# Your quantum code here...

# View the captured trace
qbom.show()

# Export for sharing/publication
qbom.export("my_experiment.qbom.json")
```

### Command Line

```bash
# List recent traces
qbom list

# View a specific trace
qbom show qbom_c4b17b13

# Check reproducibility score
qbom score qbom_c4b17b13

# Export to CycloneDX SBOM format
qbom export qbom_c4b17b13 experiment.cdx.json -f cyclonedx

# Generate paper reproducibility statement
qbom paper qbom_c4b17b13
```

---

## What QBOM Captures

QBOM automatically captures everything needed to reproduce a quantum experiment:

### Environment
- Python version and platform
- All quantum SDK versions (qiskit, cirq, pennylane)
- Scientific package versions (numpy, scipy)

### Circuit
- Gate counts and types
- Circuit depth
- Qubit and classical bit counts
- Content hash for verification

### Transpilation
- Optimization level
- Layout and routing methods
- Initial and final qubit mappings
- Before/after circuit comparison

### Hardware
- Provider (IBM Quantum, Aer, Google, etc.)
- Backend name and qubit count
- Calibration data (T1, T2, error rates)
- Timestamp of calibration

### Execution
- Number of shots
- Job ID for traceability
- Submission and completion times

### Results
- Raw measurement counts
- Probability distributions
- Result hash for verification

---

## Supported Frameworks

| Framework | Status | Features |
|-----------|--------|----------|
| **Qiskit** | ✅ Full Support | Circuits, transpilation, IBM backends, Aer simulator |
| **Cirq** | ✅ Supported | Circuits, simulators, Google Quantum Engine |
| **PennyLane** | ✅ Supported | QNodes, devices, gradients |
| **Braket** | 🚧 Planned | AWS quantum hardware |

---

## CLI Reference

| Command | Description |
|---------|-------------|
| `qbom list` | List recent experiment traces |
| `qbom show <id>` | Display detailed trace information |
| `qbom score <id>` | Calculate reproducibility score (0-100) |
| `qbom validate <id>` | Check trace completeness |
| `qbom diff <id1> <id2>` | Compare two traces |
| `qbom drift <id>` | Analyze calibration drift |
| `qbom export <id> <file>` | Export trace to file |
| `qbom paper <id>` | Generate reproducibility statement |
| `qbom verify <file>` | Verify trace file integrity |

---

## Export Formats

| Format | Flag | Use Case |
|--------|------|----------|
| JSON | `-f json` | Default QBOM format |
| CycloneDX | `-f cyclonedx` | SBOM compliance, supply chain tools |
| SPDX | `-f spdx` | Open source compliance |
| YAML | `-f yaml` | Human-readable alternative |

```bash
# Export examples
qbom export qbom_abc123 trace.json
qbom export qbom_abc123 trace.cdx.json -f cyclonedx
qbom export qbom_abc123 trace.spdx.json -f spdx
```

---

## Reproducibility Score

QBOM calculates a 0-100 reproducibility score based on captured information:

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | Excellent | Fully reproducible |
| 70-89 | Good | Minor details missing |
| 50-69 | Fair | Some important info missing |
| 25-49 | Poor | Major gaps |
| 0-24 | Critical | Cannot reproduce |

```bash
$ qbom score qbom_c4b17b13

╭─────────────────────────── Reproducibility Score ────────────────────────────╮
│ 71/100 (Good)                                                                │
╰──────────────────────────────────────────────────────────────────────────────╯

┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┓
┃ Component     ┃ Category              ┃ Score ┃ Status ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━┩
│ Environment   │ Software              │ 20/20 │ ●      │
│ Circuit       │ Quantum Program       │ 17/20 │ ◐      │
│ Transpilation │ Circuit Compilation   │  7/15 │ ◐      │
│ Hardware      │ Backend & Calibration │  9/25 │ ◐      │
│ Execution     │ Run Parameters        │ 10/10 │ ●      │
│ Results       │ Output Verification   │  8/10 │ ●      │
└───────────────┴───────────────────────┴───────┴────────┘
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [Use Cases](docs/USE-CASES.md) | Real-world scenarios and examples |
| [Installation Guide](docs/INSTALLATION.md) | Detailed installation instructions |
| [Usage Guide](docs/USAGE.md) | Complete usage examples |
| [CLI Reference](docs/CLI.md) | Full command-line documentation |
| [Python API](docs/API.md) | Python API reference |
| [Adapters](docs/ADAPTERS.md) | Framework adapter details |
| [Why QBOM?](docs/WHY-QBOM.md) | Background and motivation |
| [Contributing](CONTRIBUTING.md) | Contribution guidelines |

---

## Architecture

```
~/.qbom/
└── traces/                    # Local trace storage
    ├── qbom_abc123.json
    ├── qbom_def456.json
    └── ...

qbom/
├── core/                      # Framework-agnostic core
│   ├── models.py              # Pydantic data models
│   ├── trace.py               # Trace object and builder
│   └── session.py             # Global session management
├── adapters/                  # Framework-specific hooks
│   ├── qiskit.py              # Qiskit adapter
│   ├── cirq.py                # Cirq adapter
│   └── pennylane.py           # PennyLane adapter
├── analysis/                  # Analysis tools
│   ├── score.py               # Reproducibility scoring
│   ├── drift.py               # Calibration drift analysis
│   └── validation.py          # Trace validation
├── cli/                       # Command-line interface
└── notebook/                  # Jupyter integration
```

---

## How It Works

1. **Import Detection**: When you `import qbom`, it installs an import hook
2. **Framework Detection**: When quantum frameworks are imported, adapters are installed
3. **Invisible Capture**: Adapters hook into framework functions (transpile, run, etc.)
4. **Auto-Finalization**: When results are retrieved, the trace is saved
5. **Local Storage**: Traces are stored in `~/.qbom/traces/`

```python
import qbom                    # 1. Import hook installed
from qiskit import ...         # 2. Qiskit adapter installed
transpile(circuit, backend)    # 3. Transpilation captured
job = backend.run(circuit)     # 3. Execution captured
result = job.result()          # 4. Results captured, trace saved
```

---

## Use Cases

QBOM solves real problems in quantum computing research and development:

| Use Case | Problem Solved |
|----------|---------------|
| **Academic Papers** | Generate complete reproducibility statements for publications |
| **Debugging** | Quickly identify why two runs produced different results |
| **Compliance** | Export to CycloneDX/SPDX for audit trails and regulations |
| **Teaching** | Verify student submissions and compare to reference solutions |
| **Benchmarking** | Ensure fair algorithm comparisons with controlled variables |
| **Collaboration** | Share experiments with full context across institutions |

See [detailed use cases](docs/USE-CASES.md) for complete examples.

### Academic Research

Generate reproducibility statements for papers:

```bash
$ qbom paper qbom_c4b17b13

Reproducibility Statement
─────────────────────────
Experiments were performed using qiskit==2.2.3 on the aer_simulator
backend. Circuits were transpiled with optimization level 2.
Each experiment used 4,096 shots.

Complete QBOM trace: qbom_c4b17b13
Content hash: a9463e429a524897
```

### Experiment Comparison

Understand why results differ:

```bash
$ qbom diff qbom_abc123 qbom_def456

╭─────────────────────────────────────────────────────────────────────╮
│ Property           │ qbom_abc123      │ qbom_def456      │ Match   │
├────────────────────┼──────────────────┼──────────────────┼─────────┤
│ Backend            │ ibm_brisbane     │ ibm_kyoto        │ ✗       │
│ Optimization       │ 3                │ 2                │ ✗       │
│ Shots              │ 4096             │ 4096             │ ✓       │
╰─────────────────────────────────────────────────────────────────────╯
```

### Compliance & Auditing

Export to standard SBOM formats:

```bash
qbom export qbom_c4b17b13 experiment.cdx.json -f cyclonedx
qbom export qbom_c4b17b13 experiment.spdx.json -f spdx
```

---

## Part of QRAMM

QBOM is part of the [QRAMM](https://qramm.org) (Quantum Readiness Assurance Maturity Model) toolkit developed by [CSNP](https://csnp.org).

| Tool | Purpose |
|------|---------|
| **QBOM** | Quantum experiment reproducibility |
| [CryptoScan](https://github.com/csnp/cryptoscan) | Cryptographic vulnerability discovery |
| [TLS Analyzer](https://github.com/csnp/tls-analyzer) | TLS/SSL configuration analysis |

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Development setup
git clone https://github.com/csnp/qbom.git
cd qbom
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

Apache License 2.0. See [LICENSE](LICENSE) for details.

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

Made with care by [CSNP](https://csnp.org)

</div>
