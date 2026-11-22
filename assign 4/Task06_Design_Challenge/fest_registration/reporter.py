"""
Module: fest_registration.reporter
Course: CSA08 - Python Programming
Student: V. Karthik Harish (Reg No: 192511328)

Serializes registration data into master CSV rosters, event-wise roster files,
executive summary reports, and comprehensive audit logs.
"""

import os
from datetime import datetime

def write_master_roster(output_path, master_records):
    """Writes master CSV of all unique registered students."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Register_Number,Student_Name,Department,Email,Events_Chosen\n")
        for rec in master_records:
            events_str = ";".join(rec["events"])
            f.write(f"{rec['reg_no']},{rec['name']},{rec['dept']},{rec['email']},{events_str}\n")


def write_event_rosters(output_dir, event_rosters):
    """Writes individual text files for each distinct event."""
    os.makedirs(output_dir, exist_ok=True)
    generated_files = []
    
    for event_name, students in sorted(event_rosters.items()):
        safe_filename = f"{event_name.replace(' ', '_')}.txt"
        file_path = os.path.join(output_dir, safe_filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write(f"CULTURAL FEST EVENT ROSTER: {event_name.upper()}\n")
            f.write(f"Total Enrolled Participants: {len(students)}\n")
            f.write("=" * 70 + "\n")
            f.write(f"{'Reg No':<14}{'Student Name':<20}{'Dept':<10}{'Email':<26}\n")
            f.write("-" * 70 + "\n")
            for st in sorted(students, key=lambda s: s["reg_no"]):
                f.write(f"{st['reg_no']:<14}{st['name']:<20}{st['dept']:<10}{st['email']:<26}\n")
        
        generated_files.append(file_path)
    return generated_files


def write_summary_report(output_path, summary_stats):
    """Writes an executive fest registration breakdown report."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("SIMATS CULTURAL FEST REGISTRATION DESK - EXECUTIVE SUMMARY\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")

        f.write("1. REGISTRATION OVERVIEW:\n")
        f.write(f"   - Total Unique Students Registered: {summary_stats['total_unique_students']}\n")
        f.write(f"   - Total Event Enrollments:          {summary_stats['total_event_participations']}\n")
        f.write(f"   - Total Events Scheduled:           {summary_stats['total_events']}\n")
        f.write(f"   - Total Rejected Records/Lines:     {summary_stats['total_rejected']}\n\n")

        f.write("2. DEPARTMENT PARTICIPATION BREAKDOWN:\n")
        f.write(f"   {'Department':<20}{'Unique Students':<16}\n")
        f.write(f"   {'-'*36}\n")
        for dept, count in summary_stats["dept_breakdown"].items():
            f.write(f"   {dept:<20}{count:<16}\n")
        f.write("\n")

        f.write("3. EVENT ENROLLMENT BREAKDOWN:\n")
        f.write(f"   {'Event Name':<25}{'Participants':<16}\n")
        f.write(f"   {'-'*41}\n")
        for ev, count in summary_stats["event_breakdown"].items():
            f.write(f"   {ev:<25}{count:<16}\n")
        f.write("\n" + "=" * 70 + "\n")


def write_error_log(output_path, rejected_records):
    """Writes detailed error audit log with reasons and raw line content."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("FEST REGISTRATION AUDIT & REJECTION LOG\n")
        f.write("=" * 80 + "\n")
        f.write(f"{'Source File':<16}{'Line':<6}{'Error Type':<24}{'Reason'}\n")
        f.write("-" * 80 + "\n")
        for r in rejected_records:
            f.write(f"{r['source_file']:<16}{r['line_no']:<6}{r['error_type']:<24}{r['reason']}\n")
            if r.get("raw_line"):
                f.write(f"   [Raw Content]: {r['raw_line']}\n")


def write_all_fest_reports(output_base_dir, aggregator):
    """Master reporting orchestrator."""
    os.makedirs(output_base_dir, exist_ok=True)
    master_csv = os.path.join(output_base_dir, "master_registered_students.csv")
    summary_txt = os.path.join(output_base_dir, "fest_summary_report.txt")
    error_log = os.path.join(output_base_dir, "fest_processing_errors.log")
    event_dir = os.path.join(output_base_dir, "event_rosters")

    write_master_roster(master_csv, aggregator.master_records)
    event_files = write_event_rosters(event_dir, aggregator.event_rosters)
    stats = aggregator.get_summary_statistics()
    write_summary_report(summary_txt, stats)
    write_error_log(error_log, aggregator.rejected_records)

    return {
        "master_csv": master_csv,
        "summary_txt": summary_txt,
        "error_log": error_log,
        "event_dir": event_dir,
        "event_files": event_files
    }
