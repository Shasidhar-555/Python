"""
Organisation B: Module File
File: attendance_processor.py
Course: CSA08 - Python Programming
Student: V. Karthik Harish (Reg No: 192511328)

Contains library functions for attendance data reading, statistical calculation,
consecutive absence detection, and report generation. Designed to be imported.
"""

import os

def read_attendance_files(file_paths):
    student_records = {}
    daily_sequences = {}

    for file_path in file_paths:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 3:
                    continue
                reg_no, name, status = parts[0], parts[1], parts[2].upper()
                if status not in ("P", "A"):
                    continue

                if reg_no not in student_records:
                    student_records[reg_no] = {"name": name, "present": 0, "total": 0}
                    daily_sequences[reg_no] = []

                student_records[reg_no]["total"] += 1
                if status == "P":
                    student_records[reg_no]["present"] += 1
                daily_sequences[reg_no].append(status)

    return student_records, daily_sequences


def compute_statistics(student_records):
    stats = {}
    defaulters = []
    for reg_no, rec in student_records.items():
        present = rec["present"]
        total = rec["total"]
        pct = (present / total * 100.0) if total > 0 else 0.0
        stats[reg_no] = {
            "name": rec["name"],
            "present": present,
            "total": total,
            "pct": round(pct, 2)
        }
        if pct < 75.0:
            defaulters.append((reg_no, rec["name"], round(pct, 2)))
    return stats, defaulters


def find_consecutive_absentees(daily_sequences, student_records, threshold=3):
    """
    [TASK 5.2 REQUIREMENT]: Identifies students absent for at least `threshold` consecutive days.
    """
    consecutive_absentees = []
    for reg_no, seq in daily_sequences.items():
        max_streak = 0
        current_streak = 0
        streaks = []
        start_day = 0
        for day_idx, status in enumerate(seq, 1):
            if status == "A":
                if current_streak == 0:
                    start_day = day_idx
                current_streak += 1
                if current_streak > max_streak:
                    max_streak = current_streak
            else:
                if current_streak >= threshold:
                    streaks.append((start_day, day_idx - 1, current_streak))
                current_streak = 0
        if current_streak >= threshold:
            streaks.append((start_day, len(seq), current_streak))

        if max_streak >= threshold:
            consecutive_absentees.append({
                "reg_no": reg_no,
                "name": student_records[reg_no]["name"],
                "max_streak": max_streak,
                "streaks": streaks
            })
    return consecutive_absentees


def write_reports(output_dir, stats, defaulters, consecutive_absentees):
    os.makedirs(output_dir, exist_ok=True)
    summary_path = os.path.join(output_dir, "summary_report.txt")
    defaulters_path = os.path.join(output_dir, "defaulters_report.txt")
    consecutive_path = os.path.join(output_dir, "consecutive_absent_report.txt")

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("ORG B (SINGLE MODULE) - ATTENDANCE SUMMARY REPORT\n")
        f.write("=" * 60 + "\n")
        f.write(f"{'Reg No':<12}{'Name':<15}{'Present':<10}{'Total':<10}{'Pct (%)':<10}\n")
        f.write("-" * 60 + "\n")
        for reg, s in sorted(stats.items()):
            f.write(f"{reg:<12}{s['name']:<15}{s['present']:<10}{s['total']:<10}{s['pct']:<10.2f}\n")

    with open(defaulters_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("ORG B (SINGLE MODULE) - ATTENDANCE DEFAULTERS (<75%)\n")
        f.write("=" * 60 + "\n")
        for reg, name, pct in sorted(defaulters):
            f.write(f"Register No: {reg} | Name: {name:<12} | Attendance: {pct:.2f}%\n")

    with open(consecutive_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("ORG B (SINGLE MODULE) - CONSECUTIVE ABSENTEES (>= 3 DAYS)\n")
        f.write("=" * 60 + "\n")
        for item in consecutive_absentees:
            streak_desc = ", ".join([f"Days {s}-{e} ({k} days)" for s, e, k in item["streaks"]])
            f.write(f"Register No: {item['reg_no']} | Name: {item['name']:<12} | Max Streak: {item['max_streak']} days | Details: {streak_desc}\n")

    return summary_path, defaulters_path, consecutive_path


if __name__ == "__main__":
    print("attendance_processor: module self-test running...")
