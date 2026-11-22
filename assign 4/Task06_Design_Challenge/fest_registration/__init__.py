"""
Package: fest_registration
Course: CSA08 - Python Programming
Student: V. Karthik Harish (Reg No: 192511328)

Robust modular file-processing package for cultural fest registration desk.
Designed for zero-crash fault tolerance, O(1) set deduplication, and automated reporting.
"""

from .validator import validate_email, validate_record, RegistrationValidationError
from .parser import parse_department_file
from .aggregator import RegistrationAggregator
from .reporter import write_all_fest_reports

__version__ = "1.0.0"
__author__ = "V. Karthik Harish (192511328)"

__all__ = [
    "validate_email",
    "validate_record",
    "RegistrationValidationError",
    "parse_department_file",
    "RegistrationAggregator",
    "write_all_fest_reports",
]
