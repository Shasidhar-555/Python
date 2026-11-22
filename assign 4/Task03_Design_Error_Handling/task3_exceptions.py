"""
Task 03: Design the Error Handling - Exceptions in the Attendance Processor
Course: CSA08 / CSA0807 Python Programming (CO4)
Bloom's Level: K4 - Analyse (9 Marks)

Problem Context:
Designing robust exception architecture for biometric attendance file parsing.

Key Deliverables:
1. Task 3.1: Systematic Failure Taxonomy & Built-in Exception Mapping Table.
2. Task 3.2: Custom InvalidRecord exception design and boundary defense.
3. Task 3.3: Demonstration of the complete try-except-else-finally statement
   with exception chaining (raise ... from ...).
4. Task 3.4: Misuse Experiment demonstrating the dangers of bare 'except Exception: pass'.
5. Complete the Code: Fully working implementation of TODO 1 & 2 matching expected output:
   (1, 1, [(3, 'expected 3 fields, found 2'), (4, "invalid status 'L'")])
6. Non-existent file error handling in summarise().
7. Alternative Concept: EAFP (Easier to Ask Forgiveness) vs LBYL (Look Before You Leap)
   empirical latency comparison when bad lines are rare vs common.
"""

import os
import sys
import time
import tempfile


# ==============================================================================
# 1. TASK 3.1: SYSTEMATIC FAILURE TAXONOMY TABLE
# ==============================================================================

FAILURES_TAXONOMY = [
    {
        "failure_mode": "Missing directory or input file",
        "built_in_exception": "FileNotFoundError",
        "root_cause": "The specified attendance folder or daily file path does not exist on disk.",
        "mitigation_strategy": "Catch FileNotFoundError; log diagnostic alert and skip or create directory."
    },
    {
        "failure_mode": "Insufficient file read/write permissions",
        "built_in_exception": "PermissionError",
        "root_cause": "Operating system restricts read/write access (e.g. read-only volume or root-owned file).",
        "mitigation_strategy": "Catch PermissionError; alert administrator with full path and exit gracefully."
    },
    {
        "failure_mode": "Mismatched character encoding",
        "built_in_exception": "UnicodeDecodeError",
        "root_cause": "File contains byte sequences invalid under UTF-8 (e.g., Windows-1252 or corrupted bytes).",
        "mitigation_strategy": "Explicitly pass encoding='utf-8' with fallback encoding detection or error replacement."
    },
    {
        "failure_mode": "Malformed record (missing or excess fields)",
        "built_in_exception": "IndexError / ValueError",
        "root_cause": "Line does not contain exactly 3 comma-separated tokens.",
        "mitigation_strategy": "Raise custom InvalidRecord; catch in record loop to log line and continue."
    },
    {
        "failure_mode": "Invalid status token (not 'P' or 'A')",
        "built_in_exception": "ValueError",
        "root_cause": "Biometric device outputs non-standard tokens (e.g., 'L', 'LEAVE', 'X', '?').",
        "mitigation_strategy": "Validate against {'P', 'A'} whitelist; raise InvalidRecord."
    },
    {
        "failure_mode": "Empty input file (0 bytes)",
        "built_in_exception": "EOFError (or len == 0)",
        "root_cause": "Scanner failed to record any punches for that day.",
        "mitigation_strategy": "Check file size prior to loop; record warning in daily audit log."
    },
    {
        "failure_mode": "Path is a directory, not a file",
        "built_in_exception": "IsADirectoryError",
        "root_cause": "Scanner directory path passed directly to open().",
        "mitigation_strategy": "Use path.is_file() prior to open() or catch IsADirectoryError."
    }
]


def print_failure_taxonomy():
    print("=" * 90)
    print("TASK 3.1: SYSTEMATIC FAILURE TAXONOMY & BUILT-IN EXCEPTION MAPPING")
    print("=" * 90)
    print(f"{'Failure Condition':<30} | {'Built-in Exception':<22} | {'Mitigation Strategy'}")
    print("-" * 90)
    for f in FAILURES_TAXONOMY:
        print(f"{f['failure_mode']:<30} | {f['built_in_exception']:<22} | {f['mitigation_strategy']}")
    print("-" * 90)


# ==============================================================================
# 2. TASK 3.2: CUSTOM EXCEPTION DEFINITION
# ==============================================================================

class InvalidRecord(Exception):
    """
    Raised when a line of the attendance file violates schema or domain constraints.
    - Where Raised: Inside low-level validation parser parse_line()
    - Where Handled: Inside high-level orchestrator summarise() to preserve batch integrity.
    """
    def __init__(self, message: str, line_no: int = None, raw_content: str = None):
        super().__init__(message)
        self.message = message
        self.line_no = line_no
        self.raw_content = raw_content

    def __str__(self):
        if self.line_no is not None:
            return f"Line {self.line_no}: {self.message}"
        return self.message


# ==============================================================================
# 3. COMPLETE THE CODE (AS GIVEN IN ASSIGNMENT SPECIFICATION)
# ==============================================================================

def parse_line(line):
    """'192311001,2026-10-08,P' -> ('192311001', '2026-10-08', 'P')"""
    parts = line.strip().split(",")
    # TODO 1: Raise InvalidRecord if there are not exactly 3 fields or the status is
    #   not P or A; otherwise return the 3 fields as a tuple
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    
    reg_no, dt, status = parts[0].strip(), parts[1].strip(), parts[2].strip()
    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{status}'")
        
    return (reg_no, dt, status)


def summarise(path):
    present, absent, errors = 0, 0, []
    # TODO 2: Open the file with a with statement, parse each line inside try/except
    #   InvalidRecord, count P and A, and record (line number, message) for bad lines
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line_no, raw_line in enumerate(f, start=1):
                clean_line = raw_line.strip()
                if not clean_line:
                    continue
                try:
                    reg, dt, status = parse_line(clean_line)
                    if status == "P":
                        present += 1
                    elif status == "A":
                        absent += 1
                except InvalidRecord as e:
                    errors.append((line_no, str(e)))
    except FileNotFoundError:
        return present, absent, [(0, f"file not found: '{path}'")]
        
    return present, absent, errors


def run_complete_the_code():
    print("\n" + "=" * 90)
    print("TASK 3.2 & COMPLETE THE CODE EXECUTION")
    print("=" * 90)

    data = (
        "192311001,2026-10-08,P\n192311002,2026-10-08,A\n"
        "192311003,2026-10-08\n192311004,2026-10-08,L\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
        tmp.write(data)
    
    result = summarise(tmp.name)
    print("Observed Output:", result)
    expected = (1, 1, [(3, 'expected 3 fields, found 2'), (4, "invalid status 'L'")])
    print("Expected Output:", expected)
    assert result == expected, f"Output mismatch: expected {expected}, got {result}"
    print("[✓] Complete the Code passed all assertions matching expected assignment specification.")
    os.remove(tmp.name)

    # Test handling of non-existent file
    non_existent = "non_existent_attendance_file.csv"
    missing_result = summarise(non_existent)
    print(f"\nNon-existent File Test ('{non_existent}'):")
    print("Observed Output:", missing_result)
    assert missing_result[0] == 0 and missing_result[1] == 0 and len(missing_result[2]) == 1
    print("[✓] FileNotFoundError handled gracefully inside summarise().")


# ==============================================================================
# 4. TASK 3.3: DEMONSTRATING THE COMPLETE TRY STATEMENT & EXCEPTION CHAINING
# ==============================================================================

class AttendanceProcessingError(Exception):
    """Domain-level exception wrapping lower-level causes."""
    pass


def process_record_complete_try(filepath: str):
    print("\n" + "=" * 90)
    print("TASK 3.3: DEMONSTRATION OF COMPLETE TRY-EXCEPT-ELSE-FINALLY & EXCEPTION CHAINING")
    print("=" * 90)
    
    audit_events = []
    try:
        print("[1. TRY BLOCK] Opening file and executing parsing...")
        with open(filepath, "r", encoding="utf-8") as f:
            for lnum, line in enumerate(f, start=1):
                try:
                    rec = parse_line(line.strip())
                except InvalidRecord as parse_err:
                    print(f"    [NESTED EXCEPT] Line {lnum} invalid -> {parse_err}")
                else:
                    print(f"    [NESTED ELSE] Line {lnum} parsed successfully -> {rec}")
    except (FileNotFoundError, PermissionError) as io_err:
        print(f"[2. EXCEPT BLOCK] Caught I/O Failure: {io_err}")
        # Demonstrate exception chaining using 'raise ... from ...'
        raise AttendanceProcessingError("Critical failure during batch run") from io_err
    else:
        print("[3. ELSE BLOCK] File stream processed without unhandled top-level exceptions.")
        audit_events.append("PROCESS_SUCCESS")
    finally:
        print("[4. FINALLY BLOCK] Execution cleanup complete. Audit checkpoint saved.")
        audit_events.append("FINALLY_CLEANUP")

    return audit_events


# ==============================================================================
# 5. TASK 3.4: MISUSE EXPERIMENT (EXCEPT EXCEPTION: PASS)
# ==============================================================================

def summarise_misused_buggy(path):
    """
    Deliberately flawed implementation:
    Replaces specific exceptions with 'except Exception: pass', and introduces
    a typing error in variable name 'prsent += 1' instead of 'present += 1'.
    """
    present, absent, errors = 0, 0, []
    with open(path, "r", encoding="utf-8") as f:
        for line_no, raw_line in enumerate(f, start=1):
            try:
                parts = raw_line.strip().split(",")
                reg, dt, status = parts[0], parts[1], parts[2]
                if status == "P":
                    # TYPING ERROR: 'prsent' instead of 'present' raises NameError!
                    prsent += 1  # noqa: F821
                elif status == "A":
                    absent += 1
            except Exception:
                # Swallows NameError, ValueError, IndexError indiscriminately!
                pass
    return present, absent, errors


def run_misuse_experiment():
    print("\n" + "=" * 90)
    print("TASK 3.4: MISUSE EXPERIMENT - TYPING ERROR HIDDEN BY 'EXCEPT EXCEPTION: PASS'")
    print("=" * 90)

    test_data = "192511001,2026-10-08,P\n192511002,2026-10-08,P\n192511003,2026-10-08,A\n"
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
        tmp.write(test_data)
        
    result_flawed = summarise_misused_buggy(tmp.name)
    os.remove(tmp.name)

    print(f"Input records: 2 Present ('P'), 1 Absent ('A')")
    print(f"Flawed Function Output: Present = {result_flawed[0]}, Absent = {result_flawed[1]}")
    print("\nCRITICAL OBSERVATION & EXPLANATION:")
    print("• Notice that Present count is reported as 0 instead of 2!")
    print("• Why the error was hidden:")
    print("    1. Inside the loop, 'prsent += 1' triggered a NameError: name 'prsent' is not defined.")
    print("    2. Because 'except Exception:' catches all subclasses of Exception (including NameError),")
    print("       Python silently discarded the NameError and continued looping.")
    print("    3. No error was displayed, no crash occurred, yet the calculation was completely WRONG.")
    print("    4. This demonstrates why catching specific exceptions (InvalidRecord, ValueError) is mandatory.")


# ==============================================================================
# 6. ALTERNATIVE CONCEPT: EAFP VS LBYL EMPIRICAL BENCHMARK
# ==============================================================================

def parse_eafp(line: str):
    """EAFP: Easier to Ask Forgiveness than Permission (try/except)."""
    try:
        parts = line.split(",")
        status = parts[2]
        if status != "P" and status != "A":
            raise ValueError
        return parts[0], parts[1], status
    except (IndexError, ValueError):
        return None


def parse_lbyl(line: str):
    """LBYL: Look Before You Leap (if/else checks prior to access)."""
    parts = line.split(",")
    if len(parts) == 3:
        status = parts[2]
        if status == "P" or status == "A":
            return parts[0], parts[1], status
    return None


def benchmark_eafp_vs_lbyl():
    print("\n" + "=" * 90)
    print("ALTERNATIVE CONCEPT BENCHMARK: EAFP (TRY/EXCEPT) VS LBYL (IF CHECKS)")
    print("=" * 90)

    n_lines = 100_000

    # Scenario A: Corrupt records are RARE (99.9% clean records)
    clean_lines = ["192511001,2026-10-08,P"] * n_lines
    clean_lines[500] = "corrupt,line"

    t0 = time.perf_counter()
    _ = [parse_eafp(l) for l in clean_lines]
    t_eafp_clean = time.perf_counter() - t0

    t0 = time.perf_counter()
    _ = [parse_lbyl(l) for l in clean_lines]
    t_lbyl_clean = time.perf_counter() - t0

    # Scenario B: Corrupt records are COMMON (50% corrupt records)
    mixed_lines = ["192511001,2026-10-08,P" if i % 2 == 0 else "damaged,record" for i in range(n_lines)]

    t0 = time.perf_counter()
    _ = [parse_eafp(l) for l in mixed_lines]
    t_eafp_mixed = time.perf_counter() - t0

    t0 = time.perf_counter()
    _ = [parse_lbyl(l) for l in mixed_lines]
    t_lbyl_mixed = time.perf_counter() - t0

    print(f"{'Condition':<32} | {'EAFP try/except (s)':<22} | {'LBYL if/else (s)':<20} | {'Faster Style'}")
    print("-" * 90)
    print(f"{'Rare Bad Lines (99.9% Clean)':<32} | {t_eafp_clean:<22.5f} | {t_lbyl_clean:<20.5f} | {'EAFP' if t_eafp_clean < t_lbyl_clean else 'LBYL'}")
    print(f"{'Frequent Bad Lines (50% Corrupt)':<32} | {t_eafp_mixed:<22.5f} | {t_lbyl_mixed:<20.5f} | {'LBYL' if t_lbyl_mixed < t_eafp_mixed else 'EAFP'}")
    print("-" * 90)
    print("ANALYSIS: In Python, entering a try block is nearly free (zero opcode cost in 3.11+).")
    print("When errors are rare, EAFP runs faster. When exceptions are frequent, Python's traceback")
    print("and stack frame unwinding incurs overhead, making LBYL condition checks faster.")


# ==============================================================================
# 7. MAIN FUNCTION
# ==============================================================================

def main():
    print_failure_taxonomy()
    run_complete_the_code()
    
    # Run Complete Try Demonstration with clean temp file
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as t:
        t.write("192511001,2026-10-08,P\n192511002,2026-10-08,BAD\n")
        tmp_name = t.name
    process_record_complete_try(tmp_name)
    os.remove(tmp_name)

    run_misuse_experiment()
    benchmark_eafp_vs_lbyl()


if __name__ == "__main__":
    main()
