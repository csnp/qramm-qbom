# Installation Guide

This guide covers all installation options for QBOM.

## Requirements

- Python 3.10 or higher
- pip (Python package manager)

## Quick Install

```bash
pip install qbom
```

## Installation with Framework Support

QBOM provides optional dependencies for each quantum framework:

### Qiskit (Recommended)

```bash
pip install qbom[qiskit]
```

This installs:
- qbom
- qiskit >= 1.0.0

### Cirq

```bash
pip install qbom[cirq]
```

This installs:
- qbom
- cirq >= 1.0.0

### PennyLane

```bash
pip install qbom[pennylane]
```

This installs:
- qbom
- pennylane >= 0.30.0

### All Frameworks

```bash
pip install qbom[all]
```

This installs qbom with support for all quantum frameworks.

## Development Installation

For contributing to QBOM:

```bash
# Clone the repository
git clone https://github.com/csnp/qbom.git
cd qbom

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install with all frameworks for testing
pip install -e ".[dev,all]"
```

Development dependencies include:
- pytest >= 7.0.0
- pytest-cov >= 4.0.0
- ruff >= 0.1.0
- mypy >= 1.0.0

## Verifying Installation

After installation, verify QBOM is working:

```bash
# Check version
qbom --version

# Check CLI is accessible
qbom --help
```

In Python:

```python
import qbom
print(qbom.__version__)
```

## Trace Storage Location

QBOM stores traces in your home directory:

```
~/.qbom/
└── traces/
    ├── qbom_abc123.json
    ├── qbom_def456.json
    └── ...
```

This directory is created automatically on first use.

## Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade qbom
```

## Uninstalling

```bash
pip uninstall qbom
```

Note: This does not remove stored traces. To remove all data:

```bash
rm -rf ~/.qbom
```

## Troubleshooting

### Import Errors

If you get import errors, ensure you have the correct Python version:

```bash
python --version  # Should be 3.10+
```

### Framework Not Detected

If QBOM doesn't capture your quantum framework operations, ensure:

1. `import qbom` appears **before** your framework imports
2. The framework is installed with qbom: `pip install qbom[qiskit]`

```python
# Correct order
import qbom
from qiskit import QuantumCircuit

# Incorrect order (may miss some operations)
from qiskit import QuantumCircuit
import qbom
```

### Permission Errors

If you get permission errors writing traces:

```bash
# Check permissions on trace directory
ls -la ~/.qbom/

# Fix permissions if needed
chmod 755 ~/.qbom
chmod 755 ~/.qbom/traces
```

## Next Steps

- [Usage Guide](USAGE.md) - Learn how to use QBOM
- [CLI Reference](CLI.md) - Command-line documentation
- [API Reference](API.md) - Python API documentation
