"""
Master Test Runner: Executes and Verifies All Assignment 5 Tasks
File: run_all_tasks.py
Course: CSA08 - Python Programming (Assignment 5)
Student: V. Karthik Harish (Reg No: 192511328)

Sequentially executes Task A through Task B4, verifies execution status codes,
asserts that expected output artifacts, databases, and screenshots exist,
and outputs a unified verification summary table.
"""

import os
import sys
import subprocess
import time

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

TASKS = [
    {
        "id": "Task A",
        "name": "Data Acquisition, Cleaning & AI Design Specs",
        "script": os.path.join(REPO_ROOT, "TaskA_Design", "task_a_design_spec.py"),
        "cwd": os.path.join(REPO_ROOT, "TaskA_Design"),
        "artifacts": ["output.txt", "output_screenshot.png"]
    },
    {
        "id": "Task B1",
        "name": "Cleaning Pipeline, Complete-the-Code & SQLite Queries",
        "script": os.path.join(REPO_ROOT, "TaskB1_Cleaning_Pipeline", "task_b1_pipeline.py"),
        "cwd": os.path.join(REPO_ROOT, "TaskB1_Cleaning_Pipeline"),
        "artifacts": ["output.txt", "output_screenshot.png", "cleaned_readings.csv", "air_quality.db", "b1_charts.png"]
    },
    {
        "id": "Task B2",
        "name": "Adversarial Stress Testing & SQL Injection Defense",
        "script": os.path.join(REPO_ROOT, "TaskB2_Adversarial_Data", "task_b2_adversarial.py"),
        "cwd": os.path.join(REPO_ROOT, "TaskB2_Adversarial_Data"),
        "artifacts": ["output.txt", "output_screenshot.png"]
    },
    {
        "id": "Task B3",
        "name": "Loops vs Pandas vs SQL Scaling & cProfile Bottlenecks",
        "script": os.path.join(REPO_ROOT, "TaskB3_Loops_Libraries_SQL", "task_b3_benchmark.py"),
        "cwd": os.path.join(REPO_ROOT, "TaskB3_Loops_Libraries_SQL"),
        "artifacts": ["output.txt", "output_screenshot.png", "cprofile_report.txt"]
    },
    {
        "id": "Task B4",
        "name": "Production Scaling Decision & 50-Complaint AI Evaluation",
        "script": os.path.join(REPO_ROOT, "TaskB4_Engineering_Decision", "task_b4_production.py"),
        "cwd": os.path.join(REPO_ROOT, "TaskB4_Engineering_Decision"),
        "artifacts": ["output.txt", "output_screenshot.png", "citizen_complaints_50.txt"]
    }
]


def run_suite():
    print("=" * 86)
    print("CSA08 - PYTHON PROGRAMMING ASSIGNMENT 5: COMPREHENSIVE VERIFICATION SUITE")
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
    print("ASSIGNMENT 5 VERIFICATION SUMMARY TABLE")
    print("=" * 86)
    header = f"{'Task ID':<10}{'Task Description':<48}{'Status':<12}{'Time (ms)':<12}"
    print(header)
    print("-" * 86)
    for t_id, t_name, status, el, notes in results:
        print(f"{t_id:<10}{t_name:<48}{status:<12}{el:<12.2f}")
    print("-" * 86)
    print(f"TOTAL EXECUTION TIME: {total_time:.2f} ms")
    all_passed = all(status == "PASSED" for _, _, status, _, _ in results)
    print("FINAL VERDICT:", "ALL TASKS SUCCESSFULLY VERIFIED (100% PASS)" if all_passed else "SOME TASKS FAILED")
    print("=" * 86)
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(run_suite())
