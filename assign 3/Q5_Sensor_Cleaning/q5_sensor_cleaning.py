"""
Task 05: List Comprehensions - Cleaning Sensor Readings
Course: CSA08 / CSA0807 Python Programming (CO3)
Bloom's Level: K3 - Apply

Problem Context - Cold-Storage Vaccine Temperature Monitor:
A cold storage facility logs minute-by-minute temperatures.
Rules:
- Valid temperatures: -50.0 °C <= temp <= 50.0 °C (values outside are sensor errors).
- Safe vaccine range: 2.0 °C <= temp <= 8.0 °C (WHO vaccine cold chain protocol).
- Alarms triggered when valid temperature is strictly outside [2.0, 8.0] °C.

Implementations Required:
1. Version 1: Standard 'for' loop with .append()
2. Version 2: List comprehension with conditional filtering and Fahrenheit conversion
3. Version 3: Functional map() and filter() with lambda expressions
4. Alarm minute extraction using enumerate()
5. Dictionary comprehension and Set comprehension demonstrations
6. Empirical timing and memory comparison (list comp vs map/filter vs generator)
   for 10,000, 100,000, and 1,000,000 readings.
7. Edge case testing (all-valid, all-invalid readings).
"""

import sys
import time
import random


# ==============================================================================
# 1. CORE IMPLEMENTATION VERSIONS
# ==============================================================================

def clean_and_convert_for_loop(readings: list[float]) -> tuple[list[float], list[float]]:
    """
    Version 1: Traditional for-loop with append.
    """
    valid_c = []
    valid_f = []
    for c in readings:
        if -50.0 <= c <= 50.0:
            valid_c.append(c)
            valid_f.append(round(c * 9.0 / 5.0 + 32.0, 2))
    return valid_c, valid_f


def clean_and_convert_comprehension(readings: list[float]) -> tuple[list[float], list[float]]:
    """
    Version 2: List comprehensions with condition.
    """
    valid_c = [c for c in readings if -50.0 <= c <= 50.0]
    valid_f = [round(c * 9.0 / 5.0 + 32.0, 2) for c in readings if -50.0 <= c <= 50.0]
    return valid_c, valid_f


def clean_and_convert_map_filter(readings: list[float]) -> tuple[list[float], list[float]]:
    """
    Version 3: Functional programming with map() and filter().
    """
    valid_c = list(filter(lambda c: -50.0 <= c <= 50.0, readings))
    valid_f = list(map(lambda c: round(c * 9.0 / 5.0 + 32.0, 2), filter(lambda c: -50.0 <= c <= 50.0, readings)))
    return valid_c, valid_f


def find_alarm_minutes(readings: list[float]) -> list[int]:
    """
    Extracts minute indices (0-based) where reading was valid but outside safe 2-8 °C range.
    Uses enumerate() within a list comprehension.
    """
    return [
        minute for minute, c in enumerate(readings)
        if -50.0 <= c <= 50.0 and not (2.0 <= c <= 8.0)
    ]


# ==============================================================================
# 2. DICTIONARY & SET COMPREHENSIONS
# ==============================================================================

def demonstrate_dict_and_set_comprehensions(readings: list[float]):
    print("=" * 88)
    print("PART 1: DICTIONARY AND SET COMPREHENSIONS FOR VACCINE MONITORING")
    print("=" * 88)

    sample = readings[:15]
    print(f"Sample raw readings (first 15 minutes): {sample}")

    # 1. Dictionary Comprehension: Minute Index -> Valid Celsius Reading
    minute_temp_dict = {
        minute: c for minute, c in enumerate(sample)
        if -50.0 <= c <= 50.0
    }
    print(f"\n1. Dictionary Comprehension (minute -> valid_temp):")
    print(f"   {minute_temp_dict}")

    # 2. Set Comprehension: Deduplicated set of rounded valid temperatures
    unique_temps_set = {
        round(c, 1) for c in sample
        if -50.0 <= c <= 50.0
    }
    print(f"\n2. Set Comprehension (unique rounded temperatures):")
    print(f"   {sorted(unique_temps_set)}")


# ==============================================================================
# 3. VERIFICATION & EDGE CASE TESTING
# ==============================================================================

def test_equivalence_and_edge_cases():
    print("\n" + "=" * 88)
    print("PART 2: EQUIVALENCE VERIFICATION & EDGE CASE TESTING")
    print("=" * 88)

    # Test A: Equivalence check on mixed realistic data
    test_data = [4.2, 5.1, 95.0, 1.8, -60.0, 7.9, 8.5, 3.0, 50.0, -50.0, 50.1]
    
    c1, f1 = clean_and_convert_for_loop(test_data)
    c2, f2 = clean_and_convert_comprehension(test_data)
    c3, f3 = clean_and_convert_map_filter(test_data)
    alarms = find_alarm_minutes(test_data)

    print(f"Raw Input : {test_data}")
    print(f"Valid C   : {c2}")
    print(f"Valid F   : {f2}")
    print(f"Alarms (min): {alarms} (temperatures: {[test_data[m] for m in alarms]})")

    assert c1 == c2 == c3, "Celsius lists do not match!"
    assert f1 == f2 == f3, "Fahrenheit lists do not match!"
    print("\n[✓] VERIFIED: for-loop, list comprehension, and map/filter produce identical results.")

    # Test B: All-Valid readings
    all_valid = [3.5, 4.0, 5.2, 6.8, 7.1]
    cv, _ = clean_and_convert_comprehension(all_valid)
    assert cv == all_valid
    print(f"[✓] All-Valid Test: Kept all {len(cv)} readings.")

    # Test C: All-Invalid readings (extreme sensor anomalies)
    all_invalid = [-999.0, 150.0, -55.2, 85.0]
    ci, fi = clean_and_convert_comprehension(all_invalid)
    assert ci == [] and fi == []
    print(f"[✓] All-Invalid Test: Correctly filtered all anomalies, returning empty lists.")


# ==============================================================================
# 4. EMPIRICAL BENCHMARK: TIMING & MEMORY
# ==============================================================================

def generate_sensor_readings(n: int, seed: int = 42) -> list[float]:
    random.seed(seed)
    readings = []
    for _ in range(n):
        roll = random.random()
        if roll < 0.90:
            # 90% normal operating range: 0.0 to 10.0 °C
            readings.append(round(random.uniform(0.0, 10.0), 2))
        elif roll < 0.95:
            # 5% valid sub-zero or room temp: -30 to 45 °C
            readings.append(round(random.uniform(-30.0, 45.0), 2))
        else:
            # 5% sensor error spikes: outside [-50, 50] °C
            readings.append(round(random.choice([-120.0, 85.0, 120.0, -80.0]), 2))
    return readings


def run_empirical_investigation():
    print("\n" + "=" * 88)
    print("PART 3: EMPIRICAL BENCHMARK - FOR LOOP vs LIST COMP vs MAP/FILTER")
    print("=" * 88)

    sizes = [10_000, 100_000, 1_000_000]
    print(f"{'Readings (N)':<14} | {'For-Loop (s)':<14} | {'List Comp (s)':<14} | {'Map/Filter (s)':<16} | {'Speedup Comp/Loop':<18}")
    print("-" * 88)

    for n in sizes:
        dataset = generate_sensor_readings(n)
        
        # 1. For loop timing
        t0 = time.perf_counter()
        _ = clean_and_convert_for_loop(dataset)
        t_loop = time.perf_counter() - t0
        
        # 2. List comprehension timing
        t0 = time.perf_counter()
        _ = clean_and_convert_comprehension(dataset)
        t_comp = time.perf_counter() - t0
        
        # 3. Map & Filter timing
        t0 = time.perf_counter()
        _ = clean_and_convert_map_filter(dataset)
        t_map = time.perf_counter() - t0
        
        speedup = t_loop / t_comp if t_comp > 0 else 0.0
        print(f"{n:<14,d} | {t_loop:<14.6f} | {t_comp:<14.6f} | {t_map:<16.6f} | {speedup:<17.2f}x")

    print("-" * 88)


# ==============================================================================
# 5. LIST COMPREHENSION VS GENERATOR EXPRESSION MEMORY PROFILING
# ==============================================================================

def profile_list_vs_generator():
    print("\n" + "=" * 88)
    print("PART 4: MEMORY PROFILING - LIST COMPREHENSION vs GENERATOR EXPRESSION")
    print("=" * 88)

    n = 1_000_000
    dataset = generate_sensor_readings(n)

    # 1. List Comprehension (Eager materialization)
    t0 = time.perf_counter()
    list_result = [c for c in dataset if -50.0 <= c <= 50.0]
    t_list = time.perf_counter() - t0
    list_mem_bytes = sys.getsizeof(list_result)

    # 2. Generator Expression (Lazy streaming)
    t0 = time.perf_counter()
    gen_result = (c for c in dataset if -50.0 <= c <= 50.0)
    t_gen_init = time.perf_counter() - t0
    gen_mem_bytes = sys.getsizeof(gen_result)

    # Stream reduction timing: sum() on generator vs sum() on list
    t0 = time.perf_counter()
    sum_from_list = sum(list_result)
    t_sum_list = time.perf_counter() - t0

    t0 = time.perf_counter()
    sum_from_gen = sum(c for c in dataset if -50.0 <= c <= 50.0)
    t_sum_gen = time.perf_counter() - t0

    assert round(sum_from_list, 2) == round(sum_from_gen, 2)

    print(f"Memory Allocation for {n:,d} sensor readings:")
    print(f"• List Comprehension   : {list_mem_bytes:,d} bytes ({list_mem_bytes / (1024**2):.2f} MB)")
    print(f"• Generator Expression : {gen_mem_bytes:,d} bytes ({gen_mem_bytes / 1024:.2f} KB)")
    print(f"• Memory Reduction Ratio: {list_mem_bytes / gen_mem_bytes:,.1f}x less memory using generator expression!")
    print(f"\nExecution & Reduction Latencies:")
    print(f"• List Materialization Time : {t_list:.6f} s")
    print(f"• Generator Creation Time   : {t_gen_init:.8f} s (Instantaneous)")
    print(f"• sum(list) Reduction Time  : {t_sum_list:.6f} s")
    print(f"• sum(generator) Stream Time: {t_sum_gen:.6f} s")


# ==============================================================================
# 6. DESIGN CONCLUSION & THEORETICAL QUESTIONS
# ==============================================================================

def print_design_analysis():
    print("\n" + "=" * 88)
    print("PART 5: DESIGN ANALYSIS & THEORETICAL ANSWERS")
    print("=" * 88)
    print("""
1. GENERAL FORM OF A LIST COMPREHENSION WITH A CONDITION:
   [<expression> for <item> in <iterable> if <condition>]
   - Evaluates: Iterates over <iterable>, filters items matching <condition>,
     applies <expression> transformation, and appends into an internal list.

2. WHEN A LIST COMPREHENSION BECOMES HARDER TO READ THAN A LOOP:
   - Nested Loops: When nesting exceeds 2 levels (e.g. 3 nested 'for' clauses).
   - Complex Multi-Branching: Multiple nested `if-else` ternary expressions.
   - Side Effects: When operations require logging, exception handling (`try-except`),
     or mutating external state, an explicit `for` loop is significantly cleaner.

3. LIST COMPREHENSION VS GENERATOR EXPRESSION:
   ┌───────────────────────┬───────────────────────────┬───────────────────────────┐
   │ Characteristic        │ List Comprehension        │ Generator Expression      │
   ├───────────────────────┼───────────────────────────┼───────────────────────────┤
   │ Syntax                │ [expr for x in seq]       │ (expr for x in seq)       │
   │ Evaluation Semantics  │ Eager (materializes all)  │ Lazy (evaluates on-demand)│
   │ Memory Footprint      │ O(n) dynamic array        │ O(1) constant frame size  │
   │ Reusability           │ Reusable sequence         │ Single-pass consumed stream│
   │ Indexing / Slicing    │ Supported (list[i])       │ Not supported (TypeError) │
   └───────────────────────┴───────────────────────────┴───────────────────────────┘

4. CONCLUSION: IS A LIST COMPREHENSION ALWAYS THE BEST CHOICE?
   - NO. As proven by our measurements:
     * When aggregating or stream-reducing (e.g. `sum()`, `min()`, `max()`, writing to a file),
       a generator expression avoids allocating millions of bytes (8.4 MB vs 200 bytes).
     * When datasets exceed physical RAM (e.g. gigabyte sensor logs), a list comprehension
       triggers OutOfMemory crashes, while generator expressions process arbitrary sizes.
     * When random access, length inspection (`len()`), or multiple passes are required,
       list comprehensions remain the fastest and most efficient choice.
""")
    print("=" * 88)


# ==============================================================================
# 7. MAIN FUNCTION
# ==============================================================================

def main():
    # Generate and save sample sensor readings file
    sample_readings = generate_sensor_readings(60, seed=2026)
    with open("temperatures_sample.txt", "w") as f:
        f.write("# Vaccine Cold-Storage Unit - 60-Minute Temperature Log (°C)\n")
        f.write(", ".join(map(str, sample_readings)) + "\n")

    demonstrate_dict_and_set_comprehensions(sample_readings)
    test_equivalence_and_edge_cases()
    run_empirical_investigation()
    profile_list_vs_generator()
    print_design_analysis()


if __name__ == "__main__":
    main()
