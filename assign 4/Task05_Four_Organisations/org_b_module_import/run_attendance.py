"""
Organisation B: Driver Script
File: run_attendance.py
Course: CSA08 - Python Programming
Student: V. Karthik Harish (Reg No: 192511328)

Imports the attendance_processor module and coordinates execution.
"""

import os
import attendance_processor

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_dir = os.path.join(os.path.dirname(current_dir), "sample_data")
    out_dir = os.path.join(current_dir, "outputs")
    files = [os.path.join(sample_dir, f"day{i}.txt") for i in range(1, 6)]

    # 1. Read
    records, sequences = attendance_processor.read_attendance_files(files)
    
    # 2. Stats
    stats, defaulters = attendance_processor.compute_statistics(records)
    
    # 3. Consecutive absentees (Task 5.2 requirement)
    consecutive = attendance_processor.find_consecutive_absentees(sequences, records, threshold=3)
    
    # 4. Reports
    reports = attendance_processor.write_reports(out_dir, stats, defaulters, consecutive)

    print(f"[Org B] Processed {len(stats)} students.")
    print(f"        Defaulters count: {len(defaulters)}")
    print(f"        3-Day Consecutive Absentees: {len(consecutive)}")
    for item in consecutive:
        print(f"          - {item['reg_no']} ({item['name']}): max streak {item['max_streak']} days")

if __name__ == "__main__":
    main()
