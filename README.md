# Student Attendance Tracker & Recovery Report

A Python-based attendance tracking tool that helps university students monitor attendance across multiple subjects, identify shortages, calculate recovery requirements, and estimate how many upcoming classes they can safely miss while maintaining the required attendance percentage.

Developed as a university group assignment using Python.

## Features

- **Subject-wise Attendance Tracking:** Calculate attendance percentages for multiple subjects in a single session.
- **Shortage Detection:** Identify subjects that fall below the default target attendance threshold of 75%.
- **Recovery Planning:** Calculate the minimum number of consecutive classes that must be attended to reach the target percentage.
- **Safe-Skip Estimation:** Estimate how many upcoming classes can be missed without falling below the target.
- **Overall Attendance Analysis:** Calculate weighted overall attendance and generate recovery and safe-skip recommendations while accounting for subject-wise requirements.
- **Terminal Attendance Chart:** Display progress bars for each subject and overall attendance, with a marker indicating the target percentage.
- **Colour-Coded Feedback:** Use red, yellow, and green terminal colours to distinguish attendance levels when the output is displayed in a compatible terminal.
- **Input Validation:** Reject invalid numbers, negative class counts, empty subject names, and attendance counts exceeding the number of classes conducted.
- **Summary Report:** Display attendance percentages, shortage alerts, recovery recommendations, and summary metrics.

## Technologies Used

- **Language:** Python 3
- **Standard Libraries:** `math`, `os`, `sys`
- **Interface:** Command-line interface (CLI)

The project uses Python's standard library and does not require external packages.

## Getting Started

### Prerequisites

- Python 3 installed on your computer.
- A terminal or command prompt.

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/Kaushik-Daksh/Attendance-Tracker.git
```

**2. Navigate to the project directory**

```bash
cd Attendance-Tracker
```

**3. Run the application**

```bash
python attendance_tracker.py
```

If `python` does not work on Windows, try:

```bash
py attendance_tracker.py
```

## How to Use

1. Run the Python program.
2. Enter the name of a subject.
3. Enter the total number of classes conducted for that subject.
4. Enter the number of classes attended.
5. Choose whether to add another subject.
6. Repeat the process for each subject you want to track.
7. Review the subject-wise attendance report, overall attendance summary, and terminal chart.

## How It Works

### 1. Attendance Percentage

For each subject, attendance is calculated using:

\[
\text{Attendance \%} =
\frac{\text{Classes Attended}}{\text{Classes Conducted}}
\times 100
\]

If no classes have been conducted, the program reports `NO DATA` and displays an attendance percentage of 0%.

### 2. Recovery Calculation

If attendance is below the target, the program calculates the smallest number of consecutive classes that must be attended to reach the target percentage.

### 3. Safe-Skip Calculation

If attendance meets or exceeds the target, the program estimates the maximum number of upcoming classes that can be missed before attendance falls below the target.

### 4. Overall Attendance

The overall attendance percentage is calculated using the total number of classes attended divided by the total number of classes conducted across all subjects.

The overall recovery recommendation accounts for every subject that is below the target. When all subjects meet the target, the overall safe-skip recommendation is limited by both the individual subject limits and the overall attendance limit.

## Project Structure

```text
Attendance-Tracker/
├── attendance_tracker.py
└── README.md
```

## Input Validation

The application checks that:

- Subject names are not empty.
- Class counts are valid non-negative integers.
- Attended classes do not exceed the number of classes conducted.
- The target attendance percentage used by the calculation functions is between 0% and 100%, exclusive.

## Scope and Limitations

- Attendance data is entered manually.
- Data is not saved between program executions.
- The default target attendance percentage is set to 75%.
- The terminal chart uses colour only when the output is connected to a terminal that supports it.
- Attendance recommendations are mathematical estimates and assume the entered class counts are accurate.
- Official university attendance records and attendance policies take precedence over the application's recommendations.

## Learning Outcomes

This project demonstrates practical applications of:

- Python functions and modular programming.
- Conditional statements and loops.
- Input validation and exception handling.
- Mathematical calculations using the `math` module.
- Lists and dictionaries for managing subject data.
- Formatted terminal output and basic text-based data visualization.
- Git and GitHub for collaborative project development.

## Academic Context

Developed as a university group assignment to apply Python programming concepts to a practical student problem: monitoring attendance and planning how to meet minimum attendance requirements.

## Contributors

- Daksh Kaushik
- Kushagra Garg
- Nidhi Goyal
- Vanshika Gupta
- Gauri Sharma
