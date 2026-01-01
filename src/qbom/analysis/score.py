"""
QBOM Reproducibility Score

Computes a 0-100 score indicating how reproducible an experiment is.
Higher scores mean better documentation and easier reproduction.

The score is based on what information was captured:
- Environment completeness
- Circuit documentation
- Transpilation records
- Hardware calibration
- Execution parameters
- Result verification

This helps researchers understand:
- "Is my experiment well-documented?"
- "What am I missing?"
- "Can someone else reproduce this?"
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qbom.core.trace import Trace


@dataclass
class ScoreComponent:
    """A single component of the reproducibility score."""

    name: str
    category: str
    max_points: int
    earned_points: int
    status: str  # "complete", "partial", "missing"
    recommendation: str | None = None

    @property
    def percentage(self) -> float:
        if self.max_points == 0:
            return 100.0
        return (self.earned_points / self.max_points) * 100


@dataclass
class ReproducibilityScore:
    """
    Complete reproducibility score for a QBOM trace.

    The score ranges from 0-100:
    - 90-100: Excellent - Fully reproducible
    - 70-89:  Good - Minor details missing
    - 50-69:  Fair - Some important info missing
    - 25-49:  Poor - Major gaps in documentation
    - 0-24:   Critical - Cannot reproduce

    Each category contributes to the total:
    - Environment (20 points): Software versions
    - Circuit (20 points): Circuit definition
    - Transpilation (15 points): How circuit was compiled
    - Hardware (25 points): Backend and calibration
    - Execution (10 points): Run parameters
    - Results (10 points): Output verification
    """

    total_score: int
    max_score: int
    grade: str
    components: list[ScoreComponent]
    recommendations: list[str]

    @property
    def percentage(self) -> float:
        return (self.total_score / self.max_score) * 100

    @property
    def is_reproducible(self) -> bool:
        """True if score >= 70 (Good or better)."""
        return self.percentage >= 70

    def summary(self) -> str:
        """Human-readable summary."""
        return f"{self.total_score}/{self.max_score} ({self.grade})"


def compute_score(trace: Trace) -> ReproducibilityScore:
    """
    Compute the reproducibility score for a trace.

    Returns a detailed breakdown of what's captured and what's missing.
    """
    components: list[ScoreComponent] = []
    recommendations: list[str] = []

    # =========================================================================
    # ENVIRONMENT (20 points)
    # =========================================================================
    env_points = 0
    env_max = 20

    if trace.environment:
        env = trace.environment
        # Python version (5 points)
        if env.python:
            env_points += 5

        # Quantum SDK detected (8 points)
        if env.quantum_sdk:
            env_points += 8
        else:
            recommendations.append("Install a quantum SDK (qiskit, cirq, pennylane) for better tracking")

        # Multiple packages tracked (7 points)
        if len(env.packages) >= 3:
            env_points += 7
        elif len(env.packages) >= 1:
            env_points += 4
        else:
            recommendations.append("Package versions not captured - reproducibility limited")

        status = "complete" if env_points >= 18 else "partial" if env_points > 0 else "missing"
    else:
        status = "missing"
        recommendations.append("No environment captured - cannot reproduce software setup")

    components.append(ScoreComponent(
        name="Environment",
        category="Software",
        max_points=env_max,
        earned_points=env_points,
        status=status,
        recommendation="Captures Python version and package dependencies" if status == "complete" else None,
    ))

    # =========================================================================
    # CIRCUIT (20 points)
    # =========================================================================
    circuit_points = 0
    circuit_max = 20

    if trace.circuits and len(trace.circuits) > 0:
        c = trace.circuits[0]

        # Basic circuit info (8 points)
        if c.num_qubits > 0 and c.depth > 0:
            circuit_points += 8

        # Gate counts (5 points)
        if c.gates and c.gates.total > 0:
            circuit_points += 5

        # Circuit hash for verification (4 points)
        if c.hash:
            circuit_points += 4

        # QASM or JSON representation (3 points)
        if c.qasm or c.json_repr:
            circuit_points += 3
        else:
            recommendations.append("Consider storing QASM for exact circuit reproduction")

        status = "complete" if circuit_points >= 18 else "partial" if circuit_points > 0 else "missing"
    else:
        status = "missing"
        recommendations.append("No circuit captured - the core of your experiment is missing")

    components.append(ScoreComponent(
        name="Circuit",
        category="Quantum Program",
        max_points=circuit_max,
        earned_points=circuit_points,
        status=status,
    ))

    # =========================================================================
    # TRANSPILATION (15 points)
    # =========================================================================
    transp_points = 0
    transp_max = 15

    if trace.transpilation:
        t = trace.transpilation

        # Optimization level (4 points)
        if t.optimization_level is not None:
            transp_points += 4

        # Layout/routing methods (4 points)
        if t.layout_method or t.routing_method:
            transp_points += 4

        # Qubit mapping (4 points) - CRITICAL for reproduction
        if t.final_layout:
            transp_points += 4
        else:
            recommendations.append("Qubit mapping not captured - results depend on physical qubit assignment")

        # Before/after circuit comparison (3 points)
        if t.input_circuit and t.output_circuit:
            transp_points += 3

        status = "complete" if transp_points >= 13 else "partial" if transp_points > 0 else "missing"
    else:
        status = "missing"
        # Not always applicable (simulators don't transpile)
        if trace.hardware and not trace.hardware.is_simulator:
            recommendations.append("Transpilation not captured - critical for hardware experiments")

    components.append(ScoreComponent(
        name="Transpilation",
        category="Circuit Compilation",
        max_points=transp_max,
        earned_points=transp_points,
        status=status,
    ))

    # =========================================================================
    # HARDWARE (25 points) - Most important for real hardware
    # =========================================================================
    hw_points = 0
    hw_max = 25

    if trace.hardware:
        h = trace.hardware

        # Backend identification (6 points)
        if h.backend:
            hw_points += 6

        # Provider (3 points)
        if h.provider:
            hw_points += 3

        # Qubits used (4 points)
        if h.qubits_used and len(h.qubits_used) > 0:
            hw_points += 4
        elif not h.is_simulator:
            recommendations.append("Physical qubits not recorded - critical for reproduction")

        # Calibration data (12 points) - THE killer feature
        if h.calibration:
            cal = h.calibration
            # Timestamp (3 points)
            if cal.timestamp:
                hw_points += 3

            # Qubit properties (5 points)
            if cal.qubits and len(cal.qubits) > 0:
                hw_points += 5

            # Gate errors (4 points)
            if cal.gates and len(cal.gates) > 0:
                hw_points += 4
        elif not h.is_simulator:
            recommendations.append(
                "⚠️ No calibration snapshot - hardware state changes daily, "
                "reproduction without this is nearly impossible"
            )

        status = "complete" if hw_points >= 22 else "partial" if hw_points > 0 else "missing"
    else:
        status = "missing"
        recommendations.append("No hardware information - cannot determine where experiment ran")

    components.append(ScoreComponent(
        name="Hardware",
        category="Backend & Calibration",
        max_points=hw_max,
        earned_points=hw_points,
        status=status,
    ))

    # =========================================================================
    # EXECUTION (10 points)
    # =========================================================================
    exec_points = 0
    exec_max = 10

    if trace.execution:
        e = trace.execution

        # Shots (5 points)
        if e.shots and e.shots > 0:
            exec_points += 5

        # Job ID for traceability (2 points)
        if e.job_id:
            exec_points += 2

        # Timing info (3 points)
        if e.submitted_at or e.completed_at:
            exec_points += 3

        status = "complete" if exec_points >= 8 else "partial" if exec_points > 0 else "missing"
    else:
        status = "missing"
        recommendations.append("Execution parameters not captured")

    components.append(ScoreComponent(
        name="Execution",
        category="Run Parameters",
        max_points=exec_max,
        earned_points=exec_points,
        status=status,
    ))

    # =========================================================================
    # RESULTS (10 points)
    # =========================================================================
    result_points = 0
    result_max = 10

    if trace.result:
        r = trace.result

        # Counts captured (5 points)
        if r.counts and r.counts.raw:
            result_points += 5

        # Result hash for verification (3 points)
        if r.hash:
            result_points += 3

        # Metadata (2 points)
        if r.metadata:
            result_points += 2

        status = "complete" if result_points >= 8 else "partial" if result_points > 0 else "missing"
    else:
        status = "missing"
        recommendations.append("No results captured - cannot verify reproduction")

    components.append(ScoreComponent(
        name="Results",
        category="Output Verification",
        max_points=result_max,
        earned_points=result_points,
        status=status,
    ))

    # =========================================================================
    # COMPUTE FINAL SCORE
    # =========================================================================
    total_score = sum(c.earned_points for c in components)
    max_score = sum(c.max_points for c in components)
    percentage = (total_score / max_score) * 100

    # Determine grade
    if percentage >= 90:
        grade = "Excellent"
    elif percentage >= 70:
        grade = "Good"
    elif percentage >= 50:
        grade = "Fair"
    elif percentage >= 25:
        grade = "Poor"
    else:
        grade = "Critical"

    return ReproducibilityScore(
        total_score=total_score,
        max_score=max_score,
        grade=grade,
        components=components,
        recommendations=recommendations,
    )
