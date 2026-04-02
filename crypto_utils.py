from __future__ import annotations

import base64
import json
import os
from math import ceil

import numpy as np

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import hashes
    _AES_AVAILABLE = True
except Exception:
    _AES_AVAILABLE = False


def has_aes() -> bool:
    return _AES_AVAILABLE


def bits_to_key_bytes(bits: list[int]) -> bytes:
    """Pack a list of 0/1 ints into bytes (big-endian, truncated to multiple of 8)."""
    length = len(bits) - len(bits) % 8
    if length == 0:
        return b"\x00"
    chunks = (bits[i : i + 8] for i in range(0, length, 8))
    return bytes(int("".join(map(str, byte)), 2) for byte in chunks)


def derive_key_sha256(key_material: bytes) -> bytes:
    """SHA-256 based KDF -- returns 32 bytes suitable for AES-256."""
    if not _AES_AVAILABLE:
        return key_material
    h = hashes.Hash(hashes.SHA256())
    h.update(key_material)
    return h.finalize()


def xor_bytes(data: bytes, key: bytes) -> bytes:
    """Vectorised repeating-key XOR."""
    if not key:
        return data
    d = np.frombuffer(data, dtype=np.uint8)
    k = np.frombuffer(key, dtype=np.uint8)
    expanded = np.tile(k, ceil(len(d) / len(k)))[:len(d)]
    return (d ^ expanded).tobytes()


def json_encrypt_xor(obj: object, key_bytes: bytes) -> bytes:
    return xor_bytes(json.dumps(obj, separators=(",", ":")).encode(), key_bytes)


def json_decrypt_xor(enc: bytes, key_bytes: bytes) -> object:
    return json.loads(xor_bytes(enc, key_bytes).decode())


def aes_ctr_encrypt(plaintext: bytes, key32: bytes) -> bytes:
    if not _AES_AVAILABLE:
        raise RuntimeError("AES not available")
    nonce = os.urandom(16)
    encryptor = Cipher(algorithms.AES(key32), modes.CTR(nonce)).encryptor()
    return nonce + encryptor.update(plaintext) + encryptor.finalize()


def aes_ctr_decrypt(blob: bytes, key32: bytes) -> bytes:
    if not _AES_AVAILABLE:
        raise RuntimeError("AES not available")
    nonce, ct = blob[:16], blob[16:]
    decryptor = Cipher(algorithms.AES(key32), modes.CTR(nonce)).decryptor()
    return decryptor.update(ct) + decryptor.finalize()


def to_base64_str(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")


def from_base64_str(s: str) -> bytes:
    return base64.b64decode(s.encode("ascii"))
