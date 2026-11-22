"""
Organisation C: Main Driver
File: main.py
Course: CSA08 - Python Programming
Student: V. Karthik Harish (Reg No: 192511328)

Orchestrates reader, stats, and report modules.
"""

import os
import reader
import stats
import report

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_dir = os.path.join(os.path.dirname(current_dir), "sample_data")
    out_dir = os.path.join(current_dir, "outputs")
    files = [os.path.join(sample_dir, f"day{i}.txt") for i in range(1, 6)]

    # 1. Ingestion
    records, sequences = reader.read_attendance_files(files)
    
    # 2. Analytics
    stat_summary, defaulters = stats.compute_statistics(records, threshold_pct=75.0)
    consecutive = stats.find_consecutive_absentees(sequences, records, threshold_days=3)

    # 3. Reporting
    out_files = report.generate_all_reports(out_dir, stat_summary, defaulters, consecutive)

    print(f"[Org C] Processed {len(stat_summary)} students.")
    print(f"        Defaulters count: {len(defaulters)}")
    print(f"        3-Day Consecutive Absentees: {len(consecutive)}")
    for item in consecutive:
        print(f"          - {item['reg_no']} ({item['name']}): max streak {item['max_streak']} days")

if __name__ == "__main__":
    main()
