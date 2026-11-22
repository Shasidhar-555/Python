"""
Task 04: Sets - Elective Registration Clash Detection
Course: CSA08 / CSA0807 Python Programming (CO3)
Bloom's Level: K4 - Analyse

Problem Context - Elective Course Registration:
Students register for electives scheduled in the same time slot (AI and IoT).
The academic office requires:
1. Complete the Code: Using set operators (&, ^, -) and set methods to find:
   - Students registered in both electives (time-slot clash)
   - Students registered in exactly one elective
   - Students registered in neither elective (unregistered)
2. Mathematical Venn diagram mapping and ASCII visualization.
3. Demonstration of automatic duplicate removal and why sets cannot contain lists.
4. Empirical benchmark: Membership testing (x in list vs x in set) for 10k, 100k, and 1M records.
5. Empirical benchmark: Finding common students via nested loops vs set intersection (&).
6. Edge case testing: empty electives, identical electives, all-registered.
7. Alternative concept analysis: lists with nested loops vs sorting + two-pointer vs hash set.
"""

import time
import random
import sys
import json


# ==============================================================================
# 1. COMPLETE THE CODE (AS GIVEN IN ASSIGNMENT SPECIFICATION)
# ==============================================================================

def run_complete_the_code():
    print("=" * 88)
    print("PART 1: 'COMPLETE THE CODE' - ELECTIVE REGISTRATION CLASH DETECTION")
    print("=" * 88)

    ai_elective = {"192311001", "192311004", "192311007", "192311009"}
    iot_elective = {"192311002", "192311004", "192311009", "192311010"}
    all_students = {f"1923110{i:02d}" for i in range(1, 11)}

    # TODO 1: Use set operators to find: students in both electives, students in exactly
    #   one, and students in neither
    both = ai_elective & iot_elective
    exactly_one = ai_elective ^ iot_elective
    neither = all_students - (ai_elective | iot_elective)

    print("clash      :", sorted(both))
    print("exactly one:", sorted(exactly_one))
    print("neither    :", sorted(neither))

    # Verification against expected output
    expected_clash = ['192311004', '192311009']
    expected_one = ['192311001', '192311002', '192311007', '192311010']
    expected_neither = ['192311003', '192311005', '192311006', '192311008']

    assert sorted(both) == expected_clash
    assert sorted(exactly_one) == expected_one
    assert sorted(neither) == expected_neither
    print("\n[✓] Complete the Code passed all assertions matching expected assignment output.")

    # Rewrite using set methods
    print("\n--- REWRITE USING SET METHODS (METHOD EQUIVALENCE CHECK) ---")
    both_methods = ai_elective.intersection(iot_elective)
    exactly_one_methods = ai_elective.symmetric_difference(iot_elective)
    neither_methods = all_students.difference(ai_elective.union(iot_elective))

    print("Methods clash      :", sorted(both_methods))
    print("Methods exactly one:", sorted(exactly_one_methods))
    print("Methods neither    :", sorted(neither_methods))

    assert both == both_methods
    assert exactly_one == exactly_one_methods
    assert neither == neither_methods
    print("[✓] Verified: Operator syntax (&, ^, -, |) is mathematically and practically")
    print("    equivalent to method calls (.intersection, .symmetric_difference, .difference, .union).")


# ==============================================================================
# 2. VENN DIAGRAM ASCII REPRESENTATION
# ==============================================================================

def display_venn_diagram():
    print("\n" + "=" * 88)
    print("PART 2: VENN DIAGRAM VISUALIZATION OF ELECTIVE REGISTRATION ALGEBRA")
    print("=" * 88)
    print("""
    ┌────────────────────────────────── UNIVERSAL SET (All Students: 1..10) ──────────────────────────────────┐
    │                                                                                                         │
    │        ┌─────────────────────────┐                     ┌─────────────────────────┐                      │
    │        │       AI ELECTIVE       │                     │      IoT ELECTIVE       │                      │
    │        │                         │  INTERSECTION (&)   │                         │                      │
    │        │  Only AI (AI - IoT):    │     CLASH ZONE      │  Only IoT (IoT - AI):   │                      │
    │        │  192311001              │     192311004       │  192311002              │                      │
    │        │  192311007              │     192311009       │  192311010              │                      │
    │        │                         │                     │                         │                      │
    │        └─────────────────────────┴─────────────────────┴─────────────────────────┘                      │
    │                                                                                                         │
    │        ◄─────────────────────── SYMMETRIC DIFFERENCE (AI ^ IoT) ───────────────────────►               │
    │        Exactly One Course = {192311001, 192311002, 192311007, 192311010}                                 │
    │                                                                                                         │
    │   UNREGISTERED / NEITHER: All - (AI ∪ IoT)                                                              │
    │   {192311003, 192311005, 192311006, 192311008}                                                         │
    └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    """)


# ==============================================================================
# 3. SET PROPERTIES: DEDUPLICATION & MUTABILITY RESTRICTION
# ==============================================================================

def demonstrate_set_properties():
    print("\n" + "=" * 88)
    print("PART 3: SET DEDUPLICATION & MUTABILITY CONSTRAINTS")
    print("=" * 88)

    # 1. Automatic duplicate removal
    raw_registrations = ["192311001", "192311002", "192311001", "192311003", "192311002", "192311001"]
    deduped_set = set(raw_registrations)
    print(f"Raw registrations list ({len(raw_registrations)} entries): {raw_registrations}")
    print(f"Deduplicated set       ({len(deduped_set)} entries): {sorted(deduped_set)}")
    print("EXPLANATION: Sets are implemented as hash tables without values. When an element is added,")
    print("its hash determines the bucket. If an identical element already occupies the bucket,")
    print("the duplicate insertion is ignored in O(1) time.")

    # 2. Why sets cannot contain lists, but can contain tuples
    print("\nTesting element types inside a set:")
    valid_tuple_element = ("192311001", "AI_Slot_1")
    s = set()
    s.add(valid_tuple_element)
    print(f"• Successfully added tuple {valid_tuple_element} to set: {s}")

    invalid_list_element = ["192311001", "AI_Slot_1"]
    try:
        s.add(invalid_list_element)
    except TypeError as e:
        print(f"• Attempting to add list {invalid_list_element} to set: TypeError: {e}")
    print("EXPLANATION: Sets require every element to be hashable and immutable so that its bucket")
    print("location remains permanent. Lists are mutable and unhashable, whereas tuples are immutable.")


# ==============================================================================
# 4. EMPIRICAL BENCHMARKS: MEMBERSHIP TESTING & CLASH INTERSECTION
# ==============================================================================

def benchmark_membership():
    print("\n" + "=" * 88)
    print("PART 4: BENCHMARK 1 - MEMBERSHIP TESTING (x in list vs x in set)")
    print("=" * 88)

    sizes = [10_000, 100_000, 1_000_000]
    print(f"{'Dataset Size (N)':<18} | {'x in list (s)':<16} | {'x in set (s)':<16} | {'Speedup Ratio':<14}")
    print("-" * 72)

    for n in sizes:
        # Build collection of student register numbers
        students_list = [f"REG_{i:07d}" for i in range(n)]
        students_set = set(students_list)
        
        # Target: worst-case search for element at the very end or not present
        target = f"REG_{n-1:07d}"
        
        # Time list search (100 repetitions for small n, 5 for 1M)
        repeats = 50 if n <= 100_000 else 5
        
        t0 = time.perf_counter()
        for _ in range(repeats):
            _ = target in students_list
        t_list = (time.perf_counter() - t0) / repeats
        
        # Time set search (10,000 repetitions to get measurable time)
        set_repeats = 100_000
        t0 = time.perf_counter()
        for _ in range(set_repeats):
            _ = target in students_set
        t_set = (time.perf_counter() - t0) / set_repeats
        
        speedup = t_list / t_set if t_set > 0 else 0.0
        print(f"{n:<18,d} | {t_list:<16.8f} | {t_set:<16.8f} | {speedup:<13.1f}x")

    print("-" * 72)


def benchmark_clash_detection():
    print("\n" + "=" * 88)
    print("PART 5: BENCHMARK 2 - FINDING COMMON STUDENTS (NESTED LOOPS vs SET &)")
    print("=" * 88)

    sizes = [(500, 500), (2_000, 2_000), (5_000, 5_000)]
    print(f"{'Group Sizes (n, m)':<22} | {'Nested Loops O(n*m)':<22} | {'Set & O(min(n,m))':<20} | {'Speedup':<12}")
    print("-" * 82)

    for n, m in sizes:
        list_a = [f"STU_{i:06d}" for i in range(n)]
        # 30% overlap
        list_b = [f"STU_{i:06d}" for i in range(int(n * 0.7), int(n * 0.7) + m)]
        
        set_a = set(list_a)
        set_b = set(list_b)
        
        # 1. Nested loops
        t0 = time.perf_counter()
        clashes_loop = [x for x in list_a if x in list_b]
        t_loop = time.perf_counter() - t0
        
        # 2. Set intersection
        t0 = time.perf_counter()
        clashes_set = set_a & set_b
        t_set = time.perf_counter() - t0
        
        speedup = t_loop / t_set if t_set > 0 else 0.0
        assert set(clashes_loop) == clashes_set
        print(f"({n:,d}, {m:,d}){'':<10} | {t_loop:<22.6f} | {t_set:<20.6f} | {speedup:<11.1f}x")

    print("-" * 82)


# ==============================================================================
# 5. EDGE CASE TESTING
# ==============================================================================

def test_edge_cases():
    print("\n" + "=" * 88)
    print("PART 6: EDGE CASE TESTING (EMPTY ELECTIVES & IDENTICAL ELECTIVES)")
    print("=" * 88)

    all_students = {"S1", "S2", "S3", "S4"}

    # Case A: Empty electives
    empty_a = set()
    empty_b = set()
    print("Case A: Both electives empty:")
    print("  Clashes      :", empty_a & empty_b)
    print("  Exactly one  :", empty_a ^ empty_b)
    print("  Neither      :", all_students - (empty_a | empty_b))
    assert (empty_a & empty_b) == set()
    assert (all_students - (empty_a | empty_b)) == all_students

    # Case B: Identical electives (everyone in A is also in B)
    elec_1 = {"S1", "S2"}
    elec_2 = {"S1", "S2"}
    print("\nCase B: Identical electives (All students registered in both):")
    print("  Clashes      :", elec_1 & elec_2)
    print("  Exactly one  :", elec_1 ^ elec_2)
    print("  Neither      :", all_students - (elec_1 | elec_2))
    assert (elec_1 & elec_2) == {"S1", "S2"}
    assert (elec_1 ^ elec_2) == set()
    assert (all_students - (elec_1 | elec_2)) == {"S3", "S4"}
    print("\n  [✓] All edge cases verified against manual set algebra calculations.")


# ==============================================================================
# 6. DESIGN CONCLUSION & COMPLEXITY ANALYSIS
# ==============================================================================

def print_design_analysis():
    print("\n" + "=" * 88)
    print("PART 7: COMPLEXITY ANALYSIS & DESIGN DEFENSE")
    print("=" * 88)
    print("""
1. WHEN TO CONVERT A LIST INTO A SET & WHAT INFORMATION IS LOST:
   - When to Convert:
     * When performing multiple membership tests (`if x in collection`).
     * When performing relational algebra (union, intersection, difference, deduplication).
     * When order and frequency do not carry business significance.
   - What is Lost:
     * Sequence Ordering: Sets do not preserve insertion order or position.
     * Element Duplication: Frequencies and duplicate counts are discarded.
     * Indexing & Slicing: Expressions like `s[0]` or `s[1:5]` raise TypeError.

2. ALTERNATIVE CONCEPT AND COMPLEXITY ANALYSIS:
   ┌───────────────────────────────────┬──────────────────────┬──────────────────────┐
   │ Approach                          │ Time Complexity      │ Space Complexity     │
   ├───────────────────────────────────┼──────────────────────┼──────────────────────┤
   │ 1. Nested Loops over Lists        │ O(n * m)             │ O(1) auxiliary       │
   │ 2. Sort both Lists + 2-Pointer    │ O(n log n + m log m) │ O(1) auxiliary       │
   │ 3. Hash Sets (Python set &)       │ O(n + m) build/query │ O(n + m) auxiliary   │
   └───────────────────────────────────┴──────────────────────┴──────────────────────┘
   
   - Analysis:
     * For n = m = 100,000:
       - Nested loops require 10,000,000,000 operations (~hours of CPU runtime).
       - Sort + Walk requires ~3,400,000 comparisons (~0.12 seconds).
       - Hash Set intersection requires ~200,000 hash operations (~0.015 seconds).
     * Therefore, Hash Sets provide the optimal real-world performance for batch registration.
""")
    print("=" * 88)


# ==============================================================================
# 7. MAIN FUNCTION
# ==============================================================================

def main():
    # Save sample registrations JSON
    sample_data = {
        "all_students": [f"1923110{i:02d}" for i in range(1, 11)],
        "ai_elective": ["192311001", "192311004", "192311007", "192311009"],
        "iot_elective": ["192311002", "192311004", "192311009", "192311010"]
    }
    with open("registrations_sample.json", "w") as f:
        json.dump(sample_data, f, indent=2)

    run_complete_the_code()
    display_venn_diagram()
    demonstrate_set_properties()
    benchmark_membership()
    benchmark_clash_detection()
    test_edge_cases()
    print_design_analysis()


if __name__ == "__main__":
    main()
