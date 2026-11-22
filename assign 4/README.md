PYTHON PROGRAMMING (CSA08) – ASSIGNMENT 4 (CO4)

Robust Data Processing with Files, Exceptions, Modules and Packages

Student Details

Student Name: SHASIDHAR R

Register Number: 192524276

Institution: SIMATS Engineering, Saveetha Institute of Medical and Technical Sciences

Course Code: CSA08 / CSA0807

Course Name: Python Programming

Course Outcome: CO4

Submission Date: 15/11/2026

Total Marks: 50 Marks

1\. Introduction



This assignment focuses on the practical implementation of Python programming concepts involving file handling, exception handling, modules, and packages.



The main objective is to develop reliable and efficient Python applications capable of processing data, handling errors, organising code into reusable modules, and generating meaningful reports.



The assignment consists of six tasks covering different aspects of robust data processing and software development.



2\. Environment and Technology Stack

Component	Details

Programming Language	Python

Python Version	3.14.3

Operating System	Windows 11 (64-bit)

File Handling	Text files and CSV files

Exception Handling	Built-in and custom exceptions

Modules	Python modules and imports

Packages	Modular Python packages

Data Processing	Streaming and aggregation

Benchmarking	Time and memory analysis

Visualisation	Matplotlib and NumPy

Required Libraries

matplotlib >= 3.8.0

Pillow >= 10.0.0

python-docx >= 1.1.0

numpy >= 1.26.0



Install the required dependencies using:



bash

pip install -r requirements.txt



3\. Assignment Tasks

Task 01 – File-Processing Design Review



Python File: task1\_mess\_processor.py



Analysed the existing hostel mess bill processing program.

Identified eight architectural deficiencies.

Implemented line-by-line file processing using with open().

Used decimal.Decimal for accurate currency calculations.

Implemented appropriate exception handling.

Conducted a 50,000-line streaming versus buffering benchmark.

Demonstrated approximately 41.8x memory savings.

Task 02 – Requirement to File-Processing Design



Python File: task2\_attendance\_design.py



Designed a biometric attendance processing system.

Developed algorithmic pseudocode and trace tables.

Processed five daily attendance files.

Implemented single-pass attendance accumulation.

Generated attendance summary CSV reports.

Created defaulter reports for attendance below 75%.

Maintained separate logs for damaged records.

Demonstrated O(F × L) processing complexity.

Task 03 – Design the Error Handling



Python File: task3\_exceptions.py



Developed a custom InvalidRecord exception.

Implemented an exception hierarchy.

Completed parse\_line() and summarise() functions.

Handled invalid and malformed attendance records.

Demonstrated the disadvantages of bare except: pass.

Verified the expected program output.

Task 04 – File and Exception Forensics



Python File: task4\_library\_forensics.py



Analysed defects in library return record processing.

Identified data loss caused by write mode ("w").

Repaired file handling using append mode ("a").

Implemented context managers for resource management.

Added newline delimiters to maintain record separation.

Implemented timestamped error logging.

Created a three-day automated testing process.

Task 05 – The Same Utility Organised Four Ways



Python File: task5\_compare\_runner.py



Implemented four different Python program organisation approaches:



Monolithic single-script architecture.

Single-module architecture.

Multiple flat-module architecture.

Python package architecture.



Additional features:



Compared code organisation and maintainability.

Implemented a three-consecutive-absence requirement.

Analysed the impact of changes across architectures.

Demonstrated Python import behaviour.

Compared cold imports and cached imports using sys.modules.

Task 06 – Design Challenge: College Fest Registration Desk



Python File: task6\_fest\_desk.py



Developed a modular Python package named fest\_registration.



Package components:



validator.py – Email validation using string methods.

parser.py – Fault-tolerant streaming record parser.

aggregator.py – Set-based duplicate detection and event routing.

reporter.py – CSV reports, event rosters, and error logs.

\_\_init\_\_.py – Package metadata and public exports.



Additional features:



Processes multiple department input files.

Handles missing files and corrupted records.

Prevents duplicate registrations.

Generates individual event rosters.

Creates a master registration CSV.

Generates a fest summary report.

Maintains processing error logs.

Demonstrates O(N) set-based deduplication.

4\. Project Directory Structure

text

CSA08-192524276-Assignment4/

│

├── Task01\_File\_Processing\_Review/

│   ├── task1\_mess\_processor.py

│   ├── output.txt

│   └── output\_screenshot.png

│

├── Task02\_Requirement\_To\_Design/

│   ├── task2\_attendance\_design.py

│   ├── data/

│   ├── attendance\_summary.csv

│   ├── defaulters\_below\_75.txt

│   ├── damaged\_records.log

│   ├── output.txt

│   └── output\_screenshot.png

│

├── Task03\_Design\_Error\_Handling/

│   ├── task3\_exceptions.py

│   ├── output.txt

│   └── output\_screenshot.png

│

├── Task04\_Forensics\_And\_Repair/

│   ├── task4\_library\_forensics.py

│   ├── library\_returns.txt

│   ├── library\_errors.log

│   ├── output.txt

│   └── output\_screenshot.png

│

├── Task05\_Four\_Organisations/

│   ├── sample\_data/

│   ├── org\_a\_single\_script/

│   ├── org\_b\_module\_import/

│   ├── org\_c\_multi\_module/

│   ├── org\_d\_python\_package/

│   ├── task5\_compare\_runner.py

│   ├── output.txt

│   └── output\_screenshot.png

│

├── Task06\_Design\_Challenge/

│   ├── department\_inputs/

│   ├── fest\_registration/

│   ├── outputs/

│   ├── task6\_fest\_desk.py

│   ├── output.txt

│   └── output\_screenshot.png

│

├── report\_assets/

│   ├── fig1\_q1\_memory\_scaling.png

│   ├── fig2\_q2\_pass\_complexity.png

│   ├── fig3\_q3\_eafp\_vs\_lbyl.png

│   ├── fig4\_q4\_descriptor\_leakage.png

│   ├── fig5\_q5\_organisations\_evaluation.png

│   └── fig6\_q6\_deduplication\_scaling.png

│

├── run\_all\_tasks.py

├── render\_screenshot\_helper.py

├── ASSIGNMENT\_REPORT.md

├── CSA0807\_Assignment4\_192524276\_Report.docx

├── requirements.txt

└── README.md



5\. Execution Instructions

Step 1 – Open the Project Directory

bash

cd CSA08-192524276-Assignment4



Step 2 – Install Dependencies

bash

pip install -r requirements.txt



Step 3 – Execute All Six Tasks

bash

python run\_all\_tasks.py



Individual Task Execution



Task 1



bash

python Task01\_File\_Processing\_Review/task1\_mess\_processor.py





Task 2



bash

python Task02\_Requirement\_To\_Design/task2\_attendance\_design.py





Task 3



bash

python Task03\_Design\_Error\_Handling/task3\_exceptions.py





Task 4



bash

python Task04\_Forensics\_And\_Repair/task4\_library\_forensics.py





Task 5



bash

python Task05\_Four\_Organisations/task5\_compare\_runner.py





Task 6



bash

python Task06\_Design\_Challenge/task6\_fest\_desk.py



6\. Key Concepts Demonstrated

Concept	Application

File Handling	Reading, writing, and appending files

Context Managers	Safe file resource management

Exception Handling	Built-in and custom exceptions

Data Validation	Identifying malformed records

Decimal Arithmetic	Accurate financial calculations

CSV Processing	Structured data reporting

Streaming	Memory-efficient file processing

Modules	Code separation and reusability

Packages	Structured application architecture

Sets	Efficient duplicate detection

Import System	Module loading and caching

Benchmarking	Performance and memory comparison

7\. Performance Analysis



The assignment demonstrates the importance of selecting appropriate data structures and file-processing techniques.



Experiment	Result

Task 1 – Memory Benchmark	Approximately 41.8x memory savings

Task 2 – Attendance Processing	Single-pass O(F × L) processing

Task 4 – File Repair	Append mode preserves existing records

Task 5 – Import Benchmark	Demonstrates Python module caching

Task 6 – Deduplication	Set-based O(N) approach outperforms list-based O(N²)

8\. Testing and Verification



All six tasks include execution logs and terminal screenshots.



The complete assignment can be tested using:



bash

python run\_all\_tasks.py





The generated output files, reports, and screenshots are organised within their respective task directories.



9\. Learning Outcomes



By completing this assignment, I gained practical knowledge of:



Handling files efficiently using Python.

Implementing exception-handling techniques.

Creating custom exception classes.

Processing large datasets using streaming.

Developing reusable Python modules.

Organising applications using packages.

Generating CSV and text-based reports.

Improving program reliability and maintainability.

Understanding time and space complexity.

Performing performance benchmarking.

10\. Conclusion



This assignment provided practical experience in developing robust Python applications using file handling, exception handling, modules, and packages.



Through six different tasks, I explored efficient data processing, error detection, resource management, modular programming, and performance optimisation.



The completed work demonstrates how Python programming concepts can be applied to develop reliable, reusable, and maintainable real-world applications.



Submitted By: SHASIDHAR R

Register Number: 192524276

Course: Python Programming (CSA08 / CSA0807)

Assignment: 4 – CO4

Institution: SIMATS Engineering, Saveetha Institute of Medical and Technical Sciences

