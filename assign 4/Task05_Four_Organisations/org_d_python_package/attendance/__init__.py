"""
Package: attendance
Course: CSA08 - Python Programming
Student: V. Karthik Harish (Reg No: 192511328)

A robust modular Python package for attendance ingestion, analytics,
consecutive absence detection, and multi-format report generation.
"""

from .reader import read_attendance_files
from .stats import percentage, compute_statistics, find_consecutive_absentees
from .report import (
    write_summary_report,
    write_defaulters_report,
    write_consecutive_absent_report,
    generate_all_reports,
)

__version__ = "1.0.0"
__author__ = "V. Karthik Harish (192511328)"

__all__ = [
    "read_attendance_files",
    "percentage",
    "compute_statistics",
    "find_consecutive_absentees",
    "write_summary_report",
    "write_defaulters_report",
    "write_consecutive_absent_report",
    "generate_all_reports",
]
