# Comparative Strength Assessment of Password-Based Key Derivation Functions

A modern cybersecurity and cryptography educational benchmarking application built with **Python**, **Streamlit**, and Python's built-in cryptographic library (`hashlib`).

## 📌 Project Overview

| Detail | Description |
|---|---|
| **Project Title** | Comparative Strength Assessment of Password-Based Key Derivation Functions |
| **Domain** | Cybersecurity / Applied Cryptography |
| **Language** | Python 3.11+ |
| **Frontend** | Streamlit |
| **Algorithms** | PBKDF2 (`hashlib.pbkdf2_hmac`) & scrypt (`hashlib.scrypt`) |
| **Database** | None required |
| **Primary Goal** | Compare execution time, memory complexity, and hardware-attack resistance |

---

## 🚀 How It Works

1. **User Password & Salt**: The user enters a sample password (e.g., `Demo@12345`). The app generates a cryptographically secure 16-byte random salt (`os.urandom(16)`).
2. **Key Derivation**: PBKDF2-HMAC-SHA256 and scrypt independently derive symmetric keys (32 bytes / 256 bits).
3. **Execution Time Measurement**: Python measures execution time of both algorithms across **3 independent runs** using high-precision timers (`time.perf_counter()`).
4. **Analysis & Visualizations**:
   - Comparison table showing execution times per run, averages, and memory footprint.
   - Interactive grouped bar chart for Run 1, 2, 3 and overall average.
   - Scatter plot displaying the Computational Latency vs. Memory Frontier.
   - Security breakdown explaining why scrypt's memory hardness defeats GPU clusters and ASICs, whereas PBKDF2 remains susceptible to GPU parallel brute-forcing.

---

## 🛠️ Algorithms Comparison

| Feature | PBKDF2 | scrypt |
|---|---|---|
| **Underlying Approach** | Pure CPU iteration loop | Sequential memory-hard function |
| **Cryptographic Primitives** | HMAC-SHA256 (or HMAC-SHA512) | PBKDF2-HMAC-SHA256 + Salsa20/8 |
| **Memory Allocation** | Negligible (< a few KiB) | Configurable: ~16 MiB default (`128 × r × N`) |
| **Hardware Resistance** | Low against GPUs/ASICs | High against GPUs, FPGAs, and ASICs |
| **Python API** | `hashlib.pbkdf2_hmac()` | `hashlib.scrypt()` |
| **Standard** | RFC 2898 / PKCS #5 | RFC 7914 |

---

## 💻 Running the Application

### 1. Activate the Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Launch Streamlit
```powershell
streamlit run app.py
```
Or directly using the virtual environment's Python:
```powershell
.\.venv\Scripts\streamlit run app.py
```

The application will launch in your browser at `http://localhost:8501`.
