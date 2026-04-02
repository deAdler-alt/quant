# Quantum Duo: Secure Quantum Chemistry

Think Quantum. Build Beyond.
End-to-end demo that combines **BB84 quantum key distribution** with a **VQE simulation of H₂**.
If the channel looks secure (low QBER), we run VQE, then **encrypt the results** with a key derived from BB84.

<p align="center">
  <img src="outputs/h2_energy_curve.png" alt="H2 energy curve" width="45%"/>
  <img src="outputs/h2_error_curve.png" alt="VQE error" width="45%"/>
</p>

## Why this project?

* Covers two tracks at once: **Cryptography & Secure Communications** + **Quantum Simulations**
* Clear, visual artifacts: QBER plot, energy curve, error curve, optional heatmap and CSV walkthrough
* Minimal setup; runs on a laptop (statevector simulation, no hardware required)

---

## Features

* **BB84 simulation** with intercept-resend attacker and channel noise
* **QBER decision gate** with a configurable threshold (Shor-Preskill bound, 0.11)
* **VQE for H₂** using a lightweight 2-qubit Hamiltonian and classical optimizer
* **Exact baseline** and per-point **VQE error**
* **Secure output**: by default **AES-CTR** with a **SHA-256 KDF** (fallback: XOR)
* **Interactive Streamlit dashboard** with live parameter controls, plots, and download buttons
* Optional **QBER heatmap** and **BB84 educational walkthrough**

---

## Project structure

```
.
├── app.py                 # Streamlit dashboard (entry point)
├── bb84.py                # BB84 core + heatmap + walkthrough
├── vqe_h2.py              # VQE, exact baseline, plots
├── crypto_utils.py        # KDF, AES-CTR (fallback XOR), base64 helpers
├── requirements.txt
├── LICENSE
└── outputs/               # optional static artifacts (gitignored)
```

---

## Quick start

### 1) Environment

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Run the Streamlit dashboard

```bash
streamlit run app.py
```

The app opens in your browser. Use the **sidebar** to adjust all parameters in real time:

| Parameter | Control | Default |
|-----------|---------|---------|
| n (raw rounds) | number input | 1024 |
| Eve probability | slider | 0.25 |
| Channel noise | slider | 0.0 |
| QBER sweep steps | slider | 8 |
| Seed | number input | 1 |
| R grid (Å) | text input | 0.3,0.5,0.7,0.9,1.1,1.3 |
| Max iterations | number input | 200 |
| Ansatz reps | slider | 2 |
| Force XOR | checkbox | off |
| QBER heatmap | checkbox | off |
| Walkthrough bits | number input | 0 |

### 3) Dashboard tabs

* **BB84** — QBER metrics, QBER vs Eve plot, optional heatmap and walkthrough table
* **VQE H₂** — energy curve + error curve side by side, data table
* **Security** — encryption mode, key info, download buttons for all artifacts

---

## What it does

1. **BB84 phase**
   Generates random bits and bases for Alice and Bob. Optionally inserts an intercept-resend attacker (Eve) with probability `p_eve` and a simple channel bit-flip noise `p_noise`.
   Keeps only positions with matching bases (sifting) and computes **QBER**. Plots **QBER vs. `p_eve`**. If QBER under the Shor-Preskill threshold (0.11), we proceed.

2. **VQE phase**
   Builds a compact 2-qubit Hamiltonian for H₂ at selected bond lengths (Å), runs **VQE** with `EfficientSU2` ansatz and **L-BFGS-B** optimizer, and computes the **exact ground state** by diagonalizing the same Hamiltonian.
   Saves the **energy curve** with both **VQE** and **Exact**, plus an **absolute error** plot.

3. **Secure delivery phase**
   Derives a 256-bit key from BB84 bits via **SHA-256** and encrypts the results with **AES-CTR** (nonce prepended). If XOR is forced or AES is unavailable, uses XOR as a minimal fallback.
   Download encrypted payloads, JSON, and CSV directly from the dashboard.

---

## How it works (tech details)

* **BB84**
  State preparation in Z/X, intercept-resend attacker measured in a random basis, optional channel bit-flip noise. Sifting by matching bases, **QBER = mean(bits_Alice != bits_Bob)**.

  * **Heatmap** of QBER vs `(p_eve, p_noise)`
  * **Walkthrough** tracing each of N positions (bits, bases, kept flag)

* **VQE**
  Variational ansatz: `EfficientSU2(num_qubits=2, entanglement="full", reps=REPS)`
  Objective: ⟨ψ(θ)|H|ψ(θ)⟩ evaluated from the statevector. Optimization via **SciPy L-BFGS-B**.
  Hamiltonian matrix is cached (`lru_cache`) so the dense conversion runs once per bond length, not per optimizer iteration.
  We include an **exact baseline** by diagonalizing the same 2-qubit Hamiltonian to validate VQE.

* **Security**
  KDF: **SHA-256** over BB84 key material → 32-byte key.
  Cipher: **AES-CTR** with a 16-byte random nonce; output prepends nonce.
  Fallback: XOR when forced or `cryptography` is not installed.

---

## Reproducibility

* Use the **Seed** parameter to get deterministic BB84 sequences and VQE initial parameters.
* Streamlit caches results per parameter set — change a slider and only the affected computation reruns.

---

## Limitations

* The H₂ Hamiltonians are a compact, pre-tabulated 2-qubit model (Bravyi-Kitaev / STO-3G) for a fast demo; values are reported in **relative a.u.** to emphasize shape and minima, not absolute chemical accuracy.
* BB84 model is simplified (intercept-resend + bit-flip noise).
* AES-CTR provides confidentiality but not authenticity; for production use prefer **AES-GCM** or AES-CTR + **HMAC-SHA-256**.

---

## Install and dependencies

* Python 3.10+
* `pip install -r requirements.txt` installs:
  `qiskit`, `qiskit-aer`, `numpy`, `matplotlib`, `scipy`, `cryptography`, `streamlit`, `pandas`

---

## Authors

Kamil Piejko
Marcin Przybylski
Aleksandra Czuba
Mateusz Grabowski
Dominik Czajka

---

## License

This project is open-sourced under the **MIT License**. See `LICENSE`.

---

## References

* QKD: C. H. Bennett and G. Brassard, *Proceedings of IEEE Int. Conf. on Computers, Systems and Signal Processing*, Bangalore, India, 1984.
* QKD security: P. W. Shor and J. Preskill, *Simple proof of security of the BB84 quantum key distribution protocol*, Phys. Rev. Lett. 85, 441 (2000).
* VQE: A. Peruzzo et al., *A variational eigenvalue solver on a photonic quantum processor*, Nat. Commun. 5, 4213 (2014).
* Qiskit documentation: [https://qiskit.org/documentation/](https://qiskit.org/documentation/)
* SciPy optimize: [https://docs.scipy.org/doc/scipy/reference/optimize.html](https://docs.scipy.org/doc/scipy/reference/optimize.html)
