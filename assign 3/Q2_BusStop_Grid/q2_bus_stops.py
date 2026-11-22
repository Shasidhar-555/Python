"""
Task 02: Tuples, Mutability and Copying - City Bus-Stop Map
Course: CSA08 / CSA0807 Python Programming (CO3)
Bloom's Level: K4 - Analyse

Problem Context - City Bus-Stop Map:
A city bus service stores GPS coordinates of stops as (latitude, longitude) tuples
and uses a grid of zones (rows x cols) to count passengers boarding in each zone.
A developer created the grid with `[[0] * cols] * rows`, causing shallow reference
aliasing where updating one row mutates all rows.

Key Deliverables:
1. Complete the Code (TODO 1) generating distinct row lists with a list comprehension.
2. Demonstration of why tuples can be dict keys while lists cannot (TypeError: unhashable).
3. Demonstration of aliasing, shallow copying, and deep copying.
4. Tuple unpacking in loops.
5. In-place list mutation inside a tuple and its effect on hashability.
6. Empirical memory (sys.getsizeof) and latency benchmarks for 1,000,000 items.
7. Alternative Concept: Sparse dictionary grid keyed by (row, col) vs dense matrix.
"""

import sys
import copy
import time
import json


# ==============================================================================
# 1. COMPLETE THE CODE (AS GIVEN IN ASSIGNMENT SPECIFICATION)
# ==============================================================================

def execute_complete_the_code():
    print("=" * 88)
    print("PART 1: 'COMPLETE THE CODE' - GRID DUPLICATION FIX & TUPLE KEYS")
    print("=" * 88)

    rows, cols = 3, 4

    bad = [[0] * cols] * rows          # every row is the SAME list object
    bad[0][1] = 7

    # TODO 1: Create a rows x cols grid of zeros using a list comprehension so that every
    #   row is a separate list
    good = [[0] * cols for _ in range(rows)]
    good[0][1] = 7

    print("bad :", bad)
    print("good:", good)
    print(bad[0] is bad[1], good[0] is good[1])

    # Tuples are immutable, so they can be used as dictionary keys
    stops = {(13.0827, 80.2707): "Chennai Central", (13.0418, 80.2341): "T. Nagar"}
    print(stops[(13.0418, 80.2341)])

    # Verification against expected output
    assert bad == [[0, 7, 0, 0], [0, 7, 0, 0], [0, 7, 0, 0]]
    assert good == [[0, 7, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    assert (bad[0] is bad[1]) is True
    assert (good[0] is good[1]) is False
    assert stops[(13.0418, 80.2341)] == "T. Nagar"
    print("\n[✓] Complete the Code passed all assertions matching expected assignment output.")


# ==============================================================================
# 2. HASHABILITY EXPERIMENT: LIST AS DICTIONARY KEY ERROR
# ==============================================================================

def test_list_as_dict_key():
    print("\n" + "=" * 88)
    print("PART 2: HASHABILITY EXPERIMENT - LIST AS DICTIONARY KEY")
    print("=" * 88)
    
    stop_list = [13.0418, 80.2341]
    print(f"Attempting to insert key of type {type(stop_list)}: {stop_list} into a dictionary...")
    try:
        invalid_dict = {}
        invalid_dict[stop_list] = "T. Nagar"
    except TypeError as e:
        print(f"CAUGHT EXPECTED ERROR: TypeError: {e}")
        print("\nEXPLANATION:")
        print("1. Python dictionaries are implemented as open-address hash tables.")
        print("2. A dictionary key must implement `__hash__()` and satisfy the invariant that")
        print("   its hash value never changes throughout its lifetime.")
        print("3. Lists are mutable (elements can be appended, removed, or reassigned in-place).")
        print("   If a list could be hashed, mutating the list would change its hash value,")
        print("   meaning the key would now be located in the wrong hash bucket, making lookup")
        print("   impossible and corrupting hash table integrity.")
        print("4. Therefore, lists deliberately set `__hash__ = None` in CPython, raising TypeError.")
        print("5. Tuples containing only immutable elements are hashable and guarantee immutable integrity.")


# ==============================================================================
# 3. ALIASING, SHALLOW COPY, AND DEEP COPY DEMONSTRATION
# ==============================================================================

def demonstrate_copy_semantics():
    print("\n" + "=" * 88)
    print("PART 3: ALIASING, SHALLOW COPY, AND DEEP COPY IN BUS-STOP PASSENGER GRIDS")
    print("=" * 88)

    original_grid = [
        [15, 20, 0],
        [30, 45, 12]
    ]

    # 1. Aliasing (Simple assignment)
    aliased_grid = original_grid
    aliased_grid[0][0] = 999
    print(f"1. Aliasing (aliased_grid = original_grid):")
    print(f"   aliased_grid is original_grid : {aliased_grid is original_grid}")
    print(f"   original_grid[0][0] modified  : {original_grid[0][0]} (Changed!)")

    # Reset
    original_grid[0][0] = 15

    # 2. Shallow Copy (copy.copy or slicing [:])
    shallow_grid = copy.copy(original_grid)
    shallow_slice = original_grid[:]
    print(f"\n2. Shallow Copy (shallow_grid = copy.copy(original_grid)):")
    print(f"   shallow_grid is original_grid         : {shallow_grid is original_grid} (Outer list is NEW)")
    print(f"   shallow_grid[0] is original_grid[0]   : {shallow_grid[0] is original_grid[0]} (Inner row lists are SHARED!)")
    
    # Mutating top-level of shallow copy vs mutating nested element
    shallow_grid.append([0, 0, 0])
    print(f"   Appended row to shallow copy -> len(original): {len(original_grid)}, len(shallow): {len(shallow_grid)}")
    shallow_grid[0][1] = 777
    print(f"   Modified nested element shallow_grid[0][1] = 777:")
    print(f"   original_grid[0][1] is now            : {original_grid[0][1]} (Shared reference updated!)")

    # Reset
    original_grid[0][1] = 20

    # 3. Deep Copy (copy.deepcopy)
    deep_grid = copy.deepcopy(original_grid)
    print(f"\n3. Deep Copy (deep_grid = copy.deepcopy(original_grid)):")
    print(f"   deep_grid is original_grid           : {deep_grid is original_grid} (Outer list is NEW)")
    print(f"   deep_grid[0] is original_grid[0]     : {deep_grid[0] is original_grid[0]} (Inner row lists are NEW!)")
    deep_grid[0][0] = 888
    print(f"   deep_grid[0][0] = 888 -> original_grid[0][0]: {original_grid[0][0]} (Completely Isolated!)")


# ==============================================================================
# 4. FUNCTION ARGUMENT MUTABILITY (CALL-BY-OBJECT-REFERENCE)
# ==============================================================================

def add_passenger_trip(zone_counts: list[list[int]], row: int, col: int, boardings: int):
    """
    Mutates caller's nested list in-place because Python passes object references by value.
    """
    zone_counts[row][col] += boardings


def demonstrate_call_by_reference():
    print("\n" + "=" * 88)
    print("PART 4: FUNCTION ARGUMENT MUTABILITY (PASS-BY-ASSIGNMENT)")
    print("=" * 88)
    
    grid = [[0, 0], [0, 0]]
    print(f"Caller's grid before function call: {grid} (id: {id(grid)})")
    add_passenger_trip(grid, 0, 1, 5)
    print(f"Caller's grid after function call : {grid} (id: {id(grid)})")
    print("EXPLANATION:")
    print("Python uses 'call-by-object-reference'. The parameter 'zone_counts' binds to the exact")
    print("same list object in memory. In-place modifications (indexing, append) directly mutate")
    print("the underlying object visible to the caller.")


# ==============================================================================
# 5. TUPLE UNPACKING IN FOR LOOPS
# ==============================================================================

def demonstrate_tuple_unpacking():
    print("\n" + "=" * 88)
    print("PART 5: TUPLE UNPACKING IN CITY BUS NETWORK")
    print("=" * 88)

    bus_stops = {
        (13.0827, 80.2707): {"name": "Chennai Central", "zone": (0, 1), "routes": 42},
        (13.0418, 80.2341): {"name": "T. Nagar", "zone": (1, 2), "routes": 65},
        (12.9815, 80.2180): {"name": "Guindy Kathipara", "zone": (2, 0), "routes": 58},
        (13.0594, 80.2834): {"name": "Marina Beach", "zone": (0, 3), "routes": 24},
        (12.9915, 80.2337): {"name": "Saidapet", "zone": (1, 1), "routes": 37}
    }

    print(f"{'Bus Stop Name':<20} | {'Latitude':<10} | {'Longitude':<10} | {'Zone (R,C)':<12} | {'Routes':<6}")
    print("-" * 72)
    # Tuple unpacking in for loop: (lat, lon) unpacked from dictionary key
    for (lat, lon), info in bus_stops.items():
        r, c = info["zone"]
        print(f"{info['name']:<20} | {lat:<10.4f} | {lon:<10.4f} | ({r}, {c}){'':<6} | {info['routes']:<6}")


# ==============================================================================
# 6. MUTABLE LIST STORED INSIDE AN IMMUTABLE TUPLE
# ==============================================================================

def test_mutable_inside_tuple():
    print("\n" + "=" * 88)
    print("PART 6: MUTABLE LIST INSIDE AN IMMUTABLE TUPLE")
    print("=" * 88)

    hybrid_tuple = ("Chennai Central", [10, 20, 30])
    print(f"Original tuple: {hybrid_tuple} (id: {id(hybrid_tuple)})")

    # 1. Reassigning the tuple slot raises TypeError (tuple is immutable)
    try:
        hybrid_tuple[1] = [50, 60]
    except TypeError as e:
        print(f"Attempting `hybrid_tuple[1] = ...`: TypeError: {e}")

    # 2. Mutating the list object within the tuple succeeds!
    hybrid_tuple[1].append(40)
    print(f"After `hybrid_tuple[1].append(40)`: {hybrid_tuple}")
    print("Notice the tuple ID remains unchanged:", id(hybrid_tuple))

    # 3. Hashability failure
    try:
        hash(hybrid_tuple)
    except TypeError as e:
        print(f"Attempting `hash(hybrid_tuple)`: TypeError: {e}")
    print("EXPLANATION: A tuple's structure is fixed, but if it contains pointers to mutable")
    print("objects, those inner objects can mutate in-place, which forfeits hashability.")


# ==============================================================================
# 7. EMPIRICAL BENCHMARK: TUPLE VS LIST (MEMORY & RUNTIME)
# ==============================================================================

def run_empirical_investigation():
    print("\n" + "=" * 88)
    print("PART 7: EMPIRICAL BENCHMARK - TUPLE VS LIST (1,000,000 VALUES)")
    print("=" * 88)

    n = 1_000_000
    
    # 1. Memory Measurement (sys.getsizeof)
    test_list = list(range(n))
    test_tuple = tuple(test_list)

    list_mem_bytes = sys.getsizeof(test_list)
    tuple_mem_bytes = sys.getsizeof(test_tuple)

    print(f"Memory Allocation for {n:,d} elements:")
    print(f"• List  Size : {list_mem_bytes:,d} bytes ({list_mem_bytes / (1024**2):.2f} MB)")
    print(f"• Tuple Size : {tuple_mem_bytes:,d} bytes ({tuple_mem_bytes / (1024**2):.2f} MB)")
    print(f"• Memory Overhead Difference: {list_mem_bytes - tuple_mem_bytes:,d} bytes saved by tuple ({((list_mem_bytes - tuple_mem_bytes)/list_mem_bytes)*100:.2f}% reduction)")

    # 2. Creation Timing
    t0 = time.perf_counter()
    _ = [i for i in range(n)]
    t_list_create = time.perf_counter() - t0

    t0 = time.perf_counter()
    _ = tuple(i for i in range(n))
    t_tuple_create = time.perf_counter() - t0

    # 3. Indexing Timing (10,000,000 lookups)
    num_lookups = 5_000_000
    
    t0 = time.perf_counter()
    for _ in range(num_lookups):
        _ = test_list[500_000]
    t_list_lookup = time.perf_counter() - t0

    t0 = time.perf_counter()
    for _ in range(num_lookups):
        _ = test_tuple[500_000]
    t_tuple_lookup = time.perf_counter() - t0

    print(f"\nTiming Comparison:")
    print(f"• List Creation Time  : {t_list_create:.6f} s")
    print(f"• Tuple Creation Time : {t_tuple_create:.6f} s")
    print(f"• List Lookup ({num_lookups:,d} reads) : {t_list_lookup:.6f} s")
    print(f"• Tuple Lookup ({num_lookups:,d} reads): {t_tuple_lookup:.6f} s")


# ==============================================================================
# 8. ALTERNATIVE CONCEPT: SPARSE DICTIONARY GRID VS DENSE 2D LIST
# ==============================================================================

def evaluate_sparse_vs_dense():
    print("\n" + "=" * 88)
    print("PART 8: ALTERNATIVE CONCEPT - SPARSE DICT GRID VS DENSE 2D LIST")
    print("=" * 88)

    rows, cols = 1000, 1000  # 1,000,000 total zones
    num_active_stops = 250   # Only 250 zones have passenger activity

    # 1. Dense Representation: List of Lists
    t0 = time.perf_counter()
    dense_grid = [[0] * cols for _ in range(rows)]
    for i in range(num_active_stops):
        dense_grid[i][i] = 10 + i
    t_dense_build = time.perf_counter() - t0
    dense_mem = sys.getsizeof(dense_grid) + sum(sys.getsizeof(row) for row in dense_grid)

    # 2. Sparse Representation: Dictionary keyed by (row, col)
    t0 = time.perf_counter()
    sparse_grid = {}
    for i in range(num_active_stops):
        sparse_grid[(i, i)] = 10 + i
    t_sparse_build = time.perf_counter() - t0
    sparse_mem = sys.getsizeof(sparse_grid) + sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in sparse_grid.items())

    print(f"Grid Configuration: {rows} x {cols} = {rows*cols:,d} total zones | Active Zones: {num_active_stops}")
    print(f"• Dense List of Lists : Memory = {dense_mem / 1024:.2f} KB | Build Time = {t_dense_build:.6f} s")
    print(f"• Sparse Dict Grid    : Memory = {sparse_mem / 1024:.2f} KB | Build Time = {t_sparse_build:.6f} s")
    print(f"• Memory Reduction Ratio: {dense_mem / sparse_mem:.1f}x less memory using sparse dictionary!")
    print("\nComplexity Analysis:")
    print("• Dense Matrix: Access time O(1) via dense_grid[r][c]. Space O(rows * cols).")
    print("• Sparse Dict : Access time O(1) average via sparse_grid.get((r, c), 0). Space O(E) where E = active stops.")


# ==============================================================================
# 9. MAIN EXECUTION & JSON SAMPLE GENERATION
# ==============================================================================

def main():
    # Save sample bus stop dataset
    sample_stops = [
        {"name": "Chennai Central", "lat": 13.0827, "lon": 80.2707, "zone": [0, 1], "daily_passengers": 14200},
        {"name": "T. Nagar", "lat": 13.0418, "lon": 80.2341, "zone": [1, 2], "daily_passengers": 21500},
        {"name": "Guindy Kathipara", "lat": 12.9815, "lon": 80.2180, "zone": [2, 0], "daily_passengers": 18900},
        {"name": "Marina Beach", "lat": 13.0594, "lon": 80.2834, "zone": [0, 3], "daily_passengers": 8300},
        {"name": "Saidapet", "lat": 12.9915, "lon": 80.2337, "zone": [1, 1], "daily_passengers": 11400}
    ]
    with open("bus_stops_sample.json", "w") as f:
        json.dump(sample_stops, f, indent=2)

    execute_complete_the_code()
    test_list_as_dict_key()
    demonstrate_copy_semantics()
    demonstrate_call_by_reference()
    demonstrate_tuple_unpacking()
    test_mutable_inside_tuple()
    run_empirical_investigation()
    evaluate_sparse_vs_dense()

    print("\n" + "=" * 88)
    print("CONCLUSION: WHEN TO USE TUPLE VS LIST & IMMUTABILITY PROTECTION")
    print("=" * 88)
    print("""
1. WHEN TO USE A TUPLE:
   - For heterogeneous fixed records (e.g. coordinates (lat, lon), database rows, RGB colors).
   - Whenever an object must serve as a dictionary key or set element (demands hashability).
   - When communicating data across functions that must NEVER be modified in-place by callers.
   - For read-only data structures where memory efficiency and immutability guarantees matter.

2. WHAT IMMUTABILITY PROTECTS YOU FROM:
   - Accidental Side Effects: Prevents helper functions or background threads from silently
     modifying shared state.
   - Hash Table Invariant Corruption: Ensures dictionary and set keys maintain constant hash
     values and bucket assignments throughout program execution.
   - Aliasing Bugs: Eliminates bugs where two variables referencing the same sequence cause
     unintended synchronized mutations (as demonstrated in the `[[0]*cols]*rows` bug).
""")
    print("=" * 88)


if __name__ == "__main__":
    main()
