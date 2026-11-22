"""
Analytical Charts and Visual Architectural Diagrams Generator
Course: CSA08 / CSA0807 Python Programming - Assignment 3 (CO3)
Student: V. Karthik Harish | Register Number: 192511328
Generates 7 publication-grade figures for the 50-mark analytical laboratory report.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report_assets")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set global aesthetic styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 1.0


# ==============================================================================
# FIG 1: Q1 RAINFALL MOVING AVERAGE RUNTIME SCALING
# ==============================================================================
def generate_fig1_rainfall():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    
    n_sizes = [365, 36500, 365000]
    t_naive = [0.000228, 0.016419, 0.172745]
    t_running = [0.000114, 0.009647, 0.108006]
    t_deque = [0.000130, 0.011785, 0.120879]
    
    # Subplot 1: Latency Curve
    ax1.plot(n_sizes, t_naive, 'o-', color='#dc2626', linewidth=2.2, label='Naive Window Slice O(k·n)')
    ax1.plot(n_sizes, t_running, 's-', color='#16a34a', linewidth=2.2, label='Running Sum O(n)')
    ax1.plot(n_sizes, t_deque, '^-', color='#2563eb', linewidth=2.0, label='collections.deque O(n)')
    
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_title("A. Moving Average Execution Time (Log-Log Scale)", fontsize=12, fontweight='bold', pad=12)
    ax1.set_xlabel("Number of Daily Rainfall Readings (n)", fontsize=11, fontweight='semibold')
    ax1.set_ylabel("Execution Latency (seconds)", fontsize=11, fontweight='semibold')
    ax1.grid(True, which="both", ls="--", alpha=0.5)
    ax1.legend(frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1')
    
    # Subplot 2: Operation Count Derivation Bar Chart
    ops_labels = ['n = 365', 'n = 36,500', 'n = 365,000']
    naive_ops = [(365 - 6) * 6, (36500 - 6) * 6, (365000 - 6) * 6]
    running_ops = [6 + 2 * (365 - 7), 6 + 2 * (36500 - 7), 6 + 2 * (365000 - 7)]
    
    x = np.arange(len(ops_labels))
    width = 0.35
    
    rects1 = ax2.bar(x - width/2, [o/1000 for o in naive_ops], width, label='Naive Additions (6n - 36)', color='#f87171')
    rects2 = ax2.bar(x + width/2, [o/1000 for o in running_ops], width, label='Running-Sum Ops (2n - 8)', color='#4ade80')
    
    ax2.set_title("B. Theoretical Arithmetic Operations (Thousands)", fontsize=12, fontweight='bold', pad=12)
    ax2.set_xticks(x)
    ax2.set_xticklabels(ops_labels, fontsize=10, fontweight='semibold')
    ax2.set_ylabel("Total Operations (kilo-ops)", fontsize=11, fontweight='semibold')
    ax2.grid(True, axis='y', ls="--", alpha=0.5)
    ax2.legend(frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1')
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig_q1_rainfall_scaling.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"[✓] Generated: {path}")


# ==============================================================================
# FIG 2: Q2 BUS STOP GRID MEMORY & ALIASING ARCHITECTURAL DIAGRAM
# ==============================================================================
def generate_fig2_bus_grid():
    fig = plt.figure(figsize=(14, 6.2), dpi=300)
    
    # 1. Left Diagram: Memory reference aliasing bug vs fix
    ax1 = plt.subplot2grid((1, 2), (0, 0))
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title("A. Memory Pointer Topology: Aliased vs Corrected Grid", fontsize=12, fontweight='bold', pad=10)
    
    # Top Section: Bad Grid
    ax1.text(0.2, 9.2, "Flawed Grid: [[0]*3]*3 (Shallow Outer Replication)", fontsize=10.5, fontweight='bold', color='#dc2626')
    ax1.add_patch(patches.Rectangle((0.2, 7.2), 2.2, 1.6, facecolor='#fee2e2', edgecolor='#dc2626', lw=1.5))
    ax1.text(0.4, 8.2, "Outer List\n[ptr0, ptr1, ptr2]", fontsize=9, color='#991b1b')
    
    # Target Single Inner List
    ax1.add_patch(patches.Rectangle((5.0, 7.2), 4.2, 1.6, facecolor='#fef08a', edgecolor='#ca8a04', lw=1.5))
    ax1.text(5.2, 8.2, "Single Shared Inner List Object\n[0, 7, 0] (id: 0x2A14...)", fontsize=9, fontweight='semibold', color='#854d0e')
    
    # Arrows converging to SAME object
    ax1.annotate("", xy=(5.0, 8.4), xytext=(2.4, 8.4), arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.5))
    ax1.annotate("", xy=(5.0, 8.0), xytext=(2.4, 8.0), arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.5))
    ax1.annotate("", xy=(5.0, 7.6), xytext=(2.4, 7.6), arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.5))
    ax1.text(2.6, 8.7, "bad[0] is bad[1] is True", fontsize=8.5, color='#dc2626', style='italic')

    # Bottom Section: Good Grid
    ax1.text(0.2, 5.2, "Corrected Grid: [[0]*3 for _ in range(3)] (Independent)", fontsize=10.5, fontweight='bold', color='#16a34a')
    ax1.add_patch(patches.Rectangle((0.2, 2.0), 2.2, 2.6, facecolor='#dcfce7', edgecolor='#16a34a', lw=1.5))
    ax1.text(0.4, 3.4, "Outer List\n[ptr0, ptr1, ptr2]", fontsize=9, color='#166534')
    
    # 3 Separate Inner Lists
    for i in range(3):
        y_pos = 3.8 - i * 1.0
        val_str = "[0, 7, 0]" if i == 0 else "[0, 0, 0]"
        ax1.add_patch(patches.Rectangle((5.0, y_pos), 4.2, 0.75, facecolor='#f1f5f9', edgecolor='#475569', lw=1.2))
        ax1.text(5.2, y_pos + 0.22, f"Row {i} List: {val_str}", fontsize=8.5, color='#1e293b')
        ax1.annotate("", xy=(5.0, y_pos + 0.37), xytext=(2.4, 3.8 - i * 0.7), 
                     arrowprops=dict(arrowstyle="->", color="#16a34a", lw=1.4))
    ax1.text(2.6, 1.3, "good[0] is good[1] is False", fontsize=8.5, color='#16a34a', style='italic')

    # 2. Right Subplot: Memory Allocation (Tuple vs List & Dense vs Sparse Grid)
    ax2 = plt.subplot2grid((1, 2), (0, 1))
    
    categories = ['Dense Grid (1000x1000)\nList-of-Lists', 'Sparse Dict Grid\n250 Active Stops', 'List (1M ints)\nDynamic Array', 'Tuple (1M ints)\nFixed Immutability']
    mem_mb = [7.98, 0.045, 8.54, 8.00]
    colors = ['#f87171', '#34d399', '#60a5fa', '#a78bfa']
    
    bars = ax2.bar(categories, mem_mb, color=colors, edgecolor='#334155', width=0.55)
    ax2.set_title("B. Memory Footprint Profile (Megabytes)", fontsize=12, fontweight='bold', pad=12)
    ax2.set_ylabel("Memory Allocated (MB)", fontsize=11, fontweight='semibold')
    ax2.grid(True, axis='y', ls="--", alpha=0.5)
    
    for bar in bars:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., h + 0.15, f"{h:.2f} MB", ha='center', va='bottom', fontsize=9.5, fontweight='bold')
    
    ax2.set_ylim(0, 10.5)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig_q2_grid_memory_aliasing.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"[✓] Generated: {path}")


# ==============================================================================
# FIG 3: Q3 FARMER HELPLINE WORD COUNTING SCALING
# ==============================================================================
def generate_fig3_farmer_helpline():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    
    n_complaints = [1000, 10000, 100000]
    t_get = [0.000278, 0.003045, 0.030394]
    t_counter = [0.000169, 0.001713, 0.017684]
    t_count = [0.001963, 0.019476, 0.179324]
    
    # Subplot 1: Runtime Comparison
    ax1.plot(n_complaints, t_counter, 's-', color='#16a34a', linewidth=2.2, label='collections.Counter O(n) (C-Optimized)')
    ax1.plot(n_complaints, t_get, 'o-', color='#2563eb', linewidth=2.2, label='dict.get() Loop O(n)')
    ax1.plot(n_complaints, t_count, 'd--', color='#dc2626', linewidth=2.0, label='list.count() Nested Loop O(n·d)')
    
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_title("A. Word Frequency Runtime vs Dataset Size", fontsize=12, fontweight='bold', pad=12)
    ax1.set_xlabel("Number of Farmer Complaints (n)", fontsize=11, fontweight='semibold')
    ax1.set_ylabel("Execution Latency (seconds)", fontsize=11, fontweight='semibold')
    ax1.grid(True, which="both", ls="--", alpha=0.5)
    ax1.legend(frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1')
    
    # Subplot 2: Algorithmic Efficiency Bar at 100,000 Complaints
    methods = ['collections.Counter', 'dict.get() Loop', 'list.count() (45 words)', 'list.count() (5k vocab)']
    times_ms = [17.68, 30.39, 179.32, 19920.0]  # Projected full vocabulary
    bar_colors = ['#22c55e', '#3b82f6', '#f59e0b', '#ef4444']
    
    bars = ax2.bar(methods, times_ms, color=bar_colors, edgecolor='#334155', width=0.5)
    ax2.set_yscale('log')
    ax2.set_title("B. Production Latency for 100,000 Complaints (Log ms)", fontsize=12, fontweight='bold', pad=12)
    ax2.set_ylabel("Processing Latency (milliseconds)", fontsize=11, fontweight='semibold')
    ax2.set_xticklabels(methods, rotation=15, ha='right', fontsize=9.5, fontweight='semibold')
    ax2.grid(True, axis='y', ls="--", alpha=0.5)
    
    for bar in bars:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., h * 1.25, f"{h:,.1f} ms", ha='center', va='bottom', fontsize=9, fontweight='bold')
        
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig_q3_complaint_scaling.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"[✓] Generated: {path}")


# ==============================================================================
# FIG 4: Q4 ELECTIVE VENN DIAGRAM & MEMBERSHIP BENCHMARK
# ==============================================================================
def generate_fig4_elective_sets():
    fig = plt.figure(figsize=(14, 6.0), dpi=300)
    
    # 1. Left Diagram: Venn Diagram of Sets
    ax1 = plt.subplot2grid((1, 2), (0, 0))
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title("A. Elective Course Venn Diagram (AI & IoT Registration)", fontsize=12, fontweight='bold', pad=10)
    
    # Universal Box (All Students)
    ax1.add_patch(patches.Rectangle((0.5, 0.5), 9.0, 8.5, facecolor='#f8fafc', edgecolor='#64748b', lw=2.0))
    ax1.text(0.8, 8.4, "Universal Set: All Students (192311001 to 192311010)", fontsize=9.5, fontweight='bold', color='#1e293b')
    
    # Circle AI
    circle_ai = patches.Circle((4.0, 5.0), 2.6, facecolor='#93c5fd', edgecolor='#2563eb', alpha=0.6, lw=2.0)
    # Circle IoT
    circle_iot = patches.Circle((6.0, 5.0), 2.6, facecolor='#fca5a5', edgecolor='#dc2626', alpha=0.6, lw=2.0)
    ax1.add_patch(circle_ai)
    ax1.add_patch(circle_iot)
    
    # Region Labels
    ax1.text(2.6, 6.5, "AI Elective\n(4 students)", fontsize=10, fontweight='bold', color='#1e40af', ha='center')
    ax1.text(7.4, 6.5, "IoT Elective\n(4 students)", fontsize=10, fontweight='bold', color='#991b1b', ha='center')
    
    # AI Only (AI - IoT)
    ax1.text(2.6, 4.8, "Only AI:\n192311001\n192311007", fontsize=8.5, color='#1e3a8a', ha='center')
    # IoT Only (IoT - AI)
    ax1.text(7.4, 4.8, "Only IoT:\n192311002\n192311010", fontsize=8.5, color='#7f1d1d', ha='center')
    # Intersection Clash Zone (AI & IoT)
    ax1.text(5.0, 4.8, "CLASH (&):\n192311004\n192311009", fontsize=9, fontweight='bold', color='#450a0a', ha='center')
    
    # Unregistered (Outside Circles)
    ax1.text(5.0, 1.2, "Unregistered / Neither (All - (AI ∪ IoT)):\n{192311003, 192311005, 192311006, 192311008}", 
             fontsize=9, fontweight='semibold', color='#334155', ha='center',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='#e2e8f0', edgecolor='#94a3b8'))

    # 2. Right Subplot: Membership Testing (x in list vs x in set)
    ax2 = plt.subplot2grid((1, 2), (0, 1))
    sizes = [10000, 100000, 1000000]
    t_list_us = [87.91, 757.14, 8369.82]   # microseconds
    t_set_us = [0.018, 0.018, 0.018]       # microseconds
    
    ax2.plot(sizes, t_list_us, 'o-', color='#dc2626', linewidth=2.2, label='x in list (O(n) Linear Scan)')
    ax2.plot(sizes, t_set_us, 's-', color='#16a34a', linewidth=2.2, label='x in set (O(1) Hash Table Lookup)')
    
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_title("B. Membership Search Latency (Log-Log Scale)", fontsize=12, fontweight='bold', pad=12)
    ax2.set_xlabel("Number of Registered Students (N)", fontsize=11, fontweight='semibold')
    ax2.set_ylabel("Query Latency (microseconds)", fontsize=11, fontweight='semibold')
    ax2.grid(True, which="both", ls="--", alpha=0.5)
    ax2.legend(frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1')
    
    ax2.text(200000, 0.05, "466,000x Speedup\nat N = 1,000,000", fontsize=9.5, fontweight='bold', color='#16a34a',
             bbox=dict(boxstyle="round,pad=0.4", facecolor='#dcfce7', edgecolor='#86efac'))
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig_q4_set_venn_and_lookup.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"[✓] Generated: {path}")


# ==============================================================================
# FIG 5: Q5 SENSOR CLEANING LIST COMP VS GENERATOR BENCHMARK
# ==============================================================================
def generate_fig5_sensor_cleaning():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    
    sizes = [10000, 100000, 1000000]
    t_loop = [0.003079, 0.025525, 0.316379]
    t_comp = [0.003270, 0.036306, 0.322398]
    t_map = [0.003467, 0.041397, 0.431409]
    
    # Subplot 1: Execution Latency across methods
    ax1.plot(sizes, t_comp, 's-', color='#2563eb', linewidth=2.2, label='List Comprehension')
    ax1.plot(sizes, t_loop, 'o-', color='#16a34a', linewidth=2.0, label='for-loop with append()')
    ax1.plot(sizes, t_map, '^-', color='#f59e0b', linewidth=2.0, label='map() + filter() + lambda')
    
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_title("A. Transformation Latency across Iteration Styles", fontsize=12, fontweight='bold', pad=12)
    ax1.set_xlabel("Number of Vaccine Sensor Readings (N)", fontsize=11, fontweight='semibold')
    ax1.set_ylabel("Execution Latency (seconds)", fontsize=11, fontweight='semibold')
    ax1.grid(True, which="both", ls="--", alpha=0.5)
    ax1.legend(frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1')
    
    # Subplot 2: Memory Footprint (List Comp vs Generator Expression)
    cats = ['List Comprehension\n(Eager Materialization)', 'Generator Expression\n(Lazy Stream Iterator)']
    mem_kb = [8448.7, 0.216]
    colors = ['#ef4444', '#10b981']
    
    bars = ax2.bar(cats, mem_kb, color=colors, edgecolor='#334155', width=0.45)
    ax2.set_yscale('log')
    ax2.set_title("B. Memory Footprint for 1,000,000 Readings (Log KB)", fontsize=12, fontweight='bold', pad=12)
    ax2.set_ylabel("Memory Consumption (Kilobytes)", fontsize=11, fontweight='semibold')
    ax2.grid(True, axis='y', ls="--", alpha=0.5)
    
    ax2.text(0, mem_kb[0] * 1.3, "8,448 KB (8.25 MB)", ha='center', fontsize=9.5, fontweight='bold', color='#b91c1c')
    ax2.text(1, mem_kb[1] * 2.0, "0.216 KB (216 Bytes)\n[39,114x Less RAM!]", ha='center', fontsize=9.5, fontweight='bold', color='#047857')
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig_q5_sensor_cleaning_benchmark.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"[✓] Generated: {path}")


# ==============================================================================
# FIG 6: Q6 RAILWAY TIMETABLE INDEX SPEEDUP & HIERARCHY
# ==============================================================================
def generate_fig6_railway():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    
    trains = [100, 1000, 10000]
    t_linear_ms = [0.062, 0.414, 5.448]
    t_indexed_ms = [0.014, 0.148, 2.142]
    
    # Subplot 1: Linear Scan vs Indexed Query Latency
    ax1.plot(trains, t_linear_ms, 'o-', color='#dc2626', linewidth=2.2, label='Linear Scan O(T·S) (No Index)')
    ax1.plot(trains, t_indexed_ms, 's-', color='#16a34a', linewidth=2.2, label='Inverted Station Index O(K)')
    
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_title("A. Railway Station Query Latency vs Timetable Size", fontsize=12, fontweight='bold', pad=12)
    ax1.set_xlabel("Total Trains in Master Timetable (T)", fontsize=11, fontweight='semibold')
    ax1.set_ylabel("Query Latency (milliseconds)", fontsize=11, fontweight='semibold')
    ax1.grid(True, which="both", ls="--", alpha=0.5)
    ax1.legend(frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1')
    
    # Subplot 2: Structural Breakdown & Index Overhead
    comps = ['Master Timetable\n(1,000 Trains)', 'Inverted Index\n(Station Hash Map)', 'Flat Tuple Array\n(Alternative)']
    mems = [205.11, 56.22, 142.30]
    colors = ['#3b82f6', '#8b5cf6', '#64748b']
    
    bars = ax2.bar(comps, mems, color=colors, edgecolor='#334155', width=0.5)
    ax2.set_title("B. Data Structure Memory Profile (1,000 Trains)", fontsize=12, fontweight='bold', pad=12)
    ax2.set_ylabel("Memory Footprint (Kilobytes)", fontsize=11, fontweight='semibold')
    ax2.grid(True, axis='y', ls="--", alpha=0.5)
    
    for bar in bars:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., h + 5.0, f"{h:.1f} KB", ha='center', va='bottom', fontsize=9.5, fontweight='bold')
    
    ax2.set_ylim(0, 245)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig_q6_timetable_index_speedup.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"[✓] Generated: {path}")


# ==============================================================================
# FIG 7: Q7 CONTACT MERGING SCALABILITY (HASH DSU VS PAIRWISE O(N^2))
# ==============================================================================
def generate_fig7_contact_merging():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    
    contacts = [1000, 10000, 100000]
    t_dsu = [0.004564, 0.054028, 0.813197]
    t_pairwise = [0.1377, 14.90, 1260.0]  # Measured and extrapolated
    
    # Subplot 1: Scalability Scaling Curves
    ax1.plot(contacts, t_dsu, 's-', color='#16a34a', linewidth=2.4, label='Inverted Hash + DSU O(N·α(N)) (Our Design)')
    ax1.plot(contacts, t_pairwise, 'o--', color='#dc2626', linewidth=2.2, label='Pairwise Compare All Pairs O(N²)')
    
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_title("A. Contact Merging Scalability: O(N) vs O(N²)", fontsize=12, fontweight='bold', pad=12)
    ax1.set_xlabel("Number of Multi-Source Contacts (N)", fontsize=11, fontweight='semibold')
    ax1.set_ylabel("Processing Latency (seconds, log scale)", fontsize=11, fontweight='semibold')
    ax1.grid(True, which="both", ls="--", alpha=0.5)
    ax1.legend(frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1')
    
    # Subplot 2: Comparisons at 100,000 Contacts
    labels = ['Inverted Hash DSU\n(Single Pass Hash)', 'Pairwise Comparison\n(10 Billion Pairs)']
    times_sec = [0.813, 1260.0]  # ~21 minutes to hours
    b_colors = ['#22c55e', '#ef4444']
    
    bars = ax2.bar(labels, times_sec, color=b_colors, edgecolor='#334155', width=0.45)
    ax2.set_yscale('log')
    ax2.set_title("B. Runtime at N = 100,000 Contacts", fontsize=12, fontweight='bold', pad=12)
    ax2.set_ylabel("Total Processing Time (seconds, log scale)", fontsize=11, fontweight='semibold')
    ax2.grid(True, axis='y', ls="--", alpha=0.5)
    
    ax2.text(0, 1.2, "0.81 seconds\n(Real-time)", ha='center', fontsize=9.5, fontweight='bold', color='#15803d')
    ax2.text(1, 1500.0, "1,260 seconds (~21 mins)\n[1,550x Slower!]", ha='center', fontsize=9.5, fontweight='bold', color='#b91c1c')
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig_q7_contact_merging_scalability.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"[✓] Generated: {path}")


if __name__ == "__main__":
    generate_fig1_rainfall()
    generate_fig2_bus_grid()
    generate_fig3_farmer_helpline()
    generate_fig4_elective_sets()
    generate_fig5_sensor_cleaning()
    generate_fig6_railway()
    generate_fig7_contact_merging()
    print("\n[✓] All 7 publication-quality analytical report figures successfully generated.")
