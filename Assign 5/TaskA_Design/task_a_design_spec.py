"""
Part A: Data Acquisition, Cleaning, Analysis & AI Application Design
File: TaskA_Design/task_a_design_spec.py
Course: CSA08 - Python Programming (Assignment 5)
Student: V. Karthik Harish (Reg No: 192511328)

Contains formal design specifications, SIMATS Engineering Algorithmic Pseudocode,
relational database schemas, cleaning rules, normalisation formulas,
and AI application architecture.
"""

import os
import sys
import sqlite3

TASK_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TASK_DIR)
OUTPUT_TXT = os.path.join(TASK_DIR, "output.txt")
OUTPUT_PNG = os.path.join(TASK_DIR, "output_screenshot.png")

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def log_print(msg, fh=None):
    print(msg)
    if fh:
        fh.write(msg + "\n")


def task_a1_acquisition_design(fh):
    log_print("=" * 86, fh)
    log_print("TASK A1: DESIGN THE DATA ACQUISITION (City Air-Quality Monitoring Network)", fh)
    log_print("=" * 86, fh)

    log_print("A1.1 — Inspect the Source & Expected Data-Quality Problems:", fh)
    problems = [
        ("Missing / Blank Readings", "date,hour,pm25,pm10,no2,temperature", "2026-10-01,14,,45,22,30.5", "Sensor packet dropped or connection timeout; yields empty string '' or 'NA'."),
        ("Negative Sensor Values", "Uncalibrated zero-point drift", "2026-10-01,03,-12.4,18,10,24.0", "Physical concentration of matter cannot be negative; indicates calibration failure."),
        ("Impossibly Large Values", "Electrical power spike / ADC short", "2026-10-01,18,9999.0,80,45,28.0", "Exceeds physical atmospheric ceiling (e.g. PM2.5 > 1000 µg/m³)."),
        ("Unit Inconsistency", "Two stations transmit Fahrenheit", "2026-10-01,12,45,80,30,86.0", "Station reports 86.0°F instead of 30.0°C; distorts regional thermal statistics."),
        ("Duplicate Telemetry Rows", "Cellular retry buffer retransmission", "2026-10-01,08,55,90,32,27.0", "Same station, date, and hour repeated multiple times with identical or conflicting values."),
        ("Corrupted Delimiters / Garbage", "Transmission line noise", "2026-10-01;09;50;85;NA", "Semicolons instead of commas, non-ASCII characters, or truncated line buffers.")
    ]
    for name, trigger, example, impact in problems:
        log_print(f"  • {name:<26}: e.g. '{example}' | {impact}", fh)

    log_print("\nA1.2 — Relational Database Schema Design (SQLite):", fh)
    schema_sql = """
    -- Master station registry table
    CREATE TABLE IF NOT EXISTS stations (
        station_id TEXT PRIMARY KEY,
        station_name TEXT NOT NULL,
        zone TEXT NOT NULL,
        latitude REAL,
        longitude REAL,
        native_temp_unit TEXT DEFAULT 'C'
    );

    -- Cleaned hourly telemetry readings table
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_id TEXT NOT NULL,
        reading_date TEXT NOT NULL,      -- ISO-8601: YYYY-MM-DD
        hour INTEGER NOT NULL,           -- 0 to 23
        pm25 REAL,                       -- µg/m³
        pm10 REAL,                       -- µg/m³
        no2 REAL,                        -- ppb
        temperature REAL,                -- Standardized Celsius (°C)
        pm25_minmax REAL,                -- Normalized [0, 1]
        pm25_zscore REAL,                -- Standardized (mean=0, std=1)
        FOREIGN KEY (station_id) REFERENCES stations(station_id),
        UNIQUE(station_id, reading_date, hour)
    );

    -- Composite B-Tree index for instantaneous spatial-temporal queries
    CREATE INDEX IF NOT EXISTS idx_station_date ON readings(station_id, reading_date);
    CREATE INDEX IF NOT EXISTS idx_date_hour ON readings(reading_date, hour);
    """
    log_print(schema_sql.strip(), fh)

    log_print("\nA1.3 — CSV vs SQL Architectural Comparison for Typical Board Questions:", fh)
    comparisons = [
        ("Q1: Average PM2.5 of Adyar in October", "Scan 12 daily CSVs per day (372 files), parse strings in Python loop.", "SELECT AVG(pm25) FROM readings WHERE station_id='Adyar' AND reading_date LIKE '2026-10-%';", "SQL is ~80x faster via B-Tree index scan."),
        ("Q2: Top 3 polluted stations by monthly PM10", "Load all files into memory, build dictionary in Python, sort keys.", "SELECT station_id, AVG(pm10) FROM readings GROUP BY station_id ORDER BY AVG(pm10) DESC LIMIT 3;", "SQL engine executes optimized in-engine hash aggregate & sort."),
        ("Q3: Hourly diurnal trend across all stations", "Read all rows, bucket by hour in Python defaultdict, compute mean.", "SELECT hour, AVG(pm25) FROM readings GROUP BY hour ORDER BY hour;", "SQL aggregates millions of rows in milliseconds using disk paging.")
    ]
    for q, csv_approach, sql_approach, verdict in comparisons:
        log_print(f"  • {q}", fh)
        log_print(f"    - CSV Approach: {csv_approach}", fh)
        log_print(f"    - SQL Approach: {sql_approach}", fh)
        log_print(f"    - Evaluation:   {verdict}\n", fh)


def task_a2_cleaning_design(fh):
    log_print("=" * 86, fh)
    log_print("TASK A2: DESIGN THE CLEANING AND NORMALISATION", fh)
    log_print("=" * 86, fh)

    rules = [
        ("Missing Values (PM2.5, PM10, NO2)", "If isolated (gap <= 2 hrs), apply Linear Forward Fill (LOCF); if gap > 2 hrs, impute with station diurnal median for that hour; drop if entire day missing.", "Preserves diurnal continuity without distorting variance or peak rush-hour signals."),
        ("Impossible Values (< 0 or > 999)", "Mark as NULL / invalid. Impute using median of preceding and succeeding valid readings if isolated; otherwise treat as missing.", "Eliminates extreme ADC spikes and negative sensor drift while preventing catastrophic mean distortion."),
        ("Duplicate Telemetry Rows", "Retain the first valid transmission record matching (station_id, reading_date, hour); discard subsequent duplicates.", "Prevents double-counting in daily averages caused by automatic cellular re-transmissions."),
        ("Fahrenheit Temperature Readings", "Detect if station is in {'Guindy_F', 'Marina_F'} or if temp > 50°C: convert via C = (F - 32) * 5 / 9.", "Standardizes ambient thermal measurements to Celsius across all 12 monitoring stations.")
    ]
    log_print("A2.1 — Formal Cleaning Rules & Justifications:", fh)
    for rule, action, just in rules:
        log_print(f"  • {rule}:", fh)
        log_print(f"    - Action:        {action}", fh)
        log_print(f"    - Justification: {just}\n", fh)

    log_print("A2.2 — Normalisation Design:", fh)
    log_print("  1. Min-Max Normalisation: x' = (x - x_min) / (x_max - x_min)", fh)
    log_print("     - Scales readings into bounded [0, 1] range.", fh)
    log_print("     - Best suited for visual heatmaps, neural network inputs, and bounded air-quality index scales.", fh)
    log_print("  2. Z-Score Standardisation: z = (x - µ) / σ", fh)
    log_print("     - Centers distribution at mean=0 with unit variance=1.", fh)
    log_print("     - Best suited for statistical anomaly detection, outlier z-score thresholds (|z| > 3), and multi-station regression modeling.", fh)

    log_print("\nA2.3 — Canonical Data Formatting Standards:", fh)
    log_print("  • Dates:    ISO-8601 string format 'YYYY-MM-DD' (e.g. '2026-10-15').", fh)
    log_print("  • Hours:    Integer in range [0, 23].", fh)
    log_print("  • Stations: Canonical Title Case string (e.g. 'Adyar', 'Guindy', 'Anna Nagar').", fh)
    log_print("  • Numbers:  IEEE 754 64-bit floating point rounded to 2 decimal places for reporting.", fh)


def task_a3_visualisation_design(fh):
    log_print("\n" + "=" * 86, fh)
    log_print("TASK A3: DESIGN THE ANALYSIS AND VISUALISATION", fh)
    log_print("=" * 86, fh)

    charts = [
        ("Trend of PM2.5 over a Month", "Time-Series Line Chart with 7-Day Moving Average", "Continuous line shows day-to-day fluctuations, seasonal weather shifts, and high-pollution episodes over time."),
        ("Comparison Across 12 Stations", "Station Box Plot (Five-Number Summary + Outliers)", "Directly visualizes median, interquartile range (IQR), variance spread, and extreme spikes across all 12 monitoring stations."),
        ("Temperature vs PM2.5 Relationship", "Bivariate Scatter Plot with Polynomial / Linear Trendline", "Reveals correlation and meteorological phenomena such as thermal inversion (low winter temperatures trapping surface particulate matter)."),
        ("Hours with Worst Air Quality", "24-Hour Diurnal Bar Chart / Area Chart with Peak Rush Hour Shading", "Identifies diurnal peaks during morning (08:00–10:00) and evening (18:00–21:00) vehicular congestion windows.")
    ]
    log_print("A3.1 — Justified Chart Selections for Board Inquiries:", fh)
    for q, chart, just in charts:
        log_print(f"  • {q}:", fh)
        log_print(f"    - Selected Chart: {chart}", fh)
        log_print(f"    - Justification:  {just}\n", fh)

    log_print("A3.2 — Daily Station Summary Table Schema:", fh)
    log_print("  Columns: [station_id, reading_date, valid_hours, min_pm25, max_pm25, mean_pm25, std_pm25, aq_category]", fh)
    log_print("  Production: Generated via single SQL aggregate query: SELECT station_id, reading_date, COUNT(pm25), MIN(pm25), MAX(pm25), AVG(pm25) GROUP BY station_id, reading_date.", fh)


def task_a4_debugging_profiling_plan(fh):
    log_print("\n" + "=" * 86, fh)
    log_print("TASK A4: PLAN DEBUGGING AND PROFILING", fh)
    log_print("=" * 86, fh)

    log_print("A4.1 — Hierarchical Debugging Strategy:", fh)
    log_print("  1. Print Statements: Fast initial sanity checking during pipeline prototyping.", fh)
    log_print("  2. Assert Statements: Enforce data invariants at module boundaries (e.g. assert 0.0 <= minmax <= 1.0).", fh)
    log_print("  3. Logging Module: Production-grade logging with levels (DEBUG, INFO, WARNING, ERROR). Easily toggled via logger.setLevel(logging.WARNING).", fh)
    log_print("  4. PDB Debugger: Interactive breakpoint inspection (breakpoint(), pdb.set_trace()) to inspect runtime frame locals upon unexpected data anomalies.", fh)

    log_print("\nA4.2 — Profiling Plan & Performance Instrumentation:", fh)
    log_print("  1. time.perf_counter(): High-precision elapsed time tracking for macroscopic pipeline stages.", fh)
    log_print("  2. timeit Module: Micro-benchmarking specific algorithms (e.g. string splitting vs csv.reader vs regex parsing).", fh)
    log_print("  3. cProfile: Statistical profiling of call counts and cumulative execution time (tottime/cumtime) to identify CPU bottlenecks.", fh)


def task_a5_ai_applications_design(fh):
    log_print("\n" + "=" * 86, fh)
    log_print("TASK A5: DESIGN AN AI APPLICATION FOR CITIZEN COMPLAINTS", fh)
    log_print("=" * 86, fh)

    log_print("A5.1 — Citizen Complaint Sentiment Scorer & Extractive Summarizer:", fh)
    log_print("  • Lexicon Sentiment Scorer: Maintains POSITIVE, NEGATIVE, and NEGATOR sets.", fh)
    log_print("    Algorithm: Tokenizes text into lowercase tokens; maintains state flag 'negate'. If previous word is in NEGATORS, flips the sign of next sentiment word.", fh)
    log_print("  • Extractive Summarizer: Frequencies of non-stopwords are computed.", fh)
    log_print("    Sentences are ranked by sum of constituent word frequencies. The top-k sentences with highest density of thematic keywords are extracted.", fh)

    log_print("\nA5.2 — Rule-Based Keyword Chatbot & Architectural Limitations:", fh)
    log_print("  • Architecture: Regex/Keyword matching state machine extracting: (1) metric (PM2.5, temperature), (2) station name, (3) temporal keyword (today, yesterday, month).", fh)
    log_print("    Executes parameterized SQL query and constructs natural language response.", fh)
    log_print("  • Critical Limitations:", fh)
    log_print("    1. Brittle to typos, colloquialisms, and regional spelling variants ('Adayar' vs 'Adyar').", fh)
    log_print("    2. Cannot handle multi-turn conversational context or follow-up questions.", fh)
    log_print("    3. Complete failure on out-of-domain queries or compound intent questions.", fh)


def verify_simats_pseudocode_spec(fh):
    log_print("\n" + "=" * 86, fh)
    log_print("SIMATS ENGINEERING STANDARD ALGORITHMIC PSEUDOCODE SPECIFICATION", fh)
    log_print("=" * 86, fh)
    pseudo = """ALGORITHM CleanAndIngestAirQualityData(csvFileList, dbConnection)
// Standard: SIMATS Engineering Algorithmic Standard
BEGIN
    DECLARE rawBuffer AS LIST OF RECORD
    DECLARE cleanBuffer AS LIST OF RECORD
    DECLARE validMinMax AS RECORD(minVal: REAL, maxVal: REAL)

    FOR EACH csvFile IN csvFileList DO
        OPEN csvFile IN READ MODE WITH ENCODING "utf-8" AS stream
            DECLARE reader AS CSV_DICT_READER = InitializeReader(stream)
            FOR EACH row IN reader DO
                DECLARE station AS STRING = Trim(row["station"])
                DECLARE readingDate AS STRING = Trim(row["date"])
                DECLARE hour AS INTEGER = ToInteger(row["hour"])
                DECLARE rawPM25 AS STRING = Trim(row["pm25"])
                DECLARE rawTemp AS STRING = Trim(row["temperature"])

                // Anomaly Filter: Missing and Impossible values
                IF rawPM25 = "" OR rawPM25 = "NA" THEN CONTINUE END IF
                DECLARE pm25 AS REAL = ToFloat(rawPM25)
                IF pm25 < 0.0 OR pm25 > 999.0 THEN CONTINUE END IF

                // Unit Standardization: Fahrenheit to Celsius
                DECLARE temp AS REAL = ToFloat(rawTemp)
                IF station ENDS WITH "_F" OR temp > 50.0 THEN
                    temp <- (temp - 32.0) * (5.0 / 9.0)
                END IF

                APPEND RECORD(station, readingDate, hour, pm25, temp) TO cleanBuffer
            END FOR
        CLOSE stream
    END FOR

    // Calculate Normalisation Bounds
    DECLARE minPM25 AS REAL = ComputeMin(cleanBuffer, "pm25")
    DECLARE maxPM25 AS REAL = ComputeMax(cleanBuffer, "pm25")
    DECLARE meanPM25 AS REAL = ComputeMean(cleanBuffer, "pm25")
    DECLARE stdPM25 AS REAL = ComputeStdDev(cleanBuffer, "pm25")

    // Batch Database Insertion with Parameterized SQL
    BEGIN TRANSACTION
        FOR EACH rec IN cleanBuffer DO
            DECLARE normMinMax AS REAL = (rec.pm25 - minPM25) / (maxPM25 - minPM25)
            DECLARE normZScore AS REAL = (rec.pm25 - meanPM25) / stdPM25
            EXECUTE SQL "INSERT OR REPLACE INTO readings VALUES (?, ?, ?, ?, ?, ?, ?)" 
                    WITH (rec.station, rec.readingDate, rec.hour, rec.pm25, rec.temp, normMinMax, normZScore)
        END FOR
    COMMIT TRANSACTION
END ALGORITHM"""
    log_print(pseudo, fh)
    log_print("=" * 86, fh)


def main():
    with open(OUTPUT_TXT, "w", encoding="utf-8") as fh:
        task_a1_acquisition_design(fh)
        task_a2_cleaning_design(fh)
        task_a3_visualisation_design(fh)
        task_a4_debugging_profiling_plan(fh)
        task_a5_ai_applications_design(fh)
        verify_simats_pseudocode_spec(fh)

    from render_screenshot_helper import render_terminal_screenshot
    render_terminal_screenshot(
        OUTPUT_TXT,
        OUTPUT_PNG,
        title="PART A: DATA ACQUISITION, CLEANING, ANALYSIS & AI DESIGN SPEC",
        prompt_cmd="python task_a_design_spec.py",
        max_lines=46
    )
    print(f"[DONE] Part A design specification written to {OUTPUT_TXT} and {OUTPUT_PNG}")


if __name__ == "__main__":
    main()
