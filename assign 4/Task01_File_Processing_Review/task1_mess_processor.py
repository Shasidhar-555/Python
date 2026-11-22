"""
Task 01: File-Processing Design Review - Diagnose and Repair a Poor Script
Course: CSA08 / CSA0807 Python Programming (CO4)
Bloom's Level: K4 - Analyse (6 Marks)

Problem Context - Hostel Mess Bill Processor:
A hostel office uses a flawed script to total mess bills recorded in a text file.
Each record contains: register number, name, amount.

Key Deliverables:
1. Task 1.1: Detailed diagnosis of 8 design deficiencies and business impact.
2. Task 1.2: Production-grade repaired function using context manager (with),
   line-by-line streaming, Decimal monetary precision, specific exception handling,
   and audit logging of rejected lines.
3. Task 1.3: Design defence for a 50,000-line file (<= 100 words).
4. Alternative Concept: Time and memory complexity analysis of f.read() vs
   f.readlines() vs line-by-line streaming across 50,000 records.
"""

import sys
import os
import time
import tracemalloc
from decimal import Decimal, InvalidOperation


# ==============================================================================
# 1. TASK 1.1: DIAGNOSIS OF DEFICIENCIES IN FLAWED SCRIPT
# ==============================================================================

DEFICIENCIES = [
    {
        "id": 1,
        "vulnerability": "Hardcoded File Path ('C:\\\\Users\\\\Office\\\\Desktop\\\\mess_oct.txt')",
        "technical_flaw": "Ties the script to a specific OS, drive, and local user account.",
        "office_consequence": "Script crashes with FileNotFoundError on any other PC, server, or if the file is moved."
    },
    {
        "id": 2,
        "vulnerability": "Unclosed File Stream (f = open(...), missing f.close() and 'with')",
        "technical_flaw": "OS file descriptor remains open until garbage collection cycles.",
        "office_consequence": "Risk of file descriptor exhaustion ('Too many open files') and data corruption if write buffers do not flush on abnormal termination."
    },
    {
        "id": 3,
        "vulnerability": "Eager Whole-File Loading (f.read() & data.split('\\n'))",
        "technical_flaw": "Allocates the entire file contents and an intermediate split list simultaneously in RAM.",
        "office_consequence": "On large multi-term or multi-hostel records (e.g. 50,000+ lines), memory bloats dramatically, triggering MemoryError / process kill on low-RAM office machines."
    },
    {
        "id": 4,
        "vulnerability": "Bare 'except:' with 'pass'",
        "technical_flaw": "Catches BaseException, suppressing KeyboardInterrupt, SystemExit, MemoryError, and NameError.",
        "office_consequence": "Users cannot cancel a hanging process (Ctrl+C). Corrupted or fraudulent billing records are silently ignored without alerts."
    },
    {
        "id": 5,
        "vulnerability": "Integer Conversion of Monetary Values (int(parts[2]))",
        "technical_flaw": "int() rejects strings containing decimals (e.g. '1250.50' raises ValueError).",
        "office_consequence": "Every student bill containing paise (fractional currency) triggers an exception and is silently discarded, resulting in massive revenue undercounting."
    },
    {
        "id": 6,
        "vulnerability": "Quadratic String Concatenation (report = report + ...)",
        "technical_flaw": "Strings are immutable; repeated concatenation creates intermediate string copies, yielding O(N^2) time complexity.",
        "office_consequence": "Generating reports for thousands of students slows the application to an unworkable crawl."
    },
    {
        "id": 7,
        "vulnerability": "Unchecked Trailing Empty Line Handling",
        "technical_flaw": "Standard text files terminate with a newline '\\n'. data.split('\\n') produces a trailing empty string ''.",
        "office_consequence": "Attempting parts[2] on '' raises IndexError, which relies on the bare except to avoid crashing, conflating formatting artifacts with real errors."
    },
    {
        "id": 8,
        "vulnerability": "Zero Record of Rejected Lines",
        "technical_flaw": "Exceptions are discarded with pass; no audit log, error count, or line number tracking exists.",
        "office_consequence": "Hostel accountants have no visibility into how many students were skipped or why the calculated total does not match physical bank receipts."
    }
]


def print_diagnosis():
    print("=" * 90)
    print("TASK 1.1: ARCHITECTURAL DIAGNOSIS OF FLAWED MESS BILL SCRIPT")
    print("=" * 90)
    for d in DEFICIENCIES:
        print(f"[{d['id']}] DEFICIENCY: {d['vulnerability']}")
        print(f"    Technical Flaw     : {d['technical_flaw']}")
        print(f"    Office Consequence : {d['office_consequence']}")
        print()


# ==============================================================================
# 2. TASK 1.2: REPAIRED DESIGN IMPLEMENTATION
# ==============================================================================

def process_mess_bills(filepath: str) -> dict:
    """
    Repaired file processor for hostel mess billing.
    Uses:
    - Context manager (with) for guaranteed stream cleanup
    - Line-by-line iteration (O(1) memory overhead)
    - Specific exceptions (ValueError, IndexError, InvalidOperation)
    - Decimal arithmetic for high-precision currency handling
    - Structured audit tracking for rejected lines
    - Parameterized input path
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Mess bill file not found: {filepath}")

    total_amount = Decimal("0.00")
    valid_records = []
    rejected_records = []

    with open(filepath, mode="r", encoding="utf-8") as f:
        for line_num, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            # Gracefully handle blank lines without throwing exceptions
            if not line:
                continue

            try:
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 3:
                    raise IndexError(f"Expected 3 fields (reg_no, name, amount), found {len(parts)}")

                reg_no, name, amount_str = parts[0], parts[1], parts[2]
                if not reg_no or not name:
                    raise ValueError("Student register number or name is empty")

                # Parse monetary amount using Decimal to prevent floating point inaccuracies
                amount = Decimal(amount_str).quantize(Decimal("0.01"))
                if amount < 0:
                    raise ValueError(f"Negative bill amount ({amount}) is invalid")

                total_amount += amount
                valid_records.append((reg_no, name, amount))

            except (IndexError, ValueError, InvalidOperation) as err:
                rejected_records.append({
                    "line_number": line_num,
                    "raw_content": raw_line.rstrip("\r\n"),
                    "reason": str(err)
                })

    # Efficient report construction via join (O(N) time)
    report_lines = [f"{name:<25} | Rs. {amount:>10.2f}" for _, name, amount in valid_records]
    report_str = "\n".join(report_lines)

    return {
        "total_amount": total_amount,
        "valid_count": len(valid_records),
        "rejected_count": len(rejected_records),
        "valid_records": valid_records,
        "rejected_records": rejected_records,
        "report": report_str
    }


# ==============================================================================
# 3. TASK 1.3: DESIGN DEFENCE (STRICTLY <= 100 WORDS)
# ==============================================================================

def print_design_defence():
    print("=" * 90)
    print("TASK 1.3: DESIGN DEFENCE FOR 50,000-LINE PROCESSING (<= 100 WORDS)")
    print("=" * 90)
    defence_text = (
        "Our repaired implementation processes 50,000 lines safely by streaming records line by line, "
        "maintaining O(1) memory instead of allocating entire files in RAM. The 'with' statement guarantees "
        "deterministic descriptor release even during runtime failures. Replacing int() with Decimal preserves "
        "exact currency with paise, preventing silent financial leakage. Specific exception handling isolates "
        "malformed records into an audit log without suppressing critical system signals or halting execution, "
        "while list joining eliminates quadratic string concatenation latency."
    )
    words = defence_text.split()
    print(defence_text)
    print(f"\nWord Count: {len(words)} words (Passes strict <= 100 words requirement: {len(words) <= 100})")
    print("=" * 90)


# ==============================================================================
# 4. ALTERNATIVE CONCEPT: F.READ() VS F.READLINES() VS LINE ITERATION
# ==============================================================================

def generate_synthetic_mess_file(filepath: str, n_records: int = 50_000):
    """Generates synthetic mess billing file with 50,000 records."""
    import random
    random.seed(42)
    names = ["Karthik", "Ravi", "Priya", "Anand", "Divya", "Suresh", "Meena", "Vijay", "Swetha", "Rajesh"]
    
    with open(filepath, "w", encoding="utf-8") as f:
        for i in range(1, n_records + 1):
            reg = f"192511{i:04d}"
            name = f"{random.choice(names)} Student_{i}"
            # Mix integer amounts and paise amounts
            amt = round(random.uniform(850.0, 3450.75), 2)
            # Inject 0.5% corrupt lines
            if i % 200 == 0:
                f.write(f"{reg},{name}\n")  # Missing amount
            elif i % 500 == 0:
                f.write(f"{reg},{name},INVALID_NUM\n")  # Non-numeric
            else:
                f.write(f"{reg},{name},{amt:.2f}\n")


def benchmark_file_reading_approaches(filepath: str):
    """
    Measures time and memory for:
    1. f.read() + splitlines()
    2. f.readlines()
    3. Line-by-line iteration (streaming generator)
    """
    print("\n" + "=" * 90)
    print("ALTERNATIVE CONCEPT & COMPLEXITY ANALYSIS: 50,000 LINES BENCHMARK")
    print("=" * 90)

    # Approach 1: f.read()
    tracemalloc.start()
    t0 = time.perf_counter()
    with open(filepath, "r", encoding="utf-8") as f:
        data = f.read()
        lines_read = data.splitlines()
        count_1 = len(lines_read)
    t_read = time.perf_counter() - t0
    mem_read = tracemalloc.get_traced_memory()[1] / (1024 * 1024)
    tracemalloc.stop()

    # Approach 2: f.readlines()
    tracemalloc.start()
    t0 = time.perf_counter()
    with open(filepath, "r", encoding="utf-8") as f:
        lines_readlines = f.readlines()
        count_2 = len(lines_readlines)
    t_readlines = time.perf_counter() - t0
    mem_readlines = tracemalloc.get_traced_memory()[1] / (1024 * 1024)
    tracemalloc.stop()

    # Approach 3: Line-by-line streaming
    tracemalloc.start()
    t0 = time.perf_counter()
    count_3 = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            count_3 += 1
    t_stream = time.perf_counter() - t0
    mem_stream = tracemalloc.get_traced_memory()[1] / (1024 * 1024)
    tracemalloc.stop()

    print(f"{'Method':<28} | {'Lines':<8} | {'Time (s)':<12} | {'Peak Memory (MB)':<18} | {'Space Complexity'}")
    print("-" * 90)
    print(f"{'1. f.read() + splitlines()':<28} | {count_1:<8,d} | {t_read:<12.5f} | {mem_read:<18.3f} | O(File Size)")
    print(f"{'2. f.readlines() list':<28} | {count_2:<8,d} | {t_readlines:<12.5f} | {mem_readlines:<18.3f} | O(File Size)")
    print(f"{'3. Line-by-line stream':<28} | {count_3:<8,d} | {t_stream:<12.5f} | {mem_stream:<18.3f} | O(One Line) [Optimal]")
    print("-" * 90)
    print("ANALYSIS: Line-by-line streaming maintains a constant micro-buffer (O(1) space),")
    print(f"consuming {mem_read / max(mem_stream, 0.001):.1f}x less RAM than eager reading while achieving identical O(N) throughput.")


# ==============================================================================
# 5. DEMONSTRATION & VERIFICATION ON SAMPLE FILE
# ==============================================================================

def main():
    sample_file = "mess_oct_sample.txt"
    sample_data = (
        "192511001, Karthik Harish, 1850.50\n"
        "192511002, Ravi Kumar, 2100.00\n"
        "192511003, Priya S, 1950.25\n"
        "192511004, Damaged Student\n"              # Missing amount
        "192511005, Corrupt Amount, Rs.3000\n"       # Invalid numeric format
        "192511006, Negative Bill, -500.00\n"        # Negative amount
        "192511007, Divya Raman, 2450.75\n"
        "\n"                                         # Empty line
    )
    with open(sample_file, "w", encoding="utf-8") as f:
        f.write(sample_data)

    print_diagnosis()
    
    print("\n" + "=" * 90)
    print("TASK 1.2: EXECUTING REPAIRED MESS BILL PROCESSOR ON SAMPLE DATA")
    print("=" * 90)
    results = process_mess_bills(sample_file)

    print("\n--- VALID STUDENT MESS REPORT ---")
    print(results["report"])
    print("-" * 45)
    print(f"Total Mess Revenue Collected : Rs. {results['total_amount']:,.2f}")
    print(f"Total Valid Bills Processed   : {results['valid_count']}")
    print(f"Total Rejected Corrupt Records: {results['rejected_count']}")

    print("\n--- REJECTED RECORDS AUDIT LOG ---")
    for r in results["rejected_records"]:
        print(f"• Line {r['line_number']}: '{r['raw_content']}' -> Error: {r['reason']}")

    assert results["valid_count"] == 4, "Expected 4 valid records"
    assert results["rejected_count"] == 3, "Expected 3 rejected records"
    assert results["total_amount"] == Decimal("8351.50"), f"Expected 8351.50, got {results['total_amount']}"
    print("\n[✓] All financial and audit assertions verified successfully.")

    print_design_defence()

    # Run 50,000-line empirical benchmark
    bench_file = "temp_mess_50000.txt"
    generate_synthetic_mess_file(bench_file, 50_000)
    benchmark_file_reading_approaches(bench_file)
    if os.path.exists(bench_file):
        os.remove(bench_file)


if __name__ == "__main__":
    main()
