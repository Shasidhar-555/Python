"""
Task 04: File and Exception Forensics - Library Returns Logging System
Course: CSA08 / CSA0807 Python Programming (CO4)
Bloom's Level: K4 - Analyse (7 Marks)

Problem Context - Library Book Return Logging:
A library script records daily returned books to returns.log.
Symptoms:
1. After 7 days, earlier days' returns are obliterated; only the last day survives.
2. Books returned on the same day are concatenated into a single unbroken string.
3. On one day, the program crashed with an unhandled exception, leaving no diagnostic log.

Key Deliverables:
1. Task 4.1: Forensic defect localization and root cause analysis.
2. Task 4.2: Automated 3-day test harness demonstrating all 3 defects empirically.
3. Task 4.3: Fully repaired program using append mode ('a'), explicit newlines,
   context managers ('with'), and structured audit logging.
4. Task 4.4: Two cardinal engineering rules to prevent defect recurrence.
5. Alternative Concept & Complexity Analysis: Manual try/finally vs 'with' statements,
   analyzing descriptor leaks and failure safety.
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path


# ==============================================================================
# 1. ORIGINAL FLAWED IMPLEMENTATION (FOR EVIDENCE & DEMONSTRATION)
# ==============================================================================

def save_returns_flawed(books, log_file="returns_flawed.log"):
    # DEFECT 1: mode='w' truncates the file every time, wiping previous days!
    log = open(log_file, "w")
    for b in books:
        # DEFECT 2: Missing '\n' concatenates book titles into one continuous string!
        # DEFECT 3: If write() raises an exception, log.close() is never reached!
        log.write(b)
    log.close()


def process_flawed(day_file, log_file="returns_flawed.log"):
    try:
        # DEFECT 4: open(day_file) is never closed explicitly!
        # DEFECT 5: split('\n') creates trailing empty string artifact.
        books = open(day_file).read().split("\n")
        save_returns_flawed(books, log_file)
    except FileNotFoundError:
        # DEFECT 6: Only FileNotFoundError is caught; all other exceptions crash unlogged!
        print("missing")


# ==============================================================================
# 2. TASK 4.2: CONSTRUCTING EMPIRICAL EVIDENCE (3-DAY TEST HARNESS)
# ==============================================================================

def run_flawed_evidence_test(work_dir: Path):
    print("=" * 90)
    print("TASK 4.2: CONSTRUCTING EMPIRICAL EVIDENCE (RUNNING FLAWED PROGRAM FOR 3 DAYS)")
    print("=" * 90)

    # Setup daily input files
    day1_file = work_dir / "day1_returns.txt"
    day2_file = work_dir / "day2_returns.txt"
    day3_file = work_dir / "day3_returns.txt"
    flawed_log = work_dir / "returns_flawed.log"

    day1_file.write_text("Clean Code\nDesign Patterns\n", encoding="utf-8")
    day2_file.write_text("Introduction to Algorithms\nPython Crash Course\n", encoding="utf-8")
    day3_file.write_text("Fluent Python\nThe Pragmatic Programmer\n", encoding="utf-8")

    # Run Day 1
    process_flawed(str(day1_file), str(flawed_log))
    day1_snapshot = flawed_log.read_text(encoding="utf-8")
    print(f"[Day 1 Processed] returns.log contents:\n'{day1_snapshot}'")

    # Run Day 2
    process_flawed(str(day2_file), str(flawed_log))
    day2_snapshot = flawed_log.read_text(encoding="utf-8")
    print(f"\n[Day 2 Processed] returns.log contents:\n'{day2_snapshot}'")

    # Run Day 3
    process_flawed(str(day3_file), str(flawed_log))
    day3_snapshot = flawed_log.read_text(encoding="utf-8")
    print(f"\n[Day 3 Processed] returns.log contents:\n'{day3_snapshot}'")

    print("\n" + "-" * 90)
    print("FORENSIC EVIDENCE SUMMARY:")
    print("1. DATA OBLITERATION: Day 1 ('Clean Code') and Day 2 ('Algorithms') are completely GONE!")
    print("   Only Day 3 returns exist because mode='w' executed an open-time truncation (truncate to 0).")
    print("2. DELIMITER CORRUPTION: Books on Day 3 are merged without spaces or linebreaks:")
    print(f"   '{day3_snapshot}' instead of separate parseable rows.")
    print("3. RESOURCE LEAK: File handles from open(day_file).read() remained unclosed by the OS.")
    print("-" * 90)


# ==============================================================================
# 3. TASK 4.3: REPAIRED PRODUCTION IMPLEMENTATION
# ==============================================================================

def log_library_error(error_msg: str, error_log_path: Path):
    """Logs timestamped errors with stack context to a dedicated error audit log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(error_log_path, mode="a", encoding="utf-8") as err_file:
        err_file.write(f"[{timestamp}] [ERROR] {error_msg}\n")


def save_returns_repaired(books: list[str], log_path: Path, date_str: str = None):
    """
    Repaired return recorder:
    - Uses append mode ('a') to preserve historical returns.
    - Appends explicit '\\n' delimiters to separate records cleanly.
    - Uses 'with' statement for deterministic file closure and buffer flushing.
    - Adds audit metadata (timestamp/date header).
    """
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    with open(log_path, mode="a", encoding="utf-8") as log:
        for book in books:
            clean_title = book.strip()
            if clean_title:
                log.write(f"[{date_str}] {clean_title}\n")


def process_repaired(day_file: Path, returns_log: Path, error_log: Path, date_str: str = None) -> bool:
    """
    Repaired file orchestrator:
    - Encapsulates both reading and writing in context managers.
    - Strips empty lines and whitespace artifacts.
    - Catches specific I/O and data exceptions, logging actionable diagnostics.
    """
    try:
        if not day_file.exists():
            raise FileNotFoundError(f"Daily return file '{day_file}' not found.")

        books = []
        with open(day_file, mode="r", encoding="utf-8") as f:
            for line_no, raw_line in enumerate(f, start=1):
                title = raw_line.strip()
                if title:
                    books.append(title)

        if not books:
            raise ValueError(f"Daily file '{day_file.name}' is empty (zero return records).")

        save_returns_repaired(books, returns_log, date_str)
        return True

    except (FileNotFoundError, PermissionError, UnicodeDecodeError, ValueError) as err:
        log_library_error(f"Failed processing '{day_file.name}': {err}", error_log)
        return False
    except Exception as unexpected:
        log_library_error(f"Unexpected critical error on '{day_file.name}': {unexpected}", error_log)
        raise


# ==============================================================================
# 4. DEMONSTRATION OF REPAIRED PROGRAM
# ==============================================================================

def run_repaired_verification(work_dir: Path):
    print("\n" + "=" * 90)
    print("TASK 4.3: VERIFYING REPAIRED PROGRAM (3-DAY PERSISTENCE & ERROR LOGGING)")
    print("=" * 90)

    repaired_log = work_dir / "returns_repaired.log"
    error_log = work_dir / "library_errors.log"

    # Reset logs
    if repaired_log.exists():
        repaired_log.unlink()
    if error_log.exists():
        error_log.unlink()

    day1 = work_dir / "day1_returns.txt"
    day2 = work_dir / "day2_returns.txt"
    day3 = work_dir / "day3_returns.txt"
    missing_day = work_dir / "day4_missing.txt"

    # Process Days 1, 2, 3 and simulated missing day
    s1 = process_repaired(day1, repaired_log, error_log, date_str="2026-10-01")
    s2 = process_repaired(day2, repaired_log, error_log, date_str="2026-10-02")
    s3 = process_repaired(day3, repaired_log, error_log, date_str="2026-10-03")
    s4 = process_repaired(missing_day, repaired_log, error_log, date_str="2026-10-04")

    print(f"Day 1 Processed: {s1}")
    print(f"Day 2 Processed: {s2}")
    print(f"Day 3 Processed: {s3}")
    print(f"Day 4 (Missing): {s4} (Gracefully caught & logged without crash)")

    print("\n--- REPAIRED RETURNS.LOG (CUMULATIVE AUDIT TRAIL) ---")
    print(repaired_log.read_text(encoding="utf-8").strip())

    print("\n--- LIBRARY ERRORS.LOG AUDIT TRAIL ---")
    print(error_log.read_text(encoding="utf-8").strip())

    # Assertions
    log_content = repaired_log.read_text(encoding="utf-8")
    assert "Clean Code" in log_content
    assert "Introduction to Algorithms" in log_content
    assert "Fluent Python" in log_content
    assert log_content.count("\n") == 6, "Expected exactly 6 distinct lines for 6 books"
    print("\n[✓] All 6 books across all 3 days safely persisted with distinct linebreaks.")
    print("[✓] Missing file event recorded in error log without crashing.")


# ==============================================================================
# 5. TASK 4.4: CARDINAL RULES TO PREVENT DEFECT RECURRENCE
# ==============================================================================

def print_prevention_rules():
    print("\n" + "=" * 90)
    print("TASK 4.4: TWO CARDINAL ENGINEERING RULES FOR ROBUST FILE PROCESSING")
    print("=" * 90)
    print("""
RULE 1: ALWAYS GOVERN FILE STREAMS WITH CONTEXT MANAGERS ('with open(...)')
- Never invoke bare open() without an immediately associated 'with' statement.
- The context manager guarantees deterministic invocation of __exit__(), ensuring that
  OS file descriptors are released and internal I/O buffers are flushed to disk even
  if exceptions, returns, or interruptions occur midway through execution.

RULE 2: STRICTLY DISTINGUISH ATOMIC OVERWRITE ('w') FROM AUDIT ACCUMULATION ('a')
- For logs, transactions, and event streams, always use append mode ('a') with explicit
  record delimiters ('\\n' or RFC-standard CSV delimiters).
- Never allow an incremental logging subsystem to open an audit destination in write mode ('w'),
  and never write record payloads without positive record termination characters.
""")
    print("=" * 90)


# ==============================================================================
# 6. ALTERNATIVE CONCEPT: MANUAL TRY/FINALLY VS CONTEXT MANAGERS
# ==============================================================================

def analyze_alternative_concept():
    print("\n" + "=" * 90)
    print("ALTERNATIVE CONCEPT AND COMPLEXITY ANALYSIS: MANUAL TRY/FINALLY VS 'WITH'")
    print("=" * 90)
    print("""
1. CODE STRUCTURE COMPARISON:
   Manual try/finally:
       log = open("returns.log", "a", encoding="utf-8")
       try:
           for b in books:
               log.write(f"{b}\\n")
       finally:
           log.close()

   Context Manager ('with'):
       with open("returns.log", "a", encoding="utf-8") as log:
           for b in books:
               log.write(f"{b}\\n")

2. COMPLEXITY ANALYSIS:
   - Time Complexity : O(N) in both implementations. Python's 'with' statement incurs
     virtually zero overhead (SETUP_WITH and WITH_EXCEPT_START bytecodes).
   - Space Complexity: O(1) in both.

3. DESCRIPTOR LEAK RISK & EXCEPTION SAFETY:
   - In manual try/finally:
     * If an error occurs between 'log = open()' and the entry of 'try:', the file descriptor
       leaks permanently until process termination.
     * When opening multiple files (e.g. reading from source and writing to destination),
       nesting multiple try/finally blocks leads to 'Pyramid of Doom' boilerplate where
       a failure in the second open() leaves the first file unclosed.
     * In contrast, 'with open(...) as f1, open(...) as f2:' guarantees that if the second
       open fails, f1 is automatically and deterministically closed by Python.
""")
    print("=" * 90)


# ==============================================================================
# 7. MAIN FUNCTION
# ==============================================================================

def main():
    work_dir = Path(__file__).resolve().parent
    run_flawed_evidence_test(work_dir)
    run_repaired_verification(work_dir)
    print_prevention_rules()
    analyze_alternative_concept()


if __name__ == "__main__":
    main()
