"""
Organisation D: Top-Level Main Driver
File: main.py
Course: CSA08 - Python Programming
Student: V. Karthik Harish (Reg No: 192511328)

Demonstrates package import syntax and orchestrates the full pipeline.
"""

import os
import sys

# Ensure current directory is on sys.path for direct script execution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Demonstrating the three import syntax forms required by Task 5.3:
# Syntax 1: import attendance.stats
import attendance.stats

# Syntax 2: from attendance import stats
from attendance import stats

# Syntax 3: from attendance.stats import percentage
from attendance.stats import percentage

# Top-level package namespace import
import attendance

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_dir = os.path.join(os.path.dirname(current_dir), "sample_data")
    out_dir = os.path.join(current_dir, "outputs")
    files = [os.path.join(sample_dir, f"day{i}.txt") for i in range(1, 6)]

    # 1. Ingestion via top-level package namespace
    records, sequences = attendance.read_attendance_files(files)

    # 2. Statistics computation via sub-module
    stat_summary, defaulters = attendance.stats.compute_statistics(records, threshold_pct=75.0)

    # 3. Consecutive absent calculation (Task 5.2 requirement)
    consecutive = stats.find_consecutive_absentees(sequences, records, threshold_days=3)

    # 4. Report generation
    reports = attendance.generate_all_reports(out_dir, stat_summary, defaulters, consecutive)

    print(f"[Org D] Processed {len(stat_summary)} students using package 'attendance'.")
    print(f"        Defaulters count: {len(defaulters)}")
    print(f"        3-Day Consecutive Absentees: {len(consecutive)}")
    for item in consecutive:
        print(f"          - {item['reg_no']} ({item['name']}): max streak {item['max_streak']} days")
    
    # Verify the syntax forms produce identical results
    val1 = attendance.stats.percentage(3, 4)
    val2 = stats.percentage(3, 4)
    val3 = percentage(3, 4)
    assert val1 == val2 == val3 == 75.0
    print(f"        Import syntax equivalence verified: {val1}% == {val2}% == {val3}%")

if __name__ == "__main__":
    main()
