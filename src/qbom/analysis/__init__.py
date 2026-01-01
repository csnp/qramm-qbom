"""
QBOM Analysis Tools.

Provides analysis capabilities for quantum experiment reproducibility:
- Reproducibility scoring (0-100)
- Calibration drift analysis
- Experiment comparison
- Trace validation
"""

from qbom.analysis.score import (
    compute_score,
    ReproducibilityScore,
    ScoreComponent,
)
from qbom.analysis.drift import (
    analyze_drift,
    explain_result_difference,
    DriftAnalysis,
    QubitDrift,
    GateDrift,
)
from qbom.analysis.validation import (
    validate_trace,
    validate_for_publication,
    ValidationResult,
    ValidationIssue,
    ValidationLevel,
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
