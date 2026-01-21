"""
QBOM Analysis Tools.

Provides analysis capabilities for quantum experiment reproducibility:
- Reproducibility scoring (0-100)
- Calibration drift analysis
- Experiment comparison
- Trace validation
"""

from qbom.analysis.drift import (
    DriftAnalysis,
    GateDrift,
    QubitDrift,
    analyze_drift,
    explain_result_difference,
)
from qbom.analysis.score import (
    ReproducibilityScore,
    ScoreComponent,
    compute_score,
)
from qbom.analysis.validation import (
    ValidationIssue,
    ValidationLevel,
    ValidationResult,
    validate_for_publication,
    validate_trace,
)

__all__ = [
    # Scoring
    "compute_score",
    "ReproducibilityScore",
    "ScoreComponent",
    # Drift analysis
    "analyze_drift",
    "explain_result_difference",
    "DriftAnalysis",
    "QubitDrift",
    "GateDrift",
    # Validation
    "validate_trace",
    "validate_for_publication",
    "ValidationResult",
    "ValidationIssue",
    "ValidationLevel",
]
