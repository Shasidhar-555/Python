"""
Master Test Runner: Executes and Verifies All 6 Tasks
File: run_all_tasks.py
Course: CSA08 - Python Programming (Assignment 4)
Student: V. Karthik Harish (Reg No: 192511328)

Sequentially executes Task01 through Task06, checks execution status codes,
asserts that expected output artifacts and screenshots exist, and outputs
a unified verification summary table.
"""

import os
import sys
import subprocess
import time

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

TASKS = [
    {
        "id": "Task 01",
        "name": "Mess Bill Processor Diagnosis & Repair",
        "script": os.path.join(REPO_ROOT, "Task01_File_Processing_Review", "task1_mess_processor.py"),
        "cwd": os.path.join(REPO_ROOT, "Task01_File_Processing_Review"),
        "artifacts": ["output.txt", "output_screenshot.png"]
    },
    {
        "id": "Task 02",
        "name": "Biometric Attendance Processing & Reports",
        "script": os.path.join(REPO_ROOT, "Task02_Requirement_To_Design", "task2_attendance_design.py"),
        "cwd": os.path.join(REPO_ROOT, "Task02_Requirement_To_Design"),
        "artifacts": ["output.txt", "output_screenshot.png", "attendance_summary.csv", "defaulters_below_75.txt", "damaged_records.log"]
    },
    {
        "id": "Task 03",
        "name": "Exception Hierarchy, InvalidRecord & Complete try",
        "script": os.path.join(REPO_ROOT, "Task03_Design_Error_Handling", "task3_exceptions.py"),
        "cwd": os.path.join(REPO_ROOT, "Task03_Design_Error_Handling"),
        "artifacts": ["output.txt", "output_screenshot.png"]
    },
    {
        "id": "Task 04",
        "name": "Library Returns Forensics & Append Repair",
        "script": os.path.join(REPO_ROOT, "Task04_Forensics_And_Repair", "task4_library_forensics.py"),
        "cwd": os.path.join(REPO_ROOT, "Task04_Forensics_And_Repair"),
        "artifacts": ["output.txt", "output_screenshot.png", "library_errors.log"]
    },
    {
        "id": "Task 05",
        "name": "Four Organisations Comparison & sys.modules Caching",
        "script": os.path.join(REPO_ROOT, "Task05_Four_Organisations", "task5_compare_runner.py"),
        "cwd": os.path.join(REPO_ROOT, "Task05_Four_Organisations"),
        "artifacts": ["output.txt", "output_screenshot.png"]
    },
    {
        "id": "Task 06",
        "name": "Cultural Fest Registration Desk & Set Deduplication",
        "script": os.path.join(REPO_ROOT, "Task06_Design_Challenge", "task6_fest_desk.py"),
        "cwd": os.path.join(REPO_ROOT, "Task06_Design_Challenge"),
        "artifacts": [
            "output.txt",
            "output_screenshot.png",
            os.path.join("outputs", "master_registered_students.csv"),
            os.path.join("outputs", "fest_summary_report.txt"),
            os.path.join("outputs", "fest_processing_errors.log")
        ]
    }
]


def run_suite():
    print("=" * 86)
    print("CSA08 - PYTHON PROGRAMMING ASSIGNMENT 4: COMPREHENSIVE VERIFICATION SUITE")
    print("Student: V. Karthik Harish (Reg No: 192511328) | Python:", sys.version.split()[0])
    print("=" * 86)

    results = []
    total_start = time.perf_counter()

    for t in TASKS:
        t_id = t["id"]
        t_name = t["name"]
        print(f"\n[RUNNING] {t_id}: {t_name}...")
        t0 = time.perf_counter()
        
        proc = subprocess.run(
            [sys.executable, t["script"]],
            cwd=t["cwd"],
            capture_output=True,
            text=True
        )
        elapsed = (time.perf_counter() - t0) * 1000.0

        if proc.returncode != 0:
            print(f"  [FAILED] Return code: {proc.returncode}")
            print(f"  Stderr: {proc.stderr[:300]}")
            results.append((t_id, t_name, "FAILED", elapsed, "Non-zero exit"))
            continue

        # Check required artifacts
        missing = []
        for art in t["artifacts"]:
            art_path = os.path.join(t["cwd"], art)
            if not os.path.exists(art_path):
                missing.append(art)

        if missing:
            print(f"  [WARN] Missing artifacts: {missing}")
            results.append((t_id, t_name, "ARTIFACT_MISSING", elapsed, f"Missing {len(missing)} files"))
        else:
            print(f"  [PASSED] Completed in {elapsed:.2f} ms with all artifacts verified.")
            results.append((t_id, t_name, "PASSED", elapsed, "All artifacts verified"))

    total_time = (time.perf_counter() - total_start) * 1000.0

    print("\n" + "=" * 86)
    print("ASSIGNMENT 4 VERIFICATION SUMMARY TABLE")
    print("=" * 86)
    header = f"{'Task ID':<10}{'Task Description':<48}{'Status':<12}{'Time (ms)':<12}"
    print(header)
    print("-" * 86)
    for t_id, t_name, status, el, notes in results:
        print(f"{t_id:<10}{t_name:<48}{status:<12}{el:<12.2f}")
    print("-" * 86)
    print(f"TOTAL EXECUTION TIME: {total_time:.2f} ms")
    all_passed = all(status == "PASSED" for _, _, status, _, _ in results)
    print("FINAL VERDICT:", "ALL 6 TASKS SUCCESSFULLY VERIFIED (100% PASS)" if all_passed else "SOME TASKS FAILED")
    print("=" * 86)
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(run_suite())
