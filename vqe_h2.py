"""VQE simulation for H₂ with exact diagonalisation baseline.

Hamiltonian uses a compact 2-qubit Bravyi-Kitaev mapping.  Coefficients are
approximate values in *relative* atomic units -- shapes and minima are
physically meaningful, but absolute numbers are illustrative for a fast demo.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.circuit.library import EfficientSU2
from qiskit import QuantumCircuit
from scipy.optimize import minimize

# 2-qubit Bravyi-Kitaev coefficients for H₂ at selected bond lengths.
# Source: simplified mapping for STO-3G basis; values rounded for demo.
H2_COEFFS: dict[float, dict[str, float]] = {
    0.30: {"I": -0.81, "Z0": 0.045, "Z1": 0.045, "ZZ": 0.19, "XX": -0.68, "YY": -0.68},
    0.50: {"I": -1.02, "Z0": 0.030, "Z1": 0.030, "ZZ": 0.12, "XX": -0.72, "YY": -0.72},
    0.70: {"I": -1.12, "Z0": 0.010, "Z1": 0.010, "ZZ": 0.08, "XX": -0.75, "YY": -0.75},
    0.90: {"I": -1.08, "Z0": 0.005, "Z1": 0.005, "ZZ": 0.06, "XX": -0.70, "YY": -0.70},
    1.10: {"I": -1.04, "Z0": 0.003, "Z1": 0.003, "ZZ": 0.05, "XX": -0.66, "YY": -0.66},
    1.30: {"I": -1.01, "Z0": 0.002, "Z1": 0.002, "ZZ": 0.04, "XX": -0.62, "YY": -0.62},
}

_PAULI_LABELS = ("II", "ZI", "IZ", "ZZ", "XX", "YY")
_COEFF_KEYS = ("I", "Z0", "Z1", "ZZ", "XX", "YY")


def nearest_R_key(R: float) -> float:
    return min(H2_COEFFS, key=lambda k: abs(k - R))


def build_qubit_hamiltonian(R: float) -> SparsePauliOp:
    c = H2_COEFFS[nearest_R_key(R)]
    return SparsePauliOp.from_list(
        list(zip(_PAULI_LABELS, (c[k] for k in _COEFF_KEYS)))
    )


@lru_cache(maxsize=16)
def _hamiltonian_matrix(R_key: float) -> np.ndarray:
    """Dense Hamiltonian matrix, cached so VQE iterations don't rebuild it."""
    return build_qubit_hamiltonian(R_key).to_matrix(sparse=False)


def expectation(mat: np.ndarray, state: Statevector) -> float:
    """⟨ψ|H|ψ⟩"""
    v = state.data
    return float(np.real(np.vdot(v, mat @ v)))


def exact_energy(R: float) -> float:
    """Ground-state energy by full diagonalisation."""
    eigvals = np.linalg.eigvalsh(_hamiltonian_matrix(nearest_R_key(R)))
    return float(eigvals[0])


def vqe_energy(
    R: float, *, seed: int = 1, reps: int = 2, maxiter: int = 200
) -> float:
    """VQE energy using EfficientSU2 ansatz and L-BFGS-B."""
    R_key = nearest_R_key(R)
    mat = _hamiltonian_matrix(R_key)
    ansatz = EfficientSU2(num_qubits=2, entanglement="full", reps=reps)
    theta0 = np.random.default_rng(seed).standard_normal(ansatz.num_parameters) * 0.1

    def objective(theta: np.ndarray) -> float:
        qc: QuantumCircuit = ansatz.assign_parameters(theta)
        return expectation(mat, Statevector.from_instruction(qc))

    return float(minimize(objective, theta0, method="L-BFGS-B", options={"maxiter": maxiter}).fun)


def run_vqe_curve(
    R_list: list[float], *, seed: int = 1, reps: int = 2, maxiter: int = 200
) -> list[dict[str, float]]:
    seen: set[float] = set()
    results: list[dict[str, float]] = []
    for R in R_list:
        R_key = nearest_R_key(R)
        if R_key in seen:
            continue
        seen.add(R_key)
        e_exact = exact_energy(R_key)
        e_vqe = vqe_energy(R_key, seed=seed, reps=reps, maxiter=maxiter)
        results.append({
            "R": R_key,
            "E_vqe": e_vqe,
            "E_exact": e_exact,
            "error": abs(e_vqe - e_exact),
        })
    results.sort(key=lambda p: p["R"])
    return results


# ── Plotting (return Figure for Streamlit compatibility) ──────────────

def make_energy_plot(points: list[dict[str, float]]) -> Figure:
    xs = [p["R"] for p in points]
    y_vqe = [p["E_vqe"] for p in points]
    y_exact = [p["E_exact"] for p in points]
    i_min = int(np.argmin(y_vqe))

    fig, ax = plt.subplots()
    ax.plot(xs, y_vqe, marker="o", label="VQE")
    ax.plot(xs, y_exact, marker="s", label="Exact")
    ax.scatter([xs[i_min]], [y_vqe[i_min]], s=70, zorder=5)
    ax.set_xlabel("Bond length R (Å)")
    ax.set_ylabel("Relative energy (a.u.)")
    ax.set_title("H₂ potential energy curve")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    return fig


def make_error_plot(points: list[dict[str, float]]) -> Figure:
    xs = [p["R"] for p in points]
    errs = [p["error"] for p in points]

    fig, ax = plt.subplots()
    ax.plot(xs, errs, marker="o")
    ax.set_xlabel("Bond length R (Å)")
    ax.set_ylabel("|E_VQE − E_exact| (a.u.)")
    ax.set_title("VQE absolute error vs bond length")
    ax.grid(True)
    fig.tight_layout()
    return fig


def save_energy_plot(points: list[dict[str, float]], path: str) -> None:
    fig = make_energy_plot(points)
    fig.savefig(path)
    plt.close(fig)


def save_error_plot(points: list[dict[str, float]], path: str) -> None:
    fig = make_error_plot(points)
    fig.savefig(path)
    plt.close(fig)
