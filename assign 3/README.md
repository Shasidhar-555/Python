CSA0807 – Python Programming | Assignment 3 (CO3)



Course Code: CSA0807 – Python Programming

Unit: CO3 – Python Data Structures

Topics Covered: Lists, Tuples, Dictionaries, Sets, Slicing, Mutability, Copying and List Comprehensions

Bloom's Taxonomy: K3 – Apply | K4 – Analyse | K5 – Evaluate



Submitted by: SHASIDHAR R

Register Number: 192524276

Submission Date: 03/11/2026

Python Version: Python 3.14.3 (Compatible with Python 3.10+)

Repository: CSA0807-192524276-Assignment3



📑 Contents

Project Introduction

Folder Structure

Software Requirements and Libraries

How to Run the Programs

Assignment Tasks and Technical Outcomes

Git Version Control and Commit Details

1\. Project Introduction



This repository contains the Python programs developed for Assignment 3 of the CSA0807 Python Programming course.



The assignment focuses on understanding and applying Python's built-in data structures. The seven exercises explore practical situations in which structured data must be stored, accessed, modified, analysed and processed efficiently.



The implementation covers basic operations as well as alternative approaches, performance comparisons, memory considerations and algorithmic improvements.



Each task is organised separately to make the programs easier to understand, execute and maintain.



2\. Repository Folder Structure



The project is organised into individual directories according to the corresponding assignment questions.



text

CSA0807-192524276-Assignment3/

│

├── Q1\_Rainfall\_Analysis/

│   ├── q1\_rainfall.py

│   ├── rainfall\_sample\_365.txt

│   ├── output.txt

│   └── output\_screenshot.png

│

├── Q2\_BusStop\_Grid/

│   ├── q2\_bus\_stops.py

│   ├── bus\_stops\_sample.json

│   ├── output.txt

│   └── output\_screenshot.png

│

├── Q3\_Farmer\_Helpline/

│   ├── q3\_farmer\_helpline.py

│   ├── complaints\_sample.txt

│   ├── output.txt

│   └── output\_screenshot.png

│

├── Q4\_Elective\_Registration/

│   ├── q4\_elective\_registration.py

│   ├── registrations\_sample.json

│   ├── output.txt

│   └── output\_screenshot.png

│

├── Q5\_Sensor\_Cleaning/

│   ├── q5\_sensor\_cleaning.py

│   ├── temperatures\_sample.txt

│   ├── output.txt

│   └── output\_screenshot.png

│

├── Q6\_Railway\_Timetable/

│   ├── q6\_railway\_timetable.py

│   ├── trains\_sample.json

│   ├── output.txt

│   └── output\_screenshot.png

│

├── Q7\_Contact\_Merging/

│   ├── q7\_contact\_merging.py

│   ├── contacts\_raw\_sample.json

│   ├── output.txt

│   └── output\_screenshot.png

│

├── report\_assets/

├── run\_all\_tasks.py

├── requirements.txt

├── .gitignore

├── ASSIGNMENT\_REPORT.md

└── CSA0807\_Assignment3\_192524276\_Report.docx



3\. Software Requirements and Libraries



Programming language: Python

Recommended version: Python 3.10 or above.



The programs primarily use Python's standard library. Depending on the task, the following modules may be required:



Module	Application

sys	Interpreter and recursion information

time	Execution-time measurements

collections	Counter and deque operations

copy	Shallow and deep copying

random	Sample data generation

json	Reading structured datasets

math	Mathematical calculations

re	String-pattern comparison

tracemalloc	Memory usage measurement

functools	Function caching

matplotlib	Graphs and performance charts

Pillow	Image processing

python-docx	Word report generation



Install the external packages, if used, with:



bash

pip install -r requirements.txt





The standard-library modules do not require separate installation.



4\. Program Execution Instructions



Each question has an independent Python file. The programs can be executed separately from the main project directory.



Question	Program	Execution command

Q1	Rainfall analysis	python Q1\_Rainfall\_Analysis/q1\_rainfall.py

Q2	Bus-stop grid	python Q2\_BusStop\_Grid/q2\_bus\_stops.py

Q3	Farmer helpline	python Q3\_Farmer\_Helpline/q3\_farmer\_helpline.py

Q4	Elective registration	python Q4\_Elective\_Registration/q4\_elective\_registration.py

Q5	Sensor data cleaning	python Q5\_Sensor\_Cleaning/q5\_sensor\_cleaning.py

Q6	Railway timetable	python Q6\_Railway\_Timetable/q6\_railway\_timetable.py

Q7	Contact merging	python Q7\_Contact\_Merging/q7\_contact\_merging.py



To execute the complete assignment through the main runner:



bash

python run\_all\_tasks.py





The runner should be used after confirming that all seven task programs and their required input files are present.



5\. Assignment Tasks and Technical Outcomes

Q1 – Rainfall Data Processing (K3 – Apply)



Objective: Process daily rainfall measurements and obtain useful summaries from a year-long dataset.



Concepts used:



List indexing and slicing.

Weekly rainfall calculations.

Moving averages.

Identification of days with no rainfall.

Sliding-window processing with collections.deque.



Technical discussion:



List slicing provides a convenient way to extract weekly records from a larger collection. Moving averages help identify rainfall trends over consecutive days.



An alternative running-sum technique avoids recalculating the complete window at every step. This is useful when processing large collections of rainfall readings.



Q2 – Bus Stop Coordinates and Grid Management (K4 – Analyse)



Objective: Represent bus-stop locations and passenger information using suitable Python data structures.



Concepts used:



Tuples as dictionary keys.

List aliasing.

Shallow and deep copying.

Two-dimensional list creation.

Sparse dictionary representation.



Technical discussion:



Tuples are suitable for representing fixed coordinate pairs. They can be used as dictionary keys when their elements are hashable.



Repeated references to the same inner list can create unexpected changes in a two-dimensional structure. Independent list creation using list comprehension avoids this problem.



For a sparsely occupied grid, a dictionary can store only the positions that contain data, reducing unnecessary storage.



Q3 – Farmer Helpline Complaint Analysis (K4 – Analyse)



Objective: Organise complaint information and identify frequently reported words or issues.



Concepts used:



Dictionary-based frequency counting.

get() and setdefault().

collections.Counter.

District-wise grouping.

Sorting dictionary results.



Technical discussion:



Dictionaries provide an efficient way to maintain counts while processing complaint records.



The get() method allows a default value to be supplied when a key is unavailable. The setdefault() method can initialise missing entries.



The Counter class offers a convenient alternative for frequency analysis and identifying commonly occurring words.



Q4 – Elective Registration and Set Operations (K4 – Analyse)



Objective: Compare student registration lists and identify common or conflicting elective selections.



Concepts used:



Set creation.

Duplicate removal.

Union and intersection.

Difference and symmetric difference.

Membership testing.



Technical discussion:



Sets are useful when the main requirement is to maintain unique student identifiers.



Intersection identifies students common to multiple registration groups, while difference identifies students belonging to one group but not another.



Set operations provide a clear and efficient approach to detecting registration overlaps.



Q5 – Cleaning Sensor Readings (K3 – Apply)



Objective: Filter and process temperature readings collected from a monitoring system.



Concepts used:



List comprehensions.

Conditional filtering.

map() and filter().

Lambda functions.

Generator expressions.



Technical discussion:



List comprehensions combine iteration and conditional selection in a compact expression.



The map() and filter() functions provide alternative ways to transform and select data.



Generator expressions are particularly useful when processing large datasets because they produce values on demand instead of storing the complete result immediately.



Q6 – Railway Timetable Management (K4 – Analyse)



Objective: Store and retrieve train information using nested Python data structures.



Concepts used:



Nested dictionaries.

Lists and tuples.

Lambda expressions.

Multi-level sorting.

Station-based indexing.



Technical discussion:



A nested dictionary can represent train information, including stations, departure times and operating days.



Sorting functions can arrange train records according to departure time or other selected attributes.



An inverted station index provides another approach to retrieving trains associated with a particular station without repeatedly examining every train record.



Q7 – Contact Data Consolidation (K5 – Evaluate)



Objective: Identify duplicate contact records and combine information belonging to the same individual.



Concepts used:



String normalisation.

Duplicate detection.

Dictionary-based indexing.

Graph relationships.

Disjoint Set Union (DSU).



Technical discussion:



Contact records may contain inconsistent formatting, such as differences in telephone number prefixes, spaces and letter casing.



Normalisation helps standardise the records before comparing identifiers.



A Disjoint Set Union structure can group connected records and support transitive merging. This provides an alternative to comparing every contact record against every other record.



The final implementation should also ensure that people with similar names are not incorrectly combined.



6\. Git Version Control and Commit Details



Git version control can be used to maintain the development history of the assignment.



A task-wise commit structure makes it easier to identify when individual programs, datasets, corrections and reports were added.



Suggested commit organisation:



Stage	Commit description

Initial	Create repository and project structure

Task 01	Add rainfall analysis implementation

Task 02	Add bus-stop grid and copying examples

Task 03	Add farmer complaint analysis

Task 04	Add elective registration and set operations

Task 05	Add sensor data cleaning

Task 06	Add railway timetable processing

Task 07	Add contact merging implementation

Outputs	Include datasets and execution evidence

Final	Add consolidated assignment report and runner



The commit history should reflect the changes actually made to the repository.



Conclusion



Assignment 3 provides practical experience with Python's built-in data structures and their applications in different problem-solving situations.



Through these seven exercises, the assignment explores how lists, tuples, dictionaries and sets can be selected and combined according to the requirements of a problem.



The implementations also provide opportunities to examine mutability, copying behaviour, slicing, data organisation and performance.



The overall objective is to develop programs that are readable, logically organised and efficient when processing structured information.



Submitted by: SHASIDHAR R

Register Number: 192524276

Course: CSA0807 – Python Programming

