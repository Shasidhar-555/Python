"""
Module: attendance.stats
Course: CSA08 - Python Programming
Student: V. Karthik Harish (Reg No: 192511328)

Provides attendance percentage calculations, defaulter identification, and consecutive absence analysis.
"""

def percentage(present, total):
    """
    Computes attendance percentage rounded to two decimal places.
    Formula: (present / total) * 100
    """
    if total <= 0:
        return 0.0
    return round((present / total) * 100.0, 2)


def compute_statistics(student_records, threshold_pct=75.0):
    stats = {}
    defaulters = []
    for reg_no, rec in student_records.items():
        pres = rec["present"]
        tot = rec["total"]
        pct = percentage(pres, tot)
        stats[reg_no] = {
            "name": rec["name"],
            "present": pres,
            "total": tot,
            "pct": pct
        }
        if pct < threshold_pct:
            defaulters.append((reg_no, rec["name"], pct))
    return stats, defaulters


def find_consecutive_absentees(daily_sequences, student_records, threshold_days=3):
    """
    [TASK 5.2 REQUIREMENT]: Identifies students absent for at least `threshold_days` consecutive days.
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
                if current_streak >= threshold_days:
                    streaks.append((start_day, day_idx - 1, current_streak))
                current_streak = 0
        if current_streak >= threshold_days:
            streaks.append((start_day, len(seq), current_streak))

        if max_streak >= threshold_days:
            consecutive_absentees.append({
                "reg_no": reg_no,
                "name": student_records[reg_no]["name"],
                "max_streak": max_streak,
                "streaks": streaks
            })
    return consecutive_absentees

if __name__ == "__main__":
    print("attendance.stats: self-test executed.")
