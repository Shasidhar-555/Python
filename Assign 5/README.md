PYTHON PROGRAMMING (CSA08) – ASSIGNMENT 5 (CO5)

Data Acquisition, Cleaning, Analysis and AI Applications

Student Details

Student Name: SHASIDHAR R

Register Number: 192524276

Institution: SIMATS Engineering, Saveetha Institute of Medical and Technical Sciences

Course Code: CSA08 / CSA0807

Course Name: Python Programming

Course Outcome: CO5 – Develop Python programs using libraries and tools to acquire, clean, visualise and analyse data from sources such as CSV files and SQL databases.

Nature of Assignment: Individual

Total Marks: 50 Marks (Part A: 25 Marks, Part B: 25 Marks)

Submission Date: 22/11/2026

1\. Introduction



This assignment focuses on data acquisition, data cleaning, data analysis, visualisation, database operations, and AI applications using Python.



The main objective is to develop practical Python programs that can acquire data from different sources, identify and handle corrupted records, clean and normalise datasets, store information in SQL databases, perform analytical operations, and apply basic AI and Natural Language Processing techniques.



The assignment is divided into Part A and Part B, covering four implementation tasks under Part B.



2\. Environment and Dependencies

Component	Details

Programming Language	Python

Python Version	3.14.3

Operating System	Windows 11 (64-bit)

Database	SQLite

Data Processing	Pandas, NumPy

Data Visualisation	Matplotlib

File Handling	CSV and text files

Statistical Analysis	Statistics

Text Processing	Regular Expressions and NLP

Documentation	Markdown and python-docx

Required Libraries

pandas

numpy

matplotlib

Pillow

python-docx

Installation



Install the required dependencies using:



bash

pip install -r requirements.txt



3\. Assignment Structure



The assignment consists of the following sections:



Part A: Data and Program Design – 25 Marks

Part B1: Implement and Validate Cleaning Pipeline – 7 Marks

Part B2: Engineer Adversarial Data – 5 Marks

Part B3: Loops vs Libraries vs SQL Benchmarks – 8 Marks

Part B4: Final Production Engineering Decision – 5 Marks

4\. Part A – Data and Program Design



Directory: TaskA\_Design/



Main Python File: task\_a\_design\_spec.py



This task focuses on designing a complete data-processing system before implementation.



Key activities:



Designed a data acquisition and processing workflow.

Prepared formal program design specifications.

Developed SIMATS algorithmic pseudocode.

Defined data cleaning and validation rules.

Designed data storage using SQLite.

Planned data visualisation and analysis.

Designed AI-based sentiment analysis and text summarisation approaches.

Documented the complete processing architecture.



Generated Files:



task\_a\_design\_spec.py

output.txt

output\_screenshot.png

5\. Part B – Implementation and Analysis

B1 – Implement and Validate Cleaning Pipeline



Directory: TaskB1\_Cleaning\_Pipeline/



Main Python File: task\_b1\_pipeline.py



This task implements a complete data cleaning pipeline using Python libraries and SQLite.



Key activities:



Loaded raw air quality sensor readings from CSV files.

Identified missing, invalid, and inconsistent values.

Cleaned and validated sensor readings.

Applied data normalisation techniques.

Stored cleaned records in SQLite using executemany().

Executed SQL queries for data analysis.

Generated four-panel data visualisations.

Compared Min-Max and Z-score normalisation.



Generated Files:



raw\_sensor\_readings.csv

cleaned\_readings.csv

air\_quality.db

output.txt

output\_screenshot.png

B2 – Engineer Adversarial Data



Directory: TaskB2\_Adversarial\_Data/



Main Python File: task\_b2\_adversarial.py



This task evaluates the reliability of the data-processing pipeline using deliberately corrupted and unusual input data.



Key activities:



Tested CSV files with missing columns.

Tested alternative delimiters such as semicolons.

Tested Latin-1 encoded input files.

Tested empty datasets.

Examined SQL injection risks.

Implemented parameterised SQL queries.

Tested NLP edge cases.

Evaluated the system's ability to handle unexpected input.



Generated Files:



adversarial\_inputs/

output.txt

output\_screenshot.png

B3 – Loops vs Libraries vs SQL Benchmarks



Directory: TaskB3\_Loops\_Libraries\_SQL/



Main Python File: task\_b3\_benchmark.py



This task compares different data-processing approaches using performance benchmarks.



Key activities:



Compared traditional Python loops.

Evaluated Pandas-based data processing.

Compared SQL query performance.

Tested different dataset sizes.

Analysed scaling behaviour across multiple monitoring stations.

Used cProfile for execution profiling.

Identified performance bottlenecks.

Generated benchmark visualisations.



Generated Files:



task\_b3\_benchmark.py

cprofile\_report.txt

output.txt

output\_screenshot.png

B4 – Final Production Engineering Decision



Directory: TaskB4\_Engineering\_Decision/



Main Python File: task\_b4\_production.py



This task focuses on production-oriented data processing and AI applications.



Key activities:



Processed 50 citizen air pollution complaints.

Implemented negation-aware sentiment analysis.

Developed an extractive text summarisation approach.

Evaluated NLP results against human-labelled data.

Created and tested SQLite B-tree indexing.

Compared table scan and indexed query performance.

Generated sentiment evaluation and indexing visualisations.



Generated Files:



citizen\_complaints\_50.txt

task\_b4\_production.py

output.txt

output\_screenshot.png

6\. Project Directory Structure

text

CSA08-192524276-Assignment5/

│

├── TaskA\_Design/

│   ├── task\_a\_design\_spec.py

│   ├── output.txt

│   └── output\_screenshot.png

│

├── TaskB1\_Cleaning\_Pipeline/

│   ├── raw\_sensor\_readings.csv

│   ├── task\_b1\_pipeline.py

│   ├── cleaned\_readings.csv

│   ├── air\_quality.db

│   ├── output.txt

│   └── output\_screenshot.png

│

├── TaskB2\_Adversarial\_Data/

│   ├── task\_b2\_adversarial.py

│   ├── adversarial\_inputs/

│   ├── output.txt

│   └── output\_screenshot.png

│

├── TaskB3\_Loops\_Libraries\_SQL/

│   ├── task\_b3\_benchmark.py

│   ├── cprofile\_report.txt

│   ├── output.txt

│   └── output\_screenshot.png

│

├── TaskB4\_Engineering\_Decision/

│   ├── citizen\_complaints\_50.txt

│   ├── task\_b4\_production.py

│   ├── output.txt

│   └── output\_screenshot.png

│

├── report\_assets/

│   ├── fig1\_b1\_pipeline\_charts.png

│   ├── fig2\_b1\_normalisation.png

│   ├── fig3\_b2\_sql\_injection.png

│   ├── fig4\_b3\_scaling\_benchmark.png

│   ├── fig5\_b3\_cprofile\_flame.png

│   ├── fig6\_b4\_indexing\_speedup.png

│   └── fig7\_b4\_nlp\_evaluation.png

│

├── run\_all\_tasks.py

├── render\_screenshot\_helper.py

├── ASSIGNMENT\_REPORT.md

├── CSA0807\_Assignment5\_192524276\_Report.docx

└── requirements.txt



7\. Progressive Development and Testing



The assignment was organised into progressive development milestones to maintain a structured implementation workflow.



Milestone	Description

Base Setup	Created project structure and installed dependencies

Task A	Completed data acquisition and program design

Task B1	Implemented data cleaning, normalisation, and SQLite storage

Task B2	Tested adversarial datasets and input validation

Task B3	Conducted loops, Pandas, and SQL benchmarks

Task B4	Implemented NLP applications and database indexing

Final Integration	Prepared master test runner and visualisation assets

Final Report	Prepared analytical report in Markdown and Word formats

8\. Execution Instructions

Step 1 – Open the Project Directory

bash

cd CSA08-192524276-Assignment5



Step 2 – Install Dependencies

bash

pip install -r requirements.txt



Step 3 – Execute the Complete Assignment



Run the master program to execute and verify all tasks:



bash

python run\_all\_tasks.py



Individual Task Execution



Part A – Design



bash

python TaskA\_Design/task\_a\_design\_spec.py





B1 – Cleaning Pipeline



bash

python TaskB1\_Cleaning\_Pipeline/task\_b1\_pipeline.py





B2 – Adversarial Data



bash

python TaskB2\_Adversarial\_Data/task\_b2\_adversarial.py





B3 – Performance Benchmarking



bash

python TaskB3\_Loops\_Libraries\_SQL/task\_b3\_benchmark.py





B4 – Production Engineering



bash

python TaskB4\_Engineering\_Decision/task\_b4\_production.py



9\. Key Python Concepts Demonstrated

Concept	Application

Data Acquisition	Reading sensor data from CSV files

Data Cleaning	Handling missing and invalid values

Data Normalisation	Min-Max and Z-score techniques

Pandas	Data manipulation and analysis

NumPy	Numerical operations

SQLite	Database storage and querying

Parameterised SQL	Safer database operations

Data Visualisation	Charts and statistical plots

Statistical Analysis	Data interpretation

Regular Expressions	Text processing

NLP	Sentiment analysis and summarisation

Performance Benchmarking	Comparing processing methods

cProfile	Identifying execution bottlenecks

B-tree Indexing	Improving database query performance

10\. Performance and Analytical Results



The assignment explores the performance and reliability of different data-processing techniques.



Task	Main Focus

A	Complete data acquisition and program design

B1	Cleaning, normalisation, SQLite storage, and visualisation

B2	Adversarial data handling and SQL injection prevention

B3	Loops, Pandas, and SQL performance comparison

B4	NLP evaluation and SQLite indexing



The benchmark results and analytical observations are documented in the respective task output files and final assignment report.



11\. Learning Outcomes



By completing this assignment, I gained practical experience in:



Acquiring data from CSV files.

Cleaning and validating real-world datasets.

Handling missing and corrupted data.

Applying data normalisation techniques.

Storing and retrieving information using SQLite.

Writing efficient SQL queries.

Visualising datasets using Matplotlib.

Analysing data using Pandas and NumPy.

Understanding SQL injection prevention.

Applying basic Natural Language Processing techniques.

Comparing Python loops, libraries, and SQL.

Improving database performance through indexing.

Evaluating data-processing systems using benchmarks.

12\. Conclusion



This assignment provided practical experience in data acquisition, cleaning, analysis, visualisation, database management, and AI applications using Python.



Through Part A and the four implementation tasks in Part B, I explored how raw data can be transformed into meaningful information using Python libraries and database technologies.



The project demonstrates the importance of data quality, efficient processing, secure database operations, visualisation, and performance optimisation in developing reliable data-driven applications.



Submitted By: SHASIDHAR R

Register Number: 192524276

Course: Python Programming (CSA08 / CSA0807)

Assignment: 5 – CO5

Institution: SIMATS Engineering, Saveetha Institute of Medical and Technical Sciences

