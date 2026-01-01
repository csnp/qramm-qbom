# QBOM

**Invisible Provenance Capture for Quantum Computing Experiments**

*One import. Complete reproducibility. Zero code changes.*

[![CI](https://github.com/csnp/qramm-qbom/actions/workflows/ci.yml/badge.svg)](https://github.com/csnp/qramm-qbom/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/csnp/qramm-qbom/graph/badge.svg)](https://codecov.io/gh/csnp/qramm-qbom)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)

[Why QBOM](#why-qbom) • [Quick Start](#quick-start) • [Features](#features) • [Documentation](#documentation) • [Contributing](#contributing)

---

## The Quantum Reproducibility Crisis

Quantum computing experiments are notoriously difficult to reproduce. When a paper claims *"We achieved 73% fidelity on Grover's algorithm"*, reviewers and researchers have no way to verify or reproduce the result because critical information is missing:

| What's Reported | What's Actually Needed |
|-----------------|------------------------|
| "Qiskit 1.0" | Exact versions of qiskit, qiskit-aer, numpy, scipy... |
| "IBM Brisbane" | Which of the 127 qubits? What were the error rates? |
| "4096 shots" | What optimization level? What routing algorithm? |

**The challenge?** You can't reproduce what you can't document.

QBOM solves this by automatically capturing complete experiment provenance—with zero code changes required.

---

## Why QBOM

| Capability | QBOM | Manual Logging | Notebooks |
|------------|------|----------------|-----------|
| Zero code changes | Yes | No | No |
| Automatic capture | Yes | No | No |
| Calibration data (T1, T2, error rates) | Yes | Rarely | Rarely |
| Transpilation details | Yes | Often forgotten | Often forgotten |
| Content verification (hashing) | Yes | No | No |
| SBOM export (CycloneDX/SPDX) | Yes | No | No |
| Reproducibility scoring | Yes | No | No |
| Multi-framework support | Yes | Custom | Custom |

---

## Quick Start

### Installation

Requires Python 3.10+ ([install Python](https://python.org))

**Copy and paste this entire block:**

```bash
git clone https://github.com/csnp/qramm-qbom.git
cd qramm-qbom
pip install -e ".[qiskit]"
qbom --version
```

**Framework options:**

```bash
pip install -e ".[qiskit]"      # Qiskit support
pip install -e ".[cirq]"        # Cirq support
pip install -e ".[pennylane]"   # PennyLane support
pip install -e ".[all]"         # All frameworks
```

### Basic Usage

```python
import qbom  # Add this single line - that's it!

# Your existing quantum code - unchanged
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

backend = AerSimulator()
job = backend.run(qc, shots=4096)
result = job.result()

# View what was captured
qbom.show()
```

**Output:**

```
╭──────────────────────────── QBOM: qbom_c4b17b13 ─────────────────────────────╮
│ Summary: 2 circuits | on aer_simulator | 4,096 shots                         │
│ Created: 2025-01-15 14:30:07 UTC                                             │
│                                                                              │
│ ENVIRONMENT                                                                  │
│   Python:  3.11.12                                                           │
│   qiskit: 2.2.3, qiskit-aer: 0.17.2, numpy: 1.26.4                          │
│                                                                              │
│ CIRCUIT                                                                      │
│   Name: bell_state | Qubits: 2 | Depth: 3 | Gates: 5                        │
│                                                                              │
│ HARDWARE                                                                     │
│   Backend: aer_simulator | Type: Simulator                                   │
│                                                                              │
│ EXECUTION                                                                    │
│   Shots: 4,096                                                               │
│                                                                              │
│ RESULTS                                                                      │
│   |11⟩ ███████████████░░░░░░░░░░░░░░░  50.8%                                │
│   |00⟩ ██████████████░░░░░░░░░░░░░░░░  49.2%                                │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### Try It Out

```bash
# Run the included example
python examples/basic_usage.py

# List captured traces
qbom list

# View a trace
qbom show <trace-id>

# Check reproducibility score
qbom score <trace-id>
```

---

## Features

### What QBOM Captures

| Category | What's Captured |
|----------|-----------------|
| **Environment** | Python version, all package versions |
| **Circuit** | Gates, depth, qubits, content hash |
| **Transpilation** | Optimization level, qubit mapping, routing |
| **Hardware** | Backend, calibration (T1, T2, error rates) |
| **Execution** | Shots, job ID, timestamps |
| **Results** | Counts, probabilities, result hash |

### Supported Frameworks

| Framework | Status |
|-----------|--------|
| **Qiskit** | Full support |
| **Cirq** | Supported |
| **PennyLane** | Supported |
| **Braket** | Planned |

### Reproducibility Score

QBOM calculates a 0-100 score showing how reproducible your experiment is:

| Score | Meaning |
|-------|---------|
| 90-100 | Excellent - fully reproducible |
| 70-89 | Good - minor details missing |
| 50-69 | Fair - some info missing |
| 25-49 | Poor - major gaps |
| 0-24 | Critical - cannot reproduce |

```bash
$ qbom score qbom_c4b17b13

╭─────────────────────────── Reproducibility Score ────────────────────────────╮
│ 71/100 (Good)                                                                │
╰──────────────────────────────────────────────────────────────────────────────╯

┏━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┓
┃ Component     ┃ Score ┃ Status ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━┩
│ Environment   │ 20/20 │ ●      │
│ Circuit       │ 17/20 │ ◐      │
│ Transpilation │  7/15 │ ◐      │
│ Hardware      │  9/25 │ ◐      │
│ Execution     │ 10/10 │ ●      │
│ Results       │  8/10 │ ●      │
└───────────────┴───────┴────────┘
```

### Export Formats

```bash
qbom export <id> trace.json              # JSON (default)
qbom export <id> trace.cdx.json -f cyclonedx   # CycloneDX SBOM
qbom export <id> trace.spdx.json -f spdx       # SPDX SBOM
qbom export <id> trace.yaml -f yaml            # YAML
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [Installation](docs/INSTALLATION.md) | Detailed installation guide |
| [Usage Guide](docs/USAGE.md) | Complete usage examples |
| [CLI Reference](docs/CLI.md) | All commands and options |
| [Python API](docs/API.md) | Python API reference |
| [Adapters](docs/ADAPTERS.md) | Framework adapter details |
| [Use Cases](docs/USE-CASES.md) | Real-world scenarios |
| [Why QBOM?](docs/WHY-QBOM.md) | Background and motivation |

### CLI Reference

```
qbom list                     List recent traces
qbom show <id>                Display trace details
qbom score <id>               Calculate reproducibility score
qbom validate <id>            Check trace completeness
qbom diff <id1> <id2>         Compare two traces
qbom drift <id>               Analyze calibration drift
qbom export <id> <file>       Export to file
qbom paper <id>               Generate paper statement
qbom verify <file>            Verify trace integrity
```

### Python API

```python
import qbom

# View current trace
qbom.show()

# Get trace object
trace = qbom.current()
print(trace.environment.packages)
print(trace.hardware.backend_name)

# Export
qbom.export("experiment.json")

# Scoped experiments
with qbom.experiment(name="VQE optimization"):
    # quantum code here
    pass
```

---

## How It Works

```python
import qbom                    # 1. Import hook installed
from qiskit import ...         # 2. Qiskit adapter activates
transpile(circuit, backend)    # 3. Transpilation captured
job = backend.run(circuit)     # 4. Execution captured
result = job.result()          # 5. Results captured, trace saved
```

Traces are stored in `~/.qbom/traces/`.

---

## Architecture

```
qramm-qbom/
├── src/qbom/
│   ├── core/           # Data models, trace builder, session
│   ├── adapters/       # Qiskit, Cirq, PennyLane hooks
│   ├── analysis/       # Scoring, drift, validation
│   ├── cli/            # Command-line interface
│   └── notebook/       # Jupyter integration
├── docs/               # Documentation
├── examples/           # Example scripts
└── tests/              # Test suite
```

---

## Roadmap

### v0.1 (Current)
- [x] Zero-code provenance capture
- [x] Qiskit, Cirq, PennyLane support
- [x] Reproducibility scoring
- [x] CycloneDX/SPDX export
- [x] CLI and Jupyter integration

### v0.2 (Next)
- [ ] AWS Braket adapter
- [ ] Enhanced drift analysis
- [ ] Remote trace storage

### v1.0 (Future)
- [ ] IonQ and Rigetti adapters
- [ ] Web dashboard
- [ ] Team collaboration

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Development setup
git clone https://github.com/csnp/qramm-qbom.git
cd qramm-qbom
pip install -e ".[dev,all]"

# Run tests
pytest

# Type check and lint
mypy src/qbom
ruff check src/qbom
```

---

## About CSNP

QBOM is developed by the [CyberSecurity NonProfit (CSNP)](https://csnp.org), a 501(c)(3) organization dedicated to making cybersecurity knowledge accessible to everyone.

### QRAMM Toolkit

QBOM is part of the [QRAMM](https://qramm.org) (Quantum Readiness Assurance Maturity Model) toolkit:

| Tool | Purpose |
|------|---------|
| **QBOM** | Quantum experiment reproducibility |
| [CryptoScan](https://github.com/csnp/qramm-cryptoscan) | Cryptographic vulnerability discovery |
| [TLS Analyzer](https://github.com/csnp/qramm-tls-analyzer) | TLS/SSL configuration analysis |

---

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.

Copyright 2025 CyberSecurity NonProfit (CSNP)

---

## Citation

```bibtex
@software{qbom2025,
  title = {QBOM: Quantum Bill of Materials},
  author = {{CyberSecurity NonProfit (CSNP)}},
  year = {2025},
  url = {https://github.com/csnp/qramm-qbom}
}
```

---

<div align="center">

**Built with purpose by [CSNP](https://csnp.org)** — Advancing cybersecurity for everyone

[QRAMM](https://qramm.org) • [CSNP](https://csnp.org) • [Issues](https://github.com/csnp/qramm-qbom/issues)

</div>
