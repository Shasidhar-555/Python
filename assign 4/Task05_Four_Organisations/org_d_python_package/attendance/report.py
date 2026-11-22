"""
Module: attendance.report
Course: CSA08 - Python Programming
Student: V. Karthik Harish (Reg No: 192511328)

Report formatting and file writing for the attendance package.
"""

import os

def write_summary_report(file_path, stats):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("ORG D (PYTHON PACKAGE) - ATTENDANCE SUMMARY REPORT\n")
        f.write("=" * 60 + "\n")
        f.write(f"{'Reg No':<12}{'Name':<15}{'Present':<10}{'Total':<10}{'Pct (%)':<10}\n")
        f.write("-" * 60 + "\n")
        for reg, s in sorted(stats.items()):
            f.write(f"{reg:<12}{s['name']:<15}{s['present']:<10}{s['total']:<10}{s['pct']:<10.2f}\n")


def write_defaulters_report(file_path, defaulters):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("ORG D (PYTHON PACKAGE) - ATTENDANCE DEFAULTERS (<75%)\n")
        f.write("=" * 60 + "\n")
        for reg, name, pct in sorted(defaulters):
            f.write(f"Register No: {reg} | Name: {name:<12} | Attendance: {pct:.2f}%\n")


def write_consecutive_absent_report(file_path, consecutive_absentees):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("ORG D (PYTHON PACKAGE) - CONSECUTIVE ABSENTEES (>= 3 DAYS)\n")
        f.write("=" * 60 + "\n")
        for item in consecutive_absentees:
            streak_desc = ", ".join([f"Days {s}-{e} ({k} days)" for s, e, k in item["streaks"]])
            f.write(f"Register No: {item['reg_no']} | Name: {item['name']:<12} | Max Streak: {item['max_streak']} days | Details: {streak_desc}\n")


def generate_all_reports(output_dir, stats, defaulters, consecutive_absentees):
    os.makedirs(output_dir, exist_ok=True)
    summary_path = os.path.join(output_dir, "summary_report.txt")
    defaulters_path = os.path.join(output_dir, "defaulters_report.txt")
    consecutive_path = os.path.join(output_dir, "consecutive_absent_report.txt")

    write_summary_report(summary_path, stats)
    write_defaulters_report(defaulters_path, defaulters)
    write_consecutive_absent_report(consecutive_path, consecutive_absentees)
    return summary_path, defaulters_path, consecutive_path

if __name__ == "__main__":
    print("attendance.report: self-test executed.")
