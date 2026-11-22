"""
Module: fest_registration.parser
Course: CSA08 - Python Programming
Student: V. Karthik Harish (Reg No: 192511328)

Line-by-line streaming file parser with zero-crash fault tolerance.
"""

import os
from .validator import validate_record, RegistrationValidationError

def parse_department_file(file_path, error_collector=None):
    """
    Parses a single department file line by line.
    
    Args:
        file_path (str): Path to the department text file.
        error_collector (list, optional): List to append error records.
        
    Yields:
        dict: Parsed valid record containing keys:
              'reg_no', 'name', 'dept', 'email', 'events', 'source_file', 'line_no'
    """
    filename = os.path.basename(file_path)

    if not os.path.exists(file_path):
        err = {
            "source_file": filename,
            "line_no": 0,
            "error_type": "FileNotFoundError",
            "reason": f"Department file missing from storage: '{file_path}'",
            "raw_line": ""
        }
        if error_collector is not None:
            error_collector.append(err)
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_no, raw_line in enumerate(f, 1):
                clean_line = raw_line.strip()
                if not clean_line:
                    continue  # Ignore blank lines harmlessly

                try:
                    reg_no, name, dept, email, events = validate_record(clean_line)
                    yield {
                        "reg_no": reg_no,
                        "name": name,
                        "dept": dept,
                        "email": email,
                        "events": events,
                        "source_file": filename,
                        "line_no": line_no
                    }
                except RegistrationValidationError as ve:
                    err = {
                        "source_file": filename,
                        "line_no": line_no,
                        "error_type": "ValidationError",
                        "reason": str(ve),
                        "raw_line": clean_line
                    }
                    if error_collector is not None:
                        error_collector.append(err)
                except Exception as ex:
                    err = {
                        "source_file": filename,
                        "line_no": line_no,
                        "error_type": type(ex).__name__,
                        "reason": str(ex),
                        "raw_line": clean_line
                    }
                    if error_collector is not None:
                        error_collector.append(err)

    except (PermissionError, UnicodeDecodeError, OSError) as e:
        err = {
            "source_file": filename,
            "line_no": 0,
            "error_type": type(e).__name__,
            "reason": f"File I/O failure: {str(e)}",
            "raw_line": ""
        }
        if error_collector is not None:
            error_collector.append(err)
