"""
Module: fest_registration.validator
Course: CSA08 - Python Programming
Student: V. Karthik Harish (Reg No: 192511328)

Validation logic for student registration fields using string methods only (no regex).
"""

class RegistrationValidationError(Exception):
    """Raised when a registration record fails field formatting or semantic constraints."""
    pass


def validate_email(email_str):
    """
    Validates an email address using string methods ONLY (no regex).
    
    Rules:
    1. Must be a non-empty string without whitespace.
    2. Must contain exactly one '@' character.
    3. Local part (before '@') must be non-empty and must not start or end with a dot.
    4. Domain part (after '@') must contain at least one dot ('.').
    5. Domain labels between dots must be non-empty.
    6. Top-level domain (TLD) must have at least 2 alphabetic characters.
    """
    if not isinstance(email_str, str):
        return False, "Email must be a string"

    email = email_str.strip()
    if not email:
        return False, "Email address is empty"

    if " " in email:
        return False, "Email contains whitespace"

    if email.count("@") != 1:
        return False, f"Expected exactly one '@', found {email.count('@')}"

    local_part, domain_part = email.split("@")

    if not local_part:
        return False, "Local part before '@' cannot be empty"

    if local_part.startswith(".") or local_part.endswith("."):
        return False, "Local part cannot start or end with a dot"

    if ".." in local_part:
        return False, "Local part cannot contain consecutive dots"

    if not domain_part:
        return False, "Domain part after '@' cannot be empty"

    if "." not in domain_part:
        return False, "Domain part must contain at least one dot"

    domain_tokens = domain_part.split(".")
    for token in domain_tokens:
        if not token:
            return False, "Domain labels cannot be empty (no consecutive dots or leading/trailing dots)"

    tld = domain_tokens[-1]
    if len(tld) < 2 or not tld.isalpha():
        return False, f"Top-level domain '{tld}' must have at least 2 alphabetic characters"

    return True, "Valid"


def validate_record(raw_line):
    """
    Validates a raw CSV line for cultural fest registration.
    Expected format: register_number,name,department,email,events_chosen
    Events are separated by semicolons (e.g., Dance;Music;Quiz).
    
    Returns:
        tuple: (reg_no, name, dept, email, events_list)
    Raises:
        RegistrationValidationError: If the line is malformed or invalid.
    """
    if not raw_line or not raw_line.strip():
        raise RegistrationValidationError("Empty line")

    parts = [p.strip() for p in raw_line.split(",")]
    if len(parts) != 5:
        raise RegistrationValidationError(f"Expected 5 fields, found {len(parts)} (raw: '{raw_line.strip()}')")

    reg_no, name, dept, email, events_raw = parts

    if not reg_no:
        raise RegistrationValidationError("Register number cannot be empty")
    if not name:
        raise RegistrationValidationError("Student name cannot be empty")
    if not dept:
        raise RegistrationValidationError("Department cannot be empty")

    is_valid_email, reason = validate_email(email)
    if not is_valid_email:
        raise RegistrationValidationError(f"Invalid email '{email}': {reason}")

    events = [e.strip() for e in events_raw.split(";") if e.strip()]
    if not events:
        raise RegistrationValidationError(f"No valid events specified in '{events_raw}'")

    return reg_no, name, dept, email, events


if __name__ == "__main__":
    # Self test
    valid, _ = validate_email("user@simats.edu")
    assert valid is True
    invalid, reason = validate_email("user@@simats.edu")
    assert invalid is False
    print("validator.py: self-test passed successfully.")
