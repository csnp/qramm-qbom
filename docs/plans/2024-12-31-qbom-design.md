# QBOM Design Document

**Status:** Implementation Complete (Phase 1)
**Author:** CSNP
**Date:** December 2024

---

## Executive Summary

QBOM (Quantum Bill of Materials) applies the Software Bill of Materials concept to quantum computing workflows. It invisibly captures everything about a quantum experiment—software, circuit, transpilation, hardware calibration, execution, and results—enabling reproducibility and scientific integrity.

**The Problem:** Quantum experiments are unreproducible. Papers say "we used Qiskit on IBM hardware" but omit the 50 parameters needed to actually reproduce.

**The Solution:** Automatic, invisible capture of complete experiment provenance.

---

## Design Decisions

### 1. Framework-Agnostic Core

We chose to build a framework-agnostic core with adapters for specific frameworks:

- **Core Models** (`qbom/core/`): Pydantic models that work with any quantum framework
- **Adapters** (`qbom/adapters/`): Framework-specific capture logic

This positions CSNP as the authority on quantum reproducibility standards, not just "IBM's tool."

### 2. Invisible Capture

The key insight: scientists won't change their workflow to log data. So we capture it invisibly:

```python
import qbom  # That's it.
```

Implementation:
- Auto-detection of installed quantum frameworks on import
- Hook installation via function wrapping (not monkey-patching globals)
- Graceful degradation if capture fails

### 3. CycloneDX Compatibility

QBOM exports to CycloneDX format with a QBOM extension, enabling:
- Standards compliance
- Tool interoperability
- Future standardization path

### 4. Content-Addressable Traces

Each trace has a `content_hash` derived from scientific content:
- Circuit hashes
- Hardware configuration
- Execution parameters
- Result hashes

This enables verification that results haven't been tampered with.

---

## Architecture

```
qbom/
├── core/               # Framework-agnostic
│   ├── models.py       # Pydantic data models
│   ├── trace.py        # Trace object and builder
│   └── session.py      # Global session management
│
├── adapters/           # Framework-specific
│   ├── base.py         # Adapter interface
│   ├── qiskit.py       # Qiskit hooks (implemented)
│   ├── cirq.py         # Cirq hooks (stub)
│   └── pennylane.py    # PennyLane hooks (stub)
│
├── cli/                # Command-line interface
│   ├── main.py         # Click commands
│   └── display.py      # Rich formatting
│
└── notebook/           # Jupyter integration
    └── display.py      # HTML rendering
```

---

## Implementation Status

### Phase 1 (Complete)
- [x] Core QBOM models (Pydantic)
- [x] Trace object with export
- [x] Session management
- [x] Qiskit adapter
- [x] Beautiful CLI
- [x] JSON Schema specification

### Phase 2 (Planned)
- [ ] Cirq adapter
- [ ] PennyLane adapter
- [ ] Enhanced calibration drift analysis
- [ ] Experiment bundles

### Phase 3 (Planned)
- [ ] CycloneDX proposal submission
- [ ] Academic paper
- [ ] Journal reproducibility requirements

---

## Key Files

| File | Purpose |
|------|---------|
| `src/qbom/__init__.py` | Entry point, auto-starts session |
| `src/qbom/core/trace.py` | Main Trace model |
| `src/qbom/core/models.py` | All data models |
| `src/qbom/adapters/qiskit.py` | Qiskit capture hooks |
| `docs/specs/qbom-spec-1.0.json` | JSON Schema specification |

---

## Usage

```python
import qbom

# Your quantum code here...

trace = qbom.current()
trace.export("experiment.qbom.json")
```

CLI:
```bash
qbom list
qbom show qbom_xxxxxxxx
qbom export qbom_xxxxxxxx output.json
qbom paper qbom_xxxxxxxx
```

---

## Standards Strategy

1. **Publish spec** — JSON Schema available at `docs/specs/qbom-spec-1.0.json`
2. **Community adoption** — Get researchers using it in papers
3. **Provider engagement** — Work with IBM/Google/AWS on calibration data
4. **CycloneDX proposal** — Submit as official extension
5. **Academic requirements** — Encourage journals to require QBOMs
