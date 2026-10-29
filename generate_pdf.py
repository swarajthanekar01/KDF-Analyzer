import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages after page 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "Comparative Strength Assessment of PBKDF2 vs scrypt | Project Technical Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 747, 558, 747)

        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, footer_text)
        self.drawString(54, 36, "Confidential • Academic & Cybersecurity Research Project")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def build_pdf(filename="Project_Documentation_PBKDF2_vs_scrypt.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2563EB"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E3A8A")
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1E293B")
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white
    )

    story = []

    # Title & Metadata Banner
    story.append(Paragraph("Comparative Strength Assessment of Password-Based Key Derivation Functions", title_style))
    story.append(Paragraph("Comprehensive Technical Guide: Problem Context, Technologies Used, and Cryptographic Algorithms (PBKDF2 vs scrypt)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceAfter=12))

    # Executive Overview
    meta_data = [
        [Paragraph("<b>Project Domain:</b>", table_cell), Paragraph("Cybersecurity / Applied Cryptography", table_cell),
         Paragraph("<b>Algorithms:</b>", table_cell), Paragraph("PBKDF2 (RFC 2898) & scrypt (RFC 7914)", table_cell)],
        [Paragraph("<b>Language:</b>", table_cell), Paragraph("Python 3.11+", table_cell),
         Paragraph("<b>Frontend Framework:</b>", table_cell), Paragraph("Streamlit (Interactive UI)", table_cell)],
        [Paragraph("<b>Testing Regime:</b>", table_cell), Paragraph("3-Trial Empirical Timing Latency", table_cell),
         Paragraph("<b>Visual Analytics:</b>", table_cell), Paragraph("Plotly & Pandas Data Engine", table_cell)]
    ]
    meta_table = Table(meta_data, colWidths=[100, 150, 95, 159])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # Section 1: The Problem & The Need
    story.append(Paragraph("1. The Need For This Project (Problem Statement)", h1_style))
    story.append(Paragraph(
        "In modern computer systems, passwords are the most common form of user authentication. However, storing passwords directly in plain text is catastrophic. Historically, developers attempted to protect passwords by hashing them with standard cryptographic hash functions like <b>MD5</b>, <b>SHA-1</b>, or <b>SHA-256</b>. This approach is fatally flawed due to architectural shifts in modern hardware.",
        body_style
    ))
    
    story.append(Paragraph("<b>The Threat Landscape:</b>", h2_style))
    story.append(Paragraph("• <b>Extreme Hash Speed:</b> General-purpose hash functions (SHA-256) were designed for digital signatures and data integrity verification, meaning they are engineered to be <i>as fast as possible</i>. A single consumer GPU (e.g., RTX 4090) can compute over <b>10 billion SHA-256 hashes per second</b> using password-cracking suites like Hashcat.", bullet_style))
    story.append(Paragraph("• <b>Rainbow Tables & Precomputed Dictionaries:</b> Without unique salting, attackers precalculate the hashes of billions of common dictionary words and reverse stolen password databases instantaneously.", bullet_style))
    story.append(Paragraph("• <b>Asymmetric Attacker Advantage:</b> While a server only needs to verify a password once per login, an offline attacker with leaked hashes can dedicate massive clusters of GPUs, FPGAs, and custom ASICs to test billions of guesses concurrently.", bullet_style))

    # Callout Box: What is a KDF?
    callout_data = [[
        Paragraph(
            "<b>Key Insight:</b> A Password-Based Key Derivation Function (KDF) intentionally introduces computational friction (slowness) and memory complexity to balance the playing field. It transforms low-entropy human passwords into high-entropy cryptographic keys while imposing a heavy resource penalty on brute-force attackers.",
            callout_style
        )
    ]]
    callout_table = Table(callout_data, colWidths=[504])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(Spacer(1, 4))
    story.append(callout_table)
    story.append(Spacer(1, 10))

    # Section 2: Technologies Used
    story.append(Paragraph("2. Technologies and Tools Used in the Project", h1_style))
    story.append(Paragraph(
        "This project leverages Python's standard library cryptographic implementations and modern data visualization frameworks to provide an empirical, reproducible testbed:",
        body_style
    ))

    tech_data = [
        [Paragraph("Technology", table_header), Paragraph("Role in Project", table_header), Paragraph("Key Functional Contribution", table_header)],
        [
            Paragraph("<b>Python 3.11+</b>", table_cell),
            Paragraph("Core Programming Language", table_cell),
            Paragraph("Provides runtime execution environment, strong typing, and C-extension bindings for high-performance cryptography.", table_cell)
        ],
        [
            Paragraph("<b>hashlib (Standard Lib)</b>", table_cell),
            Paragraph("Cryptographic Engine", table_cell),
            Paragraph("Direct access to OpenSSL-backed <code>hashlib.pbkdf2_hmac()</code> and <code>hashlib.scrypt()</code>, avoiding unverified third-party libraries.", table_cell)
        ],
        [
            Paragraph("<b>Streamlit</b>", table_cell),
            Paragraph("Interactive Web UI Framework", table_cell),
            Paragraph("Enables dynamic parameter sliders, real-time trial triggering, tabbed layouts, and clean cyber-security dashboard styling.", table_cell)
        ],
        [
            Paragraph("<b>Plotly & Pandas</b>", table_cell),
            Paragraph("Data Analytics & Visualization", table_cell),
            Paragraph("Generates multi-run trial bar charts, average latency with error bars, and the Memory vs. Latency Trade-Off frontier plot.", table_cell)
        ],
        [
            Paragraph("<b>time.perf_counter()</b>", table_cell),
            Paragraph("High-Precision Benchmarking", table_cell),
            Paragraph("Monotonic clock with sub-microsecond resolution unaffected by system clock adjustments, ensuring accurate execution latency measurements.", table_cell)
        ],
        [
            Paragraph("<b>os.urandom(16)</b>", table_cell),
            Paragraph("Cryptographic Entropy Source", table_cell),
            Paragraph("Generates 128 bits of cryptographically strong random salt from OS kernel entropy pool (/dev/urandom or Windows CryptGenRandom).", table_cell)
        ]
    ]
    tech_table = Table(tech_data, colWidths=[110, 130, 264])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 12))

    # Page Break for clean algorithm breakdown
    story.append(PageBreak())

    # Section 3: Deep-Dive into Cryptographic Algorithms
    story.append(Paragraph("3. Deep-Dive: Cryptographic Algorithms Explained", h1_style))
    story.append(Paragraph(
        "The project evaluates two distinct design philosophies in cryptographic key derivation: <b>CPU-bound iteration</b> (PBKDF2) versus <b>Sequential Memory-Hard Functions</b> (scrypt).",
        body_style
    ))

    # PBKDF2 Subsection
    story.append(Paragraph("A. PBKDF2 (Password-Based Key Derivation Function 2 - RFC 2898)", h2_style))
    story.append(Paragraph(
        "PBKDF2 is the classical industry standard formalized in PKCS #5 v2.0 and NIST SP 800-132. It operates by iterating a Pseudorandom Function (PRF), typically <b>HMAC-SHA256</b>, over the password and salt for <i>c</i> iterations:",
        body_style
    ))
    story.append(Paragraph("• <b>Internal Operation:</b> $U_1 = \\text{PRF}(\\text{Password}, \\text{Salt} \\parallel \\text{block\\_index})$, and each subsequent round is chained as $U_k = \\text{PRF}(\\text{Password}, U_{k-1})$. The final output block is the XOR summation $T = U_1 \\oplus U_2 \\oplus \\dots \\oplus U_c$.", bullet_style))
    story.append(Paragraph("• <b>Memory Consumption:</b> <b>Negligible (&lt; 1 KiB).</b> Each step only requires storing the 32-byte hash buffer from the previous step. The CPU performs pure arithmetic hashing.", bullet_style))
    story.append(Paragraph("• <b>The Critical Vulnerability:</b> Because PBKDF2 requires virtually zero RAM, an attacker can build custom ASIC chips or utilize GPUs with thousands of compute cores. Each core can independently evaluate a password without being bottlenecked by memory access.", bullet_style))

    # scrypt Subsection
    story.append(Paragraph("B. scrypt (Sequential Memory-Hard Key Derivation - RFC 7914)", h2_style))
    story.append(Paragraph(
        "Engineered by Colin Percival in 2009, <b>scrypt</b> was created specifically to eliminate the hardware vulnerability of PBKDF2 by demanding significant amounts of fast random-access memory (RAM).",
        body_style
    ))
    story.append(Paragraph("• <b>Internal Operation (ROMix Algorithm):</b> scrypt first uses PBKDF2 to derive an initial block array. It then initializes a large array of pseudorandom data in RAM (Phase 1) and repeatedly reads from and modifies pseudo-randomly selected indices based on previous calculations (Phase 2), utilizing the Salsa20/8 stream cipher core.", bullet_style))
    story.append(Paragraph("• <b>The Memory Hardness Formula:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Memory Required (Bytes) = 128 × r × N</b>", ParagraphStyle('CodeF', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor("#1D4ED8"))))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Where <b>N</b> is the CPU/memory cost parameter (power of 2, default: 16,384), <b>r</b> is the block size factor (default: 8), and <b>p</b> is parallelization.", body_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In our benchmark: $128 \\times 8 \\times 16,384 = \\mathbf{16,777,216\\text{ bytes}} \\approx \\mathbf{16\\text{ MiB}}$.", body_style))
    story.append(Paragraph("• <b>Why Memory Hardness Thwarts Attackers:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1. <b>GPU Memory Saturation:</b> An attacker attempting 10,000 parallel password guesses with scrypt would need $10,000 \\times 16\\text{ MiB} = 160\\text{ GiB}$ of high-speed VRAM, causing GPU failure or heavy serialization.", body_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2. <b>Economic Cost of ASICs:</b> Fabricating custom silicon with 16 MiB of high-speed embedded SRAM per core vastly increases chip die size and manufacturing cost, destroying the economic return of building cracking hardware.", body_style))

    story.append(Spacer(1, 6))

    # Side-by-Side Comparison Table
    story.append(Paragraph("Algorithm Comparison Matrix", h2_style))
    matrix_data = [
        [Paragraph("Feature", table_header), Paragraph("PBKDF2 (HMAC-SHA256)", table_header), Paragraph("scrypt (Salsa20/8 Core)", table_header)],
        [Paragraph("<b>Resource Bottleneck</b>", table_cell), Paragraph("CPU Arithmetic Only", table_cell), Paragraph("CPU + RAM Memory Bandwidth", table_cell)],
        [Paragraph("<b>Memory Footprint</b>", table_cell), Paragraph("~0 MiB (Negligible)", table_cell), Paragraph("~16 MiB in standard demo (128·r·N)", table_cell)],
        [Paragraph("<b>Default Parameters</b>", table_cell), Paragraph("iterations = 100,000", table_cell), Paragraph("N = 16384, r = 8, p = 1", table_cell)],
        [Paragraph("<b>GPU Resistance</b>", table_cell), Paragraph("Low (Millions of hashes/sec on GPUs)", table_cell), Paragraph("High (GPU VRAM quickly exhausted)", table_cell)],
        [Paragraph("<b>ASIC Resistance</b>", table_cell), Paragraph("Low (Compact chip design)", table_cell), Paragraph("Very High (Huge silicon die needed for SRAM)", table_cell)],
        [Paragraph("<b>Python API</b>", table_cell), Paragraph("<code>hashlib.pbkdf2_hmac()</code>", table_cell), Paragraph("<code>hashlib.scrypt()</code>", table_cell)]
    ]
    matrix_table = Table(matrix_data, colWidths=[120, 192, 192])
    matrix_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(matrix_table)
    story.append(Spacer(1, 12))

    # Section 4: Project Workflow & Implementation
    story.append(Paragraph("4. Step-by-Step Project Workflow", h1_style))
    story.append(Paragraph(
        "When the application executes on the host computer, it carries out the following operational steps:",
        body_style
    ))
    story.append(Paragraph("<b>Step 1: Input Collection:</b> The user inputs a sample password (e.g., <code>Demo@12345</code>) or tests custom phrases.", bullet_style))
    story.append(Paragraph("<b>Step 2: Cryptographic Salting:</b> The app generates 16 bytes (128 bits) of true random entropy via <code>os.urandom(16)</code>, displayed in hexadecimal notation.", bullet_style))
    story.append(Paragraph("<b>Step 3: Triple-Trial Benchmarking:</b> Both PBKDF2 and scrypt independently derive 32-byte (256-bit) keys across 3 distinct runs. High-resolution timestamps (<code>time.perf_counter()</code>) measure latency for Run 1, Run 2, Run 3, Average, Min, and Max.", bullet_style))
    story.append(Paragraph("<b>Step 4: Real-Time Tabulation:</b> An empirical table renders execution times, latency variance, and architectural attributes.", bullet_style))
    story.append(Paragraph("<b>Step 5: Visual Performance Analytics:</b> Grouped bar charts illustrate per-trial consistency, and a scatter plot maps the Computational Latency vs. Memory Frontier.", bullet_style))
    story.append(Paragraph("<b>Step 6: Cryptographic Material Display:</b> The generated AES-256 compatible keys are displayed in hex for inspection.", bullet_style))

    # Section 5: Academic & Viva Q&A
    story.append(Spacer(1, 6))
    story.append(Paragraph("5. Academic Viva & Defense Questions", h1_style))
    story.append(Paragraph("<b>Q1: Why do we measure 3 separate runs instead of just 1?</b><br/>"
                           "<i>Answer:</i> CPU execution time is subject to operating system scheduling, background daemon spikes, CPU frequency scaling, and cache warm-up. Taking 3 runs provides empirical validity and allows calculation of mean, min, and jitter.", body_style))
    story.append(Paragraph("<b>Q2: Can we just increase PBKDF2 iterations to equal scrypt's security?</b><br/>"
                           "<i>Answer:</i> No. Increasing PBKDF2 iterations slows down the legitimate authentication server, but because PBKDF2 requires zero memory, an attacker with an array of thousands of GPU or ASIC cores still retains a massive cost-efficiency advantage. Only memory-hardness directly undermines attacker hardware.", body_style))
    story.append(Paragraph("<b>Q3: What are current industry standards?</b><br/>"
                           "<i>Answer:</i> OWASP recommends memory-hard algorithms like Argon2id and scrypt. For legacy systems constrained to PBKDF2-HMAC-SHA256, OWASP mandates a minimum of 600,000 iterations.", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {filename}")

if __name__ == "__main__":
    build_pdf()
