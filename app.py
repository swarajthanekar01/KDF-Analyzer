import streamlit as st
import hashlib
import os
import time
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="PBKDF2 vs scrypt",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Sidebar: Parameters & Configuration
# ---------------------------------------------------------
st.sidebar.title("⚙️ Settings")

st.sidebar.subheader("Password & Salt")
password_input = st.sidebar.text_input(
    "Password",
    value="Demo@12345",
    type="password"
)

salt_mode = st.sidebar.radio("Salt Source", ["Random (Auto)", "Custom"])
if salt_mode == "Random (Auto)":
    if "salt" not in st.session_state:
        st.session_state.salt = os.urandom(16)
    if st.sidebar.button("🔄 New Salt"):
        st.session_state.salt = os.urandom(16)
    salt_bytes = st.session_state.salt
else:
    custom_salt_str = st.sidebar.text_input("Custom Salt", value="CustomSalt2026")
    salt_bytes = custom_salt_str.encode("utf-8")

st.sidebar.caption(f"Salt: `{salt_bytes.hex()}`")

st.sidebar.divider()
st.sidebar.subheader("PBKDF2")
pbkdf2_iterations = st.sidebar.number_input(
    "Iterations",
    min_value=1000,
    max_value=2000000,
    value=100000,
    step=10000
)
pbkdf2_hash_algo = st.sidebar.selectbox("Hash Function", ["sha256", "sha512"])

st.sidebar.divider()
st.sidebar.subheader("scrypt")
scrypt_n = st.sidebar.select_slider(
    "CPU/Memory Cost (N)",
    options=[1024, 2048, 4096, 8192, 16384, 32768, 65536],
    value=16384
)
scrypt_r = st.sidebar.number_input("Block Size (r)", min_value=1, max_value=32, value=8)
scrypt_p = st.sidebar.number_input("Parallelization (p)", min_value=1, max_value=8, value=1)
scrypt_mem_mib = (128 * scrypt_r * scrypt_n) / (1024 * 1024)
st.sidebar.info(f"Memory: ~{scrypt_mem_mib:.1f} MiB")

st.sidebar.divider()
derived_key_len = st.sidebar.selectbox("Key Length (bytes)", [16, 32, 64], index=1)

st.sidebar.divider()
pdf_path = "Project_Documentation_PBKDF2_vs_scrypt.pdf"
if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    st.sidebar.download_button(
        label="📄 Download Report (PDF)",
        data=pdf_bytes,
        file_name="PBKDF2_vs_scrypt_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )


# ---------------------------------------------------------
# Benchmark Functions
# ---------------------------------------------------------
def run_pbkdf2(password, salt, iterations, hash_name, dklen, runs=3):
    pw = password.encode("utf-8")
    times = []
    key = None
    for _ in range(runs):
        t0 = time.perf_counter()
        key = hashlib.pbkdf2_hmac(hash_name, pw, salt, iterations, dklen=dklen)
        times.append((time.perf_counter() - t0) * 1000)
    return {"runs": times, "avg": sum(times) / len(times),
            "min": min(times), "max": max(times), "key_hex": key.hex()}


def run_scrypt(password, salt, n, r, p, dklen, runs=3):
    pw = password.encode("utf-8")
    maxmem = int(128 * r * n * 2.5) + 32 * 1024 * 1024
    times = []
    key = None
    for _ in range(runs):
        t0 = time.perf_counter()
        key = hashlib.scrypt(pw, salt=salt, n=n, r=r, p=p, maxmem=maxmem, dklen=dklen)
        times.append((time.perf_counter() - t0) * 1000)
    return {"runs": times, "avg": sum(times) / len(times),
            "min": min(times), "max": max(times),
            "key_hex": key.hex(),
            "memory_mib": (128 * r * n) / (1024 * 1024)}


# ---------------------------------------------------------
# Main Page
# ---------------------------------------------------------
st.title("🔐 PBKDF2 vs scrypt")
st.caption("Comparative Strength Assessment of Password-Based Key Derivation Functions")
st.write(
    "This tool benchmarks two cryptographic key derivation algorithms. "
    "Adjust the parameters in the sidebar, then click **Run Benchmark** to start."
)

st.divider()

run_btn = st.button("▶ Run Benchmark", type="primary", use_container_width=True)

if run_btn or "results" not in st.session_state:
    with st.spinner("Running 3 trials for each algorithm..."):
        try:
            pb = run_pbkdf2(password_input, salt_bytes, pbkdf2_iterations,
                            pbkdf2_hash_algo, derived_key_len)
            sc = run_scrypt(password_input, salt_bytes, scrypt_n,
                            scrypt_r, scrypt_p, derived_key_len)
            st.session_state.results = {"pbkdf2": pb, "scrypt": sc,
                                        "ts": time.strftime("%H:%M:%S")}
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

results = st.session_state.get("results")
if not results:
    st.stop()

pb = results["pbkdf2"]
sc = results["scrypt"]

st.caption(f"Last run at {results['ts']}")

# ---------------------------------------------------------
# Summary Metrics
# ---------------------------------------------------------
st.subheader("📊 Results Summary")
c1, c2, c3, c4 = st.columns(4)
c1.metric("PBKDF2 Avg", f"{pb['avg']:.1f} ms")
c2.metric("scrypt Avg", f"{sc['avg']:.1f} ms")
c3.metric("scrypt Memory", f"{sc['memory_mib']:.1f} MiB")
ratio = sc["avg"] / pb["avg"] if pb["avg"] > 0 else 1
c4.metric("Speed Ratio", f"{ratio:.1f}x", help="How many times slower scrypt is vs PBKDF2")

# ---------------------------------------------------------
# Timing Table
# ---------------------------------------------------------
st.subheader("⏱ Timing Results (3 Runs)")
df = pd.DataFrame({
    "Run": ["Run 1", "Run 2", "Run 3", "Average", "Min", "Max"],
    "PBKDF2 (ms)": [
        round(pb["runs"][0], 2), round(pb["runs"][1], 2), round(pb["runs"][2], 2),
        round(pb["avg"], 2), round(pb["min"], 2), round(pb["max"], 2)
    ],
    "scrypt (ms)": [
        round(sc["runs"][0], 2), round(sc["runs"][1], 2), round(sc["runs"][2], 2),
        round(sc["avg"], 2), round(sc["min"], 2), round(sc["max"], 2)
    ],
    "Difference (ms)": [
        round(sc["runs"][0] - pb["runs"][0], 2),
        round(sc["runs"][1] - pb["runs"][1], 2),
        round(sc["runs"][2] - pb["runs"][2], 2),
        round(sc["avg"] - pb["avg"], 2), "-", "-"
    ]
})
st.dataframe(df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# Bar Chart
# ---------------------------------------------------------
st.subheader("📈 Execution Time per Trial")
fig = go.Figure()
fig.add_trace(go.Bar(
    x=["Run 1", "Run 2", "Run 3", "Average"],
    y=pb["runs"] + [pb["avg"]],
    name="PBKDF2",
    marker_color="#2563EB"
))
fig.add_trace(go.Bar(
    x=["Run 1", "Run 2", "Run 3", "Average"],
    y=sc["runs"] + [sc["avg"]],
    name="scrypt",
    marker_color="#9333EA"
))
fig.update_layout(
    barmode="group",
    yaxis_title="Time (ms)",
    legend=dict(orientation="h"),
    margin=dict(l=0, r=0, t=20, b=0),
    height=320
)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# Feature Comparison Table
# ---------------------------------------------------------
st.subheader("🔍 Algorithm Comparison")
comp_df = pd.DataFrame([
    {"Feature": "Approach", "PBKDF2": "CPU iteration loop", "scrypt": "Sequential memory-hard"},
    {"Feature": "Internal Primitive", "PBKDF2": f"HMAC-{pbkdf2_hash_algo.upper()}", "scrypt": "PBKDF2 + Salsa20/8"},
    {"Feature": "Memory Usage", "PBKDF2": "Negligible (< 1 KiB)", "scrypt": f"~{sc['memory_mib']:.1f} MiB"},
    {"Feature": "Parameters", "PBKDF2": f"iterations = {pbkdf2_iterations:,}", "scrypt": f"N={scrypt_n:,}, r={scrypt_r}, p={scrypt_p}"},
    {"Feature": "GPU Resistance", "PBKDF2": "Low", "scrypt": "High"},
    {"Feature": "ASIC Resistance", "PBKDF2": "Low", "scrypt": "Very High"},
    {"Feature": "Standard", "PBKDF2": "RFC 2898 / PKCS#5", "scrypt": "RFC 7914"},
    {"Feature": "Python API", "PBKDF2": "hashlib.pbkdf2_hmac()", "scrypt": "hashlib.scrypt()"},
])
st.dataframe(comp_df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# Derived Keys
# ---------------------------------------------------------
with st.expander("🔑 View Derived Keys & Salt"):
    st.write("**Salt (hex):**")
    st.code(salt_bytes.hex())
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.write("**PBKDF2 Derived Key:**")
        st.code(pb["key_hex"])
    with col_k2:
        st.write("**scrypt Derived Key:**")
        st.code(sc["key_hex"])
    st.info(
        "Both keys are derived from the same password and salt but are "
        "completely different due to different internal algorithms."
    )

# ---------------------------------------------------------
# Security Notes
# ---------------------------------------------------------
with st.expander("🛡️ Security Notes"):
    st.markdown("""
**Why scrypt is more secure than PBKDF2:**

- **PBKDF2** repeats a hash function many times. It uses almost no memory, so attackers can run thousands of guesses in parallel on GPUs or custom ASIC chips at very low cost.

- **scrypt** forces the computer to allocate a large block of RAM (e.g. 16 MiB). An attacker trying 10,000 guesses in parallel would need 160 GiB of fast memory — physically impossible on most hardware.

**Memory formula:** `Memory = 128 x r x N bytes`

**OWASP Recommendations:**
- Use **Argon2id** (best) or **scrypt** for new systems.
- If PBKDF2 is required (FIPS compliance), use >= 600,000 iterations with SHA-256.
- Always use a random 16-byte salt from `os.urandom(16)`.
    """)

st.divider()
st.caption("CIS Mini Project - Cybersecurity & Cryptography - PBKDF2 vs scrypt")
