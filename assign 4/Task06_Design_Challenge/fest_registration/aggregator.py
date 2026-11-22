"""
Module: fest_registration.aggregator
Course: CSA08 - Python Programming
Student: V. Karthik Harish (Reg No: 192511328)

Registration aggregation engine utilizing O(1) set-based deduplication
and multi-key indexing across events and departments.
"""

from collections import defaultdict

class RegistrationAggregator:
    def __init__(self):
        # O(1) membership lookup set for duplicate registration filtering
        self.seen_reg_nos = set()
        
        # Master list of unique student records
        self.master_records = []
        
        # Event rosters: event_name -> list of student dicts
        self.event_rosters = defaultdict(list)
        
        # Department counts: dept_name -> int count of unique participants
        self.dept_counts = defaultdict(int)
        
        # Audit list of all rejected records (duplicates, invalid lines, errors)
        self.rejected_records = []

    def ingest_record(self, record):
        """
        Ingests a validated candidate record.
        
        Args:
            record (dict): Validated record dictionary.
            
        Returns:
            bool: True if accepted, False if rejected as duplicate.
        """
        reg_no = record["reg_no"]
        
        # O(1) Average Time Complexity Set Lookup
        if reg_no in self.seen_reg_nos:
            self.rejected_records.append({
                "source_file": record.get("source_file", "unknown"),
                "line_no": record.get("line_no", 0),
                "error_type": "DuplicateRegistration",
                "reason": f"Register number '{reg_no}' already registered in the fest",
                "raw_line": f"{reg_no},{record['name']},{record['dept']},{record['email']}"
            })
            return False

        # Add to seen set
        self.seen_reg_nos.add(reg_no)
        self.master_records.append(record)
        self.dept_counts[record["dept"]] += 1

        # Populate event rosters
        for event in record["events"]:
            self.event_rosters[event].append({
                "reg_no": reg_no,
                "name": record["name"],
                "dept": record["dept"],
                "email": record["email"]
            })

        return True

    def ingest_file_stream(self, record_generator):
        """Processes all records yielded by the parser generator."""
        for rec in record_generator:
            self.ingest_record(rec)

    def get_summary_statistics(self):
        """Computes executive fest summary metrics."""
        total_unique_students = len(self.master_records)
        total_event_participations = sum(len(students) for students in self.event_rosters.values())
        total_rejected = len(self.rejected_records)

        return {
            "total_unique_students": total_unique_students,
            "total_event_participations": total_event_participations,
            "total_events": len(self.event_rosters),
            "total_rejected": total_rejected,
            "dept_breakdown": dict(sorted(self.dept_counts.items())),
            "event_breakdown": {ev: len(students) for ev, students in sorted(self.event_rosters.items())}
        }
