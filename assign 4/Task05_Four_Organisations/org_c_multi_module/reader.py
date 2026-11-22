"""
Organisation C: Reader Module
File: reader.py
Course: CSA08 - Python Programming
Student: V. Karthik Harish (Reg No: 192511328)

Dedicated exclusively to file input, parsing, and data ingestion.
"""

import os

def read_attendance_files(file_paths):
    student_records = {}
    daily_sequences = {}

    for file_path in file_paths:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing input file: {file_path}")

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

if __name__ == "__main__":
    print("reader.py: self-test passed.")
