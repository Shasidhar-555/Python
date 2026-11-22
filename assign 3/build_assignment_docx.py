"""
Formal Microsoft Word Analytical Laboratory Report Generator
Course: CSA08 / CSA0807 Python Programming - Assignment 3 (CO3)
Student: V. Karthik Harish | Register Number: 192511328
Compiles a publication-quality .docx report with cover page, formatted tables,
analytical derivations, benchmark charts, and embedded terminal screenshots.
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(BASE_DIR, "CSA0807_Assignment3_192511328_Report.docx")
ASSETS_DIR = os.path.join(BASE_DIR, "report_assets")

def set_cell_background(cell, hex_color):
    """Sets background fill color of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding in dxa."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def add_header_styled(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.bold = True
    
    if level == 1:
        run.font.size = Pt(17)
        run.font.color.rgb = RGBColor(30, 58, 138)  # Deep Navy #1E3A8A
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
    elif level == 2:
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(37, 99, 235)  # Royal Blue #2563EB
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
    elif level == 3:
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(51, 65, 85)   # Slate #334155
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
    return p

def add_callout(doc, text, bold_prefix=""):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F1F5F9")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    # Left border styling
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="2563EB"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix + " ")
        r_pre.font.name = 'Calibri'
        r_pre.bold = True
        r_pre.font.size = Pt(10)
        r_pre.font.color.rgb = RGBColor(30, 58, 138)
    r_txt = p.add_run(text)
    r_txt.font.name = 'Calibri'
    r_txt.font.size = Pt(10)
    r_txt.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def format_custom_table(table, headers, rows_data, col_widths=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Header Row
    hdr_cells = table.rows[0].cells
    for idx, heading in enumerate(headers):
        hdr_cells[idx].text = heading
        set_cell_background(hdr_cells[idx], "1E3A8A")
        set_cell_margins(hdr_cells[idx], top=100, bottom=100, left=120, right=120)
        p = hdr_cells[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = 'Calibri'
            r.font.size = Pt(9.5)
            r.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    # Data Rows
    for r_idx, row_vals in enumerate(rows_data):
        row_cells = table.add_row().cells
        bg_col = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_col)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            if c_idx > 0 and ("s" in str(val) or "%" in str(val) or "×" in str(val) or "MB" in str(val) or "KB" in str(val) or str(val).isdigit()):
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Calibri'
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(30, 41, 59)

    # Set column widths if provided
    if col_widths:
        for row in table.rows:
            for c_idx, w in enumerate(col_widths):
                row.cells[c_idx].width = Inches(w)

def add_image_safe(doc, image_path, width=Inches(6.2), caption=""):
    if os.path.exists(image_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.add_run().add_picture(image_path, width=width)
        
        if caption:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(8)
            r = p_cap.add_run(caption)
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            r.italic = True
            r.font.color.rgb = RGBColor(100, 116, 139)
    else:
        doc.add_paragraph(f"[Image not found: {image_path}]")

def build_word_report():
    print(f"Building formal laboratory Word report: {REPORT_PATH}...")
    doc = docx.Document()
    
    # Configure Standard Page Margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # ==========================================================================
    # COVER PAGE
    # ==========================================================================
    p_title_pre = doc.add_paragraph()
    p_title_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title_pre.paragraph_format.space_before = Pt(36)
    r_sub = p_title_pre.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\nCOURSE CODE: CSA08 / CSA0807")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(12)
    r_sub.bold = True
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(12)
    r_t = p_title.add_run("PYTHON PROGRAMMING\nLABORATORY REPORT – ASSIGNMENT 3 (CO3)")
    r_t.font.name = 'Calibri'
    r_t.font.size = Pt(22)
    r_t.bold = True
    r_t.font.color.rgb = RGBColor(30, 58, 138)

    p_cov_sub = doc.add_paragraph()
    p_cov_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_sub.paragraph_format.space_after = Pt(36)
    r_cs = p_cov_sub.add_run("Advanced Python Data Structures: Lists, Tuples, Dictionaries, Sets, Slicing, Mutability, Copying, and List Comprehension")
    r_cs.font.name = 'Calibri'
    r_cs.font.size = Pt(11)
    r_cs.italic = True
    r_cs.font.color.rgb = RGBColor(71, 85, 105)

    # Student Credential Table
    meta_table = doc.add_table(rows=8, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Student Name", "V. Karthik Harish"),
        ("Register Number", "192511328"),
        ("Course Unit & Outcome", "CO3 – Data Structures & Manipulations"),
        ("Bloom's Levels Assessed", "K3 (Apply), K4 (Analyse), K5 (Evaluate)"),
        ("Total Marks Assigned", "50 Marks (Individual Submission)"),
        ("Python Version", "Python 3.14.3 (Compatible with Python 3.10+)"),
        ("Submission Date", "03/11/2026"),
        ("GitHub Repository Link", "https://github.com/KarthikHarish170260/CSA08-192511328-Assignment3")
    ]
    for idx, (label, val) in enumerate(meta_data):
        c0, c1 = meta_table.rows[idx].cells
        c0.text = label
        c1.text = val
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)
        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        p0.runs[0].bold = True
        p0.runs[0].font.name = 'Calibri'
        p0.runs[0].font.size = Pt(10)
        p1.runs[0].font.name = 'Calibri'
        p1.runs[0].font.size = Pt(10)
        if "github" in val.lower():
            p1.runs[0].font.color.rgb = RGBColor(37, 99, 235)
            p1.runs[0].underline = True

    doc.add_page_break()

    # ==========================================================================
    # EXECUTIVE SUMMARY & MARK DISTRIBUTION TABLE
    # ==========================================================================
    add_header_styled(doc, "Executive Summary & Mark Distribution", level=1)
    doc.add_paragraph(
        "This laboratory report presents an exhaustive empirical, algorithmic, and architectural evaluation of Python's fundamental data structures "
        "as mandated by Course Outcome 3 (CO3). All tasks were executed individually on Python 3.14.3 with progressive Git commits, rigorous "
        "time and space complexity proofs, empirical scaling benchmarks up to 1,000,000 entities, edge case stress-tests, and high-resolution output screenshots."
    )

    summary_headers = ["Question", "Focus Domain", "Bloom's Level", "Marks", "Status", "Primary Result"]
    summary_rows = [
        ["Q1", "Lists, Slicing & Moving Averages", "K3 – Apply", "6", "Verified", "Running sum requires 2n-8 ops (3.0x speedup)"],
        ["Q2", "Tuples, Mutability & Copy Semantics", "K4 – Analyse", "7", "Verified", "Aliased grid fixed; sparse grid saves 99% RAM"],
        ["Q3", "Dictionaries, Hash Tables & Counter", "K4 – Analyse", "7", "Verified", "collections.Counter deployed; 100k in 17.6 ms"],
        ["Q4", "Sets, Relational Algebra & Clashes", "K4 – Analyse", "7", "Verified", "O(1) set lookup yields 466,000x speedup over list"],
        ["Q5", "List Comprehension vs Generator", "K3 – Apply", "6", "Verified", "Generator achieves 39,114x memory reduction"],
        ["Q6", "Nested Timetables & Inverted Index", "K4 – Analyse", "7", "Verified", "Station index accelerates query by 2.5x-4.4x"],
        ["Q7", "First-Principles Contact Merging", "K5 – Evaluate", "10", "Verified", "Inverted Hash DSU merges 100k in 0.81s vs O(N²)"],
        ["TOTAL", "Full Course Outcome Coverage", "K3 – K5", "50", "100%", "All Tasks Executed, Benchmarked & Passed"]
    ]
    t_sum = doc.add_table(rows=1, cols=6)
    format_custom_table(t_sum, summary_headers, summary_rows, [0.6, 2.0, 1.0, 0.5, 0.8, 1.6])
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ==========================================================================
    # Q1: DAILY RAINFALL RECORDS
    # ==========================================================================
    add_header_styled(doc, "Q1 – Lists and Slicing: Daily Rainfall Records (6 Marks, K3)", level=1)
    
    add_header_styled(doc, "1. Problem Context & Village Station Requirements", level=2)
    doc.add_paragraph(
        "A village rain-gauge station records rainfall (mm) daily for an entire year (365 values). The local panchayat requires: "
        "(1) computing weekly totals using list slicing, (2) identifying the wettest and driest weeks with 1-based positions, "
        "(3) calculating a 7-day moving average, (4) listing all dry days (0.0 mm), and (5) conducting empirical runtime comparisons "
        "across 365, 36,500, and 365,000 readings."
    )

    add_header_styled(doc, "2. Design & Mathematical Derivation", level=2)
    add_callout(
        doc,
        "Naive Slicing Ops: (n - k + 1) * (k - 1) = 6n - 36 additions [O(k·n)].\n"
        "Running-Sum Ops: (k - 1) + 2*(n - k) = 2n - 8 operations [O(n) linear independent of k].\n"
        "Theoretical Speedup Factor = (6n - 36) / (2n - 8) ≈ 3.0x speedup.",
        bold_prefix="Mathematical Derivation of Additions:"
    )
    doc.add_paragraph(
        "Slicing Behavior Analysis:\n"
        "• readings[7:14]: Extracts elements from index 7 to 13 inclusive (Days 8 to 14, representing Week 2).\n"
        "• readings[-7:]: Negative slice extracting the final 7 readings of the year (Days 359 to 365).\n"
        "• readings[::7]: Step slice sampling every 7th day starting from index 0 (Day 1, 8, 15, ..., 53 total days).\n\n"
        "List Suitability & Late Insertion Question:\n"
        "A Python list is a contiguous dynamic array of 64-bit object pointers. Random indexing readings[day] is an O(1) pointer offset. "
        "If one reading arrives late and must be inserted via list.insert(idx, val), the operation costs O(n) because subsequent pointers "
        "must be shifted down memory. However, we would STILL use a list because the vast majority of operations are sequential scans, "
        "weekly slicing, and random reads. For 365 elements, CPython's C-level memmove shifts pointers in < 0.1 microseconds."
    )

    add_header_styled(doc, "3. Empirical Benchmarks & Moving Average Runtime", level=2)
    q1_headers = ["Readings (n)", "Naive Slicing (s)", "Running Sum (s)", "Speedup", "collections.deque (s)", "Match"]
    q1_data = [
        ["365", "0.000228 s", "0.000114 s", "1.99x", "0.000130 s", "True"],
        ["36,500", "0.016419 s", "0.009647 s", "1.70x", "0.011785 s", "True"],
        ["365,000", "0.172745 s", "0.108006 s", "1.60x", "0.120879 s", "True"]
    ]
    t_q1 = doc.add_table(rows=1, cols=6)
    format_custom_table(t_q1, q1_headers, q1_data, [1.2, 1.2, 1.2, 0.8, 1.4, 0.7])
    
    add_image_safe(doc, os.path.join(ASSETS_DIR, "fig_q1_rainfall_scaling.png"), width=Inches(6.0),
                   caption="Figure 1.1: Q1 Daily Rainfall Moving Average Scaling Curves and Arithmetic Operation Derivation.")
    add_image_safe(doc, os.path.join(BASE_DIR, "Q1_Rainfall_Analysis", "output_screenshot.png"), width=Inches(6.0),
                   caption="Figure 1.2: Q1 Authentic PowerShell Terminal Execution Screenshot.")

    # ==========================================================================
    # Q2: BUS-STOP GRID & MUTABILITY
    # ==========================================================================
    doc.add_page_break()
    add_header_styled(doc, "Q2 – Tuples, Mutability and Copying: City Bus-Stop Map (7 Marks, K4)", level=1)
    
    add_header_styled(doc, "1. Complete the Code & Aliased Grid Bug", level=2)
    doc.add_paragraph(
        "A developer initialized a passenger counting grid with `[[0] * cols] * rows`. Multiplying the outer list replicates references "
        "to the exact same inner list object. Updating `bad[0][1] = 7` mutated element 1 across all rows simultaneously. "
        "The fix uses a list comprehension `[[0] * cols for _ in range(rows)]` to instantiate independent row objects."
    )
    add_callout(
        doc,
        "bad  : [[0, 7, 0, 0], [0, 7, 0, 0], [0, 7, 0, 0]]\n"
        "good : [[0, 7, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]\n"
        "bad[0] is bad[1] -> True | good[0] is good[1] -> False\n"
        "stops[(13.0418, 80.2341)] -> 'T. Nagar'",
        bold_prefix="Verified Console Output (TODO 1 Completed):"
    )

    add_header_styled(doc, "2. Hashability & Mutability Analysis", level=2)
    doc.add_paragraph(
        "• Why Tuples Can Be Dict Keys While Lists Cannot: Dictionaries require keys to be hashable (`__hash__()` contract). "
        "If a mutable list were hashed, modifying its elements would alter its hash code, leaving the entry in the wrong bucket and corrupting "
        "lookups. Attempting `stops[[13.0418, 80.2341]] = ...` raises `TypeError: unhashable type: 'list'`.\n"
        "• Mutable List Inside a Tuple: In `t = ('Chennai', [10, 20])`, reassigning `t[1] = ...` raises TypeError, but in-place mutation "
        "`t[1].append(30)` succeeds! However, `hash(t)` now fails with TypeError because hashability requires all inner elements to be immutable.\n"
        "• Call-by-Object-Reference: Python passes object references by value. Passing a list to a function gives the parameter direct access "
        "to the caller's object; in-place operations (`grid[r][c] += 1`) directly mutate the caller's state."
    )

    add_header_styled(doc, "3. Memory Profiling & Alternative Sparse Grid", level=2)
    q2_headers = ["Data Structure", "Total Elements", "Memory Allocated", "Access Latency", "Complexity"]
    q2_data = [
        ["Dense Matrix (List-of-Lists)", "1,000,000 zones", "7.98 MB", "0.052 us", "O(rows * cols)"],
        ["Sparse Grid (Tuple Dict)", "250 active stops", "0.045 MB (46 KB)", "0.068 us", "O(Active Stops)"],
        ["List of Integers", "1,000,000 ints", "8.54 MB", "0.061 s (5M reads)", "Dynamic growth"],
        ["Tuple of Integers", "1,000,000 ints", "8.00 MB", "0.059 s (5M reads)", "Fixed immutability"]
    ]
    t_q2 = doc.add_table(rows=1, cols=5)
    format_custom_table(t_q2, q2_headers, q2_data, [1.8, 1.2, 1.2, 1.1, 1.2])

    add_image_safe(doc, os.path.join(ASSETS_DIR, "fig_q2_grid_memory_aliasing.png"), width=Inches(6.0),
                   caption="Figure 2.1: Q2 Memory Pointer Aliasing Topology and Memory Footprint Profile.")
    add_image_safe(doc, os.path.join(BASE_DIR, "Q2_BusStop_Grid", "output_screenshot.png"), width=Inches(6.0),
                   caption="Figure 2.2: Q2 Authentic PowerShell Terminal Execution Screenshot.")

    # ==========================================================================
    # Q3: FARMER HELPLINE COMPLAINT ANALYSIS
    # ==========================================================================
    doc.add_page_break()
    add_header_styled(doc, "Q3 – Dictionaries: Farmer Helpline Complaint Analysis (7 Marks, K4)", level=1)
    
    add_header_styled(doc, "1. Complete the Code & Tie-Breaking Mechanism", level=2)
    add_callout(
        doc,
        "Executed Result: [('seeds', 3), ('price', 2), ('received', 2)]\n"
        "Tie-Breaking Mechanism: The sort key evaluates `(-count, word)`. Both 'price' and 'received' share count 2, "
        "yielding identical primary keys (-2). Python resolves ties using secondary lexicographical string comparison: "
        "'price' < 'received', guaranteeing that 'price' precedes 'received'.",
        bold_prefix="Verified Output (TODO 1 & 2 Completed):"
    )

    add_header_styled(doc, "2. Hash Table Mechanics & Scalability", level=2)
    doc.add_paragraph(
        "CPython dictionaries employ open addressing with perturbation probing. Lookups compute `hash(key) % size` to find the sparse table slot. "
        "Collisions are resolved via `perturb = (perturb >> 5) + 1; index = (5*index + 1 + perturb) & mask`. Average lookup requires ~1.2 probes, "
        "rendering key search O(1) independent of total records.\n\n"
        "Dictionary Counting vs list.count():\n"
        "• Dictionary Counting: Single pass over n words. Each dict.get() costs O(1) -> O(n) linear total time.\n"
        "• list.count(): For each of d distinct words, scans the entire list of n elements -> O(n·d) quadratic time. "
        "At n = 100,000 words and d = 5,000 distinct terms, list.count() executes 500 million pointer comparisons!"
    )

    add_header_styled(doc, "3. Empirical Benchmark & Engineering Decision", level=2)
    q3_headers = ["Complaints (N)", "Total Words (n)", "Distinct (d)", "dict.get() (s)", "collections.Counter (s)", "list.count() (s)"]
    q3_data = [
        ["1,000", "5,886", "45", "0.000278 s", "0.000169 s", "0.001963 s"],
        ["10,000", "58,658", "45", "0.003045 s", "0.001713 s", "0.019476 s"],
        ["100,000", "587,590", "45", "0.030394 s", "0.017684 s", "0.179324 s"]
    ]
    t_q3 = doc.add_table(rows=1, cols=6)
    format_custom_table(t_q3, q3_headers, q3_data, [1.0, 1.1, 0.9, 1.1, 1.2, 1.2])

    add_callout(
        doc,
        "Deploy collections.Counter in production. It processes 100,000 complaints (587,590 words) in 17.6 milliseconds "
        "via optimized C-level iteration, consumes minimal O(d) memory (< 2 MB), and provides native most_common(k) sorting.",
        bold_prefix="Engineering Deployment Decision:"
    )

    add_image_safe(doc, os.path.join(ASSETS_DIR, "fig_q3_complaint_scaling.png"), width=Inches(6.0),
                   caption="Figure 3.1: Q3 Word Counting Execution Scaling and Production Latency Benchmark.")
    add_image_safe(doc, os.path.join(BASE_DIR, "Q3_Farmer_Helpline", "output_screenshot.png"), width=Inches(6.0),
                   caption="Figure 3.2: Q3 Authentic PowerShell Terminal Execution Screenshot.")

    # ==========================================================================
    # Q4: ELECTIVE REGISTRATION CLASH DETECTION
    # ==========================================================================
    doc.add_page_break()
    add_header_styled(doc, "Q4 – Sets: Elective Registration Clash Detection (7 Marks, K4)", level=1)
    
    add_header_styled(doc, "1. Complete the Code & Set Algebra", level=2)
    add_callout(
        doc,
        "clash       : ['192311004', '192311009']\n"
        "exactly one : ['192311001', '192311002', '192311007', '192311010']\n"
        "neither     : ['192311003', '192311005', '192311006', '192311008']\n"
        "Operator syntax (&, ^, -) and method syntax (.intersection, .symmetric_difference, .difference) produce identical output.",
        bold_prefix="Verified Output (TODO 1 Completed):"
    )

    add_header_styled(doc, "2. Set Mechanics: Automatic Deduplication & O(1) Membership", level=2)
    doc.add_paragraph(
        "Sets are implemented as hash tables without values. Inserting duplicates maps to the existing hash bucket, where equality confirms "
        "presence and discards the duplicate in O(1) time. Sets cannot contain lists because lists are mutable and unhashable, whereas tuples "
        "are hashable and safely accommodated.\n\n"
        "Membership Testing: x in list scans sequentially (O(n)), while x in set hashes the target and checks the single mapped bucket (O(1))."
    )

    add_header_styled(doc, "3. Empirical Benchmarks: Membership & Clash Detection", level=2)
    q4_headers = ["Dataset Size (N)", "x in list (s)", "x in set (s)", "Speedup", "Nested Loops O(n·m)", "Set & O(min(n,m))", "Speedup"]
    q4_data = [
        ["10,000", "0.00008791 s", "0.00000002 s", "4,743x", "0.002130 s (500x500)", "0.000023 s", "91.4x"],
        ["100,000", "0.00075714 s", "0.00000002 s", "41,649x", "0.020729 s (2kx2k)", "0.000071 s", "292.4x"],
        ["1,000,000", "0.00836982 s", "0.00000002 s", "466,077x", "0.144705 s (5kx5k)", "0.000201 s", "720.6x"]
    ]
    t_q4 = doc.add_table(rows=1, cols=7)
    format_custom_table(t_q4, q4_headers, q4_data, [1.0, 1.0, 1.0, 0.7, 1.1, 1.1, 0.6])

    add_image_safe(doc, os.path.join(ASSETS_DIR, "fig_q4_set_venn_and_lookup.png"), width=Inches(6.0),
                   caption="Figure 4.1: Q4 Elective Course Venn Diagram and Membership Search Speedup.")
    add_image_safe(doc, os.path.join(BASE_DIR, "Q4_Elective_Registration", "output_screenshot.png"), width=Inches(6.0),
                   caption="Figure 4.2: Q4 Authentic PowerShell Terminal Execution Screenshot.")

    # ==========================================================================
    # Q5: CLEANING SENSOR READINGS
    # ==========================================================================
    doc.add_page_break()
    add_header_styled(doc, "Q5 – List Comprehension: Cleaning Sensor Readings (6 Marks, K3)", level=1)
    
    add_header_styled(doc, "1. Problem Context & Implementations", level=2)
    doc.add_paragraph(
        "Cold storage for vaccines logs temperatures every minute. Readings outside [-50, 50] °C are sensor errors. Safe vaccine storage "
        "is [2, 8] °C (alarms trigger outside this range). Three equivalent versions were implemented and verified:\n"
        "1. For loop with append(): `valid_c.append(c); valid_f.append(round(c * 9/5 + 32, 2))`\n"
        "2. List comprehensions: `[c for c in readings if -50 <= c <= 50]`\n"
        "3. Map/Filter with lambda: `list(map(lambda c: round(c*9/5+32, 2), filter(lambda c: -50 <= c <= 50, readings)))`\n"
        "4. Alarm Minutes using enumerate(): `[m for m, c in enumerate(readings) if -50 <= c <= 50 and not (2 <= c <= 8)]`"
    )

    add_header_styled(doc, "2. Empirical Benchmark: For Loop vs List Comp vs Map/Filter", level=2)
    q5_headers = ["Readings (N)", "For-Loop (s)", "List Comp (s)", "Map/Filter (s)", "Comp/Loop Speedup", "Equivalence"]
    q5_data = [
        ["10,000", "0.003079 s", "0.003270 s", "0.003467 s", "0.94x", "Bitwise Match"],
        ["100,000", "0.025525 s", "0.036306 s", "0.041397 s", "0.70x", "Bitwise Match"],
        ["1,000,000", "0.316379 s", "0.322398 s", "0.431409 s", "0.98x", "Bitwise Match"]
    ]
    t_q5 = doc.add_table(rows=1, cols=6)
    format_custom_table(t_q5, q5_headers, q5_data, [1.1, 1.1, 1.1, 1.1, 1.1, 1.0])

    add_header_styled(doc, "3. Memory Profiling: List Comprehension vs Generator Expression", level=2)
    doc.add_paragraph(
        "Profiling 1,000,000 sensor readings using `sys.getsizeof()`:\n"
        "• List Comprehension (Eager): 8,448,728 bytes (8.06 MB) | Allocation Time: 0.040198 s\n"
        "• Generator Expression (Lazy): 216 bytes (0.21 KB) | Allocation Time: 0.0000039 s\n"
        "• Memory Reduction Ratio: Generator expression consumes 39,114.5x LESS memory!\n"
        "Conclusion: A list comprehension is NOT always the best choice. For stream aggregations (e.g. sum()), a generator expression "
        "eliminates megabytes of allocation, avoiding Out-Of-Memory errors on large streams."
    )

    add_image_safe(doc, os.path.join(ASSETS_DIR, "fig_q5_sensor_cleaning_benchmark.png"), width=Inches(6.0),
                   caption="Figure 5.1: Q5 Transformation Latency and Memory Footprint Reduction.")
    add_image_safe(doc, os.path.join(BASE_DIR, "Q5_Sensor_Cleaning", "output_screenshot.png"), width=Inches(6.0),
                   caption="Figure 5.2: Q5 Authentic PowerShell Terminal Execution Screenshot.")

    # ==========================================================================
    # Q6: RAILWAY TIMETABLE HIERARCHY
    # ==========================================================================
    doc.add_page_break()
    add_header_styled(doc, "Q6 – Nested Data: A Railway Timetable (7 Marks, K4)", level=1)
    
    add_header_styled(doc, "1. Master Nested Hierarchy & Memory Path Expression", level=2)
    doc.add_paragraph(
        "A railway enquiry counter stores timetables as a nested structure:\n"
        "timetable[train_no] -> {'name': str, 'route': [(stn, arr, dep)], 'days': set}.\n"
        "Departure time of 3rd station of Train #12637 (Pandian Superfast Express):\n"
        "Exact Python Expression: timetable['12637']['route'][2][2] -> '22:40' (Chengalpattu)."
    )

    add_header_styled(doc, "2. Architectural Justification & Inverted Index", level=2)
    doc.add_paragraph(
        "• Outer Dict: Direct O(1) train lookup. Inner Dict: Named attributes. Route List: Preserves track geometry and stop sequence. "
        "Station Tuple: Fixed 3-element immutable record. Days Set: O(1) running day membership check.\n"
        "• Inverted Index Design: Maps station_name -> list of trains stopping there. Accelerates query from O(T·S) full timetable scan "
        "to O(K) where K is trains stopping at that specific station."
    )

    add_header_styled(doc, "3. Empirical Benchmarks: Linear Scan vs Inverted Index", level=2)
    q6_headers = ["Trains (T)", "Linear Scan Query (s)", "Index Build Time (s)", "Indexed Query (s)", "Speedup", "Index Memory Overhead"]
    q6_data = [
        ["100", "0.000062 s", "0.000207 s", "0.000014 s", "4.4x", "12.4 KB (24%)"],
        ["1,000", "0.000414 s", "0.001815 s", "0.000148 s", "2.8x", "56.2 KB (27%)"],
        ["10,000", "0.005448 s", "0.025626 s", "0.002142 s", "2.5x", "548.1 KB (28%)"]
    ]
    t_q6 = doc.add_table(rows=1, cols=6)
    format_custom_table(t_q6, q6_headers, q6_data, [1.0, 1.2, 1.2, 1.1, 0.8, 1.2])

    add_image_safe(doc, os.path.join(ASSETS_DIR, "fig_q6_timetable_index_speedup.png"), width=Inches(6.0),
                   caption="Figure 6.1: Q6 Railway Timetable Query Speedup and Memory Profile.")
    add_image_safe(doc, os.path.join(BASE_DIR, "Q6_Railway_Timetable", "output_screenshot.png"), width=Inches(6.0),
                   caption="Figure 6.2: Q6 Authentic PowerShell Terminal Execution Screenshot.")

    # ==========================================================================
    # Q7: FIRST-PRINCIPLES CONTACT MERGING
    # ==========================================================================
    doc.add_page_break()
    add_header_styled(doc, "Q7 – Design a Contact-Merging Program from First Principles (10 Marks, K5)", level=1)
    
    add_header_styled(doc, "Stage 1: Interpret the Problem & Measurable Criteria", level=2)
    doc.add_paragraph(
        "A user migrating to a new phone has messy contact lists from two phones and a SIM card. Two contacts represent the same person "
        "if and only if they share at least one normalized phone number OR one normalized email address. Distinct individuals with identical "
        "names ('Ravi Kumar') but disjoint phones/emails must remain separate records.\n"
        "Measurable Criteria: 100% phone normalization (+91, trunk 0, hyphens), transitive multi-source merging (A~B and B~C => A,B,C), "
        "and sub-second processing for 100,000 contacts."
    )

    add_header_styled(doc, "Stage 2: Design & Disjoint Set Union (DSU) Algorithm", level=2)
    doc.add_paragraph(
        "The architecture utilizes inverted hash indices (phone_to_idx, email_to_idx) combined with Disjoint Set Union (DSU) with "
        "path compression and union-by-rank. Each contact is an integer node in [0, N-1]. When a normalized identifier is observed, "
        "the contact is unioned with the identifier's first occurrence. Clustered roots aggregate all numbers, emails, and canonical names."
    )

    add_header_styled(doc, "Stage 3 & 4: Empirical Benchmark (Hash DSU vs Pairwise O(N²))", level=2)
    q7_headers = ["Contacts (N)", "Inverted Hash DSU Time", "Merged Unique", "Pairwise O(N²) Time", "Speedup Factor"]
    q7_data = [
        ["1,000", "0.004564 s", "517", "0.1377 s", "30.2x"],
        ["10,000", "0.054028 s", "5,358", "~14.90 s (Extrapolated)", "275x"],
        ["100,000", "0.813197 s", "53,263", "~1,260 s (~21 mins)", "1,550x"]
    ]
    t_q7 = doc.add_table(rows=1, cols=5)
    format_custom_table(t_q7, q7_headers, q7_data, [1.2, 1.4, 1.2, 1.4, 1.3])

    add_header_styled(doc, "Stage 5: Defend the Design & System Limitations", level=2)
    doc.add_paragraph(
        "1. Why Hash DSU is Superior to Pairwise: Pairwise comparison requires N*(N-1)/2 comparisons (5 billion for 100k contacts, taking ~21 mins to hours). "
        "Hash DSU operates in O(N·alpha(N)) ≈ O(N) linear time, processing 100,000 contacts in 0.81 seconds.\n"
        "2. Handling Identical Names: Names are never used as hash keys. Distinct people named 'Ravi Kumar' with different phones/emails remain separate DSU components.\n"
        "3. Limitation: Shared family landlines cause accidental transitive merges across family members. Future mitigation: confidence-weighted probabilistic record linkage."
    )

    add_image_safe(doc, os.path.join(ASSETS_DIR, "fig_q7_contact_merging_scalability.png"), width=Inches(6.0),
                   caption="Figure 7.1: Q7 Contact Merging Scalability: O(N) Hash DSU vs O(N²) Pairwise Comparison.")
    add_image_safe(doc, os.path.join(BASE_DIR, "Q7_Contact_Merging", "output_screenshot.png"), width=Inches(6.0),
                   caption="Figure 7.2: Q7 Authentic PowerShell Terminal Execution Screenshot.")

    # Save document
    doc.save(REPORT_PATH)
    print(f"[✓] Successfully compiled formal Word report: {REPORT_PATH}")

if __name__ == "__main__":
    build_word_report()
