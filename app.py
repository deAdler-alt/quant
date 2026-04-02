"""Quantum Duo — Streamlit dashboard for BB84 QKD + H₂ VQE."""
from __future__ import annotations

import csv
import io
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from bb84 import (
    QBER_SECURITY_THRESHOLD,
    bb84_walkthrough,
    make_qber_heatmap,
    make_qber_plot,
    run_bb84,
    run_qber_heatmap,
    sanity_check_bb84,
)
from crypto_utils import (
    aes_ctr_decrypt,
    aes_ctr_encrypt,
    bits_to_key_bytes,
    derive_key_sha256,
    has_aes,
    json_decrypt_xor,
    json_encrypt_xor,
    to_base64_str,
)
from vqe_h2 import make_energy_plot, make_error_plot, run_vqe_curve

# ── Page config ───────────────────────────────────────────────────────

st.set_page_config(
    page_title="Quantum Duo",
    page_icon="⚛",
    layout="wide",
)

# ── Sidebar: parameters ──────────────────────────────────────────────

st.sidebar.title("Parameters")

st.sidebar.subheader("BB84")
n_qubits = st.sidebar.number_input("n (raw rounds)", 64, 8192, 1024, step=64)
p_eve = st.sidebar.slider("Eve intercept probability", 0.0, 1.0, 0.25, 0.01)
p_noise = st.sidebar.slider("Channel noise probability", 0.0, 0.5, 0.0, 0.01)
steps = st.sidebar.slider("QBER sweep steps", 2, 32, 8)
seed = st.sidebar.number_input("Seed", 0, 10_000, 1, step=1)

st.sidebar.subheader("VQE")
rgrid_str = st.sidebar.text_input("R grid (Å, comma-separated)", "0.3,0.5,0.7,0.9,1.1,1.3")
maxiter = st.sidebar.number_input("Max optimizer iterations", 10, 2000, 200, step=10)
reps = st.sidebar.slider("Ansatz reps", 1, 6, 2)

st.sidebar.subheader("Encryption")
force_xor = st.sidebar.checkbox("Force XOR (no AES)", value=False)

st.sidebar.subheader("Optional")
show_heatmap = st.sidebar.checkbox("Generate QBER heatmap")
hm_pe_steps = st.sidebar.slider("Heatmap Eve steps", 3, 20, 6) if show_heatmap else 6
hm_pn_steps = st.sidebar.slider("Heatmap noise steps", 3, 20, 6) if show_heatmap else 6
hm_avg = st.sidebar.number_input("Heatmap avg repeats", 1, 10, 1) if show_heatmap else 1
demo_bits = st.sidebar.number_input("Walkthrough bits (0 = off)", 0, 128, 0, step=8)


# ── Cached computation ────────────────────────────────────────────────

@st.cache_data(show_spinner="Running BB84 simulation...")
def cached_bb84(n: int, p_eve: float, p_noise: float, seed: int, steps: int):
    return run_bb84(n=n, p_eve=p_eve, p_noise=p_noise, seed=seed, steps=steps)


@st.cache_data(show_spinner="Running VQE optimisation...")
def cached_vqe(rgrid: tuple[float, ...], seed: int, reps: int, maxiter: int):
    return run_vqe_curve(list(rgrid), seed=seed, reps=reps, maxiter=maxiter)


@st.cache_data(show_spinner="Computing QBER heatmap...")
def cached_heatmap(n: int, pe_steps: int, pn_steps: int, seed: int, avg: int):
    return run_qber_heatmap(
        n=n, pe_min=0.0, pe_max=1.0, pe_steps=pe_steps,
        pn_min=0.0, pn_max=0.2, pn_steps=pn_steps,
        seed=seed, avg=avg,
    )


# ── Parse R grid ──────────────────────────────────────────────────────

def parse_grid(s: str) -> tuple[float, ...]:
    return tuple(float(x) for x in s.split(",") if x.strip())


# ── Title ─────────────────────────────────────────────────────────────

st.title("Quantum Duo: Secure Quantum Chemistry")
st.caption("BB84 quantum key distribution + VQE for H₂ + encrypted delivery")

# ── Run BB84 ──────────────────────────────────────────────────────────

bb = cached_bb84(n_qubits, p_eve, p_noise, seed, steps)
qber_clean = bb["qber_no_eve"]
channel_secure = qber_clean is not None and qber_clean <= QBER_SECURITY_THRESHOLD

# ── Tabs ──────────────────────────────────────────────────────────────

tab_bb84, tab_vqe, tab_sec = st.tabs(["BB84", "VQE H₂", "Security"])

# ╭─────────────────────────────── BB84 ───────────────────────────────╮

with tab_bb84:
    san = sanity_check_bb84()
    st.success(f"Qiskit Aer sanity check: H·H·|0⟩ → {san}")

    c1, c2, c3 = st.columns(3)
    c1.metric("QBER (no attack)", f"{qber_clean:.4f}" if qber_clean is not None else "N/A")
    c2.metric("QBER (full attack)", f"{bb['qber_full_eve']:.4f}" if bb["qber_full_eve"] is not None else "N/A")
    c3.metric("Threshold", f"{QBER_SECURITY_THRESHOLD}")

    if not channel_secure:
        st.error(f"Channel insecure: QBER = {qber_clean}, exceeds threshold {QBER_SECURITY_THRESHOLD}. VQE phase skipped.")
    else:
        st.success("Channel secure — proceeding to VQE.")

    fig_qber = make_qber_plot(bb["p_eves"], bb["qbers"])
    st.pyplot(fig_qber)
    plt.close(fig_qber)

    if show_heatmap:
        hm = cached_heatmap(n_qubits, hm_pe_steps, hm_pn_steps, seed, hm_avg)
        fig_hm = make_qber_heatmap(hm["p_eves"], hm["p_noises"], hm["qber"])
        st.pyplot(fig_hm)
        plt.close(fig_hm)

    if demo_bits > 0:
        walk = bb84_walkthrough(n=demo_bits, p_eve=p_eve, p_noise=p_noise, seed=seed)
        df_walk = pd.DataFrame({
            "idx": range(len(walk["alice_bits"])),
            "alice_bit": walk["alice_bits"],
            "alice_basis": walk["alice_bases"],
            "bob_basis": walk["bob_bases"],
            "bob_bit": walk["bob_bits"],
            "kept": walk["keep"],
        })
        st.subheader("BB84 Walkthrough")
        st.dataframe(df_walk, use_container_width=True)
        walk_qber = walk.get("qber")
        st.caption(f"Walkthrough QBER = {walk_qber:.4f}" if walk_qber is not None else "Walkthrough QBER = N/A")

# ╭─────────────────────────────── VQE ────────────────────────────────╮

with tab_vqe:
    if not channel_secure:
        st.warning("VQE skipped — channel insecure.")
    else:
        rgrid = parse_grid(rgrid_str)
        if not rgrid:
            st.error("Provide at least one R value.")
        else:
            points = cached_vqe(rgrid, seed + 1, reps, maxiter)

            col_e, col_err = st.columns(2)
            with col_e:
                fig_e = make_energy_plot(points)
                st.pyplot(fig_e)
                plt.close(fig_e)
            with col_err:
                fig_err = make_error_plot(points)
                st.pyplot(fig_err)
                plt.close(fig_err)

            df = pd.DataFrame(points)
            df.columns = ["R (Å)", "E_vqe (a.u.)", "E_exact (a.u.)", "|error| (a.u.)"]
            st.dataframe(df.style.format({
                "R (Å)": "{:.2f}",
                "E_vqe (a.u.)": "{:.6f}",
                "E_exact (a.u.)": "{:.6f}",
                "|error| (a.u.)": "{:.3e}",
            }), use_container_width=True)

# ╭───────────────────────────── Security ─────────────────────────────╮

with tab_sec:
    if not channel_secure:
        st.warning("Encryption skipped — channel insecure.")
    else:
        rgrid = parse_grid(rgrid_str)
        points = cached_vqe(rgrid, seed + 1, reps, maxiter)

        raw_key = bits_to_key_bytes(bb["key_bits"])
        use_aes = has_aes() and not force_xor
        key32 = derive_key_sha256(raw_key) if use_aes else raw_key
        enc_mode = "AES-CTR" if use_aes else "XOR"

        c1, c2, c3 = st.columns(3)
        c1.metric("Encryption", enc_mode)
        c2.metric("Raw key bytes", len(raw_key))
        c3.metric("Derived key bytes", len(key32))

        payload = json.dumps({"points": points, "unit": "Relative a.u."}, separators=(",", ":")).encode()
        if use_aes:
            blob = aes_ctr_encrypt(payload, key32)
            decrypted = json.loads(aes_ctr_decrypt(blob, key32))
        else:
            blob = json_encrypt_xor({"points": points, "unit": "Relative a.u."}, raw_key)
            decrypted = json_decrypt_xor(blob, raw_key)

        assert decrypted["points"] == points, "Round-trip decryption mismatch"
        st.success("Round-trip encryption/decryption verified.")

        ext = "aes" if use_aes else "enc"
        col_dl1, col_dl2, col_dl3, col_dl4 = st.columns(4)
        col_dl1.download_button(
            f"vqe_results.{ext}", blob, file_name=f"vqe_results.{ext}", mime="application/octet-stream"
        )
        col_dl2.download_button(
            f"vqe_results.{ext}.b64", to_base64_str(blob), file_name=f"vqe_results.{ext}.b64", mime="text/plain"
        )
        col_dl3.download_button(
            "vqe_results.json",
            json.dumps({"points": points, "unit": "Relative a.u."}, indent=2),
            file_name="vqe_results.json",
            mime="application/json",
        )

        csv_buf = io.StringIO()
        writer = csv.writer(csv_buf)
        writer.writerow(["R_Angstrom", "E_vqe_au", "E_exact_au", "abs_error_au"])
        for p in points:
            writer.writerow([p["R"], p["E_vqe"], p["E_exact"], p["error"]])
        col_dl4.download_button(
            "points.csv", csv_buf.getvalue(), file_name="points.csv", mime="text/csv"
        )
