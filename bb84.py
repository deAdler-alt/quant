"""BB84 QKD simulation with intercept-resend attacker and channel noise."""
from __future__ import annotations

from typing import Any

import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# ── BB84 security bound (Shor-Preskill, 2000) ────────────────────────
QBER_SECURITY_THRESHOLD: float = 0.11


# ── Helpers ───────────────────────────────────────────────────────────

def compute_qber(alice: list[int], bob: list[int]) -> float | None:
    """QBER = fraction of mismatched sifted bits.  None when no bits kept."""
    if not alice:
        return None
    a, b = np.asarray(alice, dtype=np.int8), np.asarray(bob, dtype=np.int8)
    return float(np.mean(a != b))


def _prepare_state(bit: int, basis: str) -> QuantumCircuit:
    qc = QuantumCircuit(1, 1)
    if basis == "Z":
        if bit:
            qc.x(0)
    elif basis == "X":
        qc.h(0)
        if bit:
            qc.z(0)
    else:
        raise ValueError(f"basis must be 'Z' or 'X', got {basis!r}")
    return qc


def _measure_in_basis(qc: QuantumCircuit, basis: str, sim: AerSimulator) -> int:
    mqc = qc.copy()
    if basis == "X":
        mqc.h(0)
    mqc.measure(0, 0)
    counts = sim.run(mqc, shots=1).result().get_counts()
    return int(counts.get("1", 0))


# ── Core loop (single parametrised function) ─────────────────────────

def _bb84_core(
    n: int = 512,
    p_eve: float = 0.0,
    p_noise: float = 0.0,
    seed: int = 123,
    track_bits: bool = False,
) -> dict[str, Any]:
    """Run one BB84 session.

    When *track_bits* is True the return dict includes per-qubit arrays
    (for the educational walkthrough); otherwise only summary statistics.
    """
    rng = np.random.default_rng(seed)
    sim = AerSimulator(seed_simulator=seed)

    alice_bits = rng.integers(0, 2, size=n)
    alice_bases = rng.choice(["Z", "X"], size=n)
    bob_bases = rng.choice(["Z", "X"], size=n)

    bob_bits = np.zeros(n, dtype=int) if track_bits else None
    keep_flags = np.zeros(n, dtype=int) if track_bits else None
    sift_a: list[int] = []
    sift_b: list[int] = []

    for i in range(n):
        qc = _prepare_state(int(alice_bits[i]), alice_bases[i])
        if rng.random() < p_eve:
            eve_basis = rng.choice(["Z", "X"])
            qc = _prepare_state(_measure_in_basis(qc, eve_basis, sim), eve_basis)
        if p_noise > 0 and rng.random() < p_noise:
            qc.x(0)
        measured = _measure_in_basis(qc, bob_bases[i], sim)
        if track_bits:
            bob_bits[i] = measured  # type: ignore[index]
        if alice_bases[i] == bob_bases[i]:
            if track_bits:
                keep_flags[i] = 1  # type: ignore[index]
            sift_a.append(int(alice_bits[i]))
            sift_b.append(measured)

    result: dict[str, Any] = {
        "qber": compute_qber(sift_a, sift_b),
        "key_bits": sift_a,
        "kept": len(sift_a),
    }
    if track_bits:
        result.update(
            alice_bits=[int(x) for x in alice_bits],
            alice_bases=[str(x) for x in alice_bases],
            bob_bases=[str(x) for x in bob_bases],
            bob_bits=[int(x) for x in bob_bits],  # type: ignore[iter-type]
            keep=[int(x) for x in keep_flags],  # type: ignore[iter-type]
        )
    return result


# ── Public API ────────────────────────────────────────────────────────

def sanity_check_bb84() -> dict:
    """H·H = I check on the Aer simulator."""
    sim = AerSimulator(seed_simulator=1)
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.h(0)
    qc.measure(0, 0)
    return sim.run(qc, shots=1).result().get_counts()


def run_bb84(
    n: int = 512,
    p_eve: float = 0.0,
    p_noise: float = 0.0,
    seed: int = 123,
    steps: int = 8,
) -> dict[str, Any]:
    """Full BB84 run: clean QBER, full-attack QBER, sweep, and key bits."""
    clean = _bb84_core(n=n, p_eve=0.0, p_noise=p_noise, seed=seed)
    full = _bb84_core(n=n, p_eve=1.0, p_noise=p_noise, seed=seed)

    p_eves = np.linspace(0.0, 1.0, steps).tolist()
    qbers = [
        (_bb84_core(n=n, p_eve=p, p_noise=p_noise, seed=seed + k + 1)["qber"] or 0.0)
        for k, p in enumerate(p_eves)
    ]

    key_bits = _collect_key_minlen(min_len=128, n=n, p_noise=p_noise, seed=seed + 99)
    return {
        "qber_no_eve": clean["qber"],
        "qber_full_eve": full["qber"],
        "p_eves": p_eves,
        "qbers": qbers,
        "key_bits": key_bits,
    }


def _collect_key_minlen(
    min_len: int = 128, n: int = 512, p_noise: float = 0.0, seed: int = 123
) -> list[int]:
    bits: list[int] = []
    for hop in range(10):
        if len(bits) >= min_len:
            break
        bits.extend(_bb84_core(n=n, p_eve=0.0, p_noise=p_noise, seed=seed + hop)["key_bits"])
    return bits[:min_len]


def bb84_walkthrough(
    n: int = 16, p_eve: float = 0.0, p_noise: float = 0.0, seed: int = 123
) -> dict[str, Any]:
    """Bit-level walkthrough for educational display."""
    return _bb84_core(n=n, p_eve=p_eve, p_noise=p_noise, seed=seed, track_bits=True)


# ── Heatmap ───────────────────────────────────────────────────────────

def run_qber_heatmap(
    n: int = 512,
    pe_min: float = 0.0, pe_max: float = 1.0, pe_steps: int = 6,
    pn_min: float = 0.0, pn_max: float = 0.2, pn_steps: int = 6,
    seed: int = 123,
    avg: int = 1,
) -> dict[str, Any]:
    p_eves = np.linspace(pe_min, pe_max, pe_steps)
    p_noises = np.linspace(pn_min, pn_max, pn_steps)
    mat = np.zeros((pn_steps, pe_steps))
    idx = 0
    for i, pn in enumerate(p_noises):
        for j, pe in enumerate(p_eves):
            total = sum(
                (_bb84_core(n=n, p_eve=float(pe), p_noise=float(pn), seed=seed + idx + k)["qber"] or 0.0)
                for k in range(avg)
            )
            mat[i, j] = total / avg
            idx += 17
    return {
        "p_eves": p_eves.tolist(),
        "p_noises": p_noises.tolist(),
        "qber": mat,
    }


# ── Plotting (return Figure for Streamlit compatibility) ──────────────

def make_qber_plot(xs: list[float], ys: list[float]) -> Figure:
    fig, ax = plt.subplots()
    ax.plot(xs, ys, marker="o")
    ax.set_xlabel("Intercept-Resend probability (Eve)")
    ax.set_ylabel("QBER")
    ax.set_title("BB84: QBER vs Eve attack probability")
    ax.grid(True)
    fig.tight_layout()
    return fig


def make_qber_heatmap(
    p_eves: list[float], p_noises: list[float], mat: np.ndarray
) -> Figure:
    fig, ax = plt.subplots()
    extent = [min(p_eves), max(p_eves), min(p_noises), max(p_noises)]
    im = ax.imshow(mat, origin="lower", aspect="auto", extent=extent, interpolation="nearest")
    fig.colorbar(im, ax=ax, label="QBER")
    ax.set_xlabel("Eve probability")
    ax.set_ylabel("Noise probability")
    ax.set_title("BB84: QBER heatmap")
    fig.tight_layout()
    return fig


def save_qber_plot(xs: list[float], ys: list[float], path: str) -> None:
    fig = make_qber_plot(xs, ys)
    fig.savefig(path)
    plt.close(fig)


def save_qber_heatmap(
    p_eves: list[float], p_noises: list[float], mat: np.ndarray, path: str
) -> None:
    fig = make_qber_heatmap(p_eves, p_noises, mat)
    fig.savefig(path)
    plt.close(fig)


# ── CSV export ────────────────────────────────────────────────────────

def save_walkthrough_csv(walk: dict[str, Any], path: str) -> None:
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["idx", "alice_bit", "alice_basis", "bob_basis", "bob_bit", "kept"])
        for i in range(len(walk["alice_bits"])):
            w.writerow([
                i,
                walk["alice_bits"][i],
                walk["alice_bases"][i],
                walk["bob_bases"][i],
                walk["bob_bits"][i],
                walk["keep"][i],
            ])
