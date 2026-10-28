# Student Attendance Tracker & Recovery Report

A Python-based attendance tracking tool that helps university students monitor subject-wise attendance, identify shortages, calculate recovery requirements, and estimate how many upcoming classes they can safely miss while maintaining the required attendance percentage.

Developed as a university group assignment using Python.

## Features

- **Subject-wise Attendance Tracking:** Calculate attendance percentages for multiple subjects in a single session.
- **Shortage Detection:** Identify subjects that fall below the target attendance threshold of 75%.
- **Recovery Planning:** Calculate the number of consecutive classes that must be attended to reach the target.
- **Safe Skip Estimation:** Estimate how many upcoming classes can be missed without falling below the required threshold.
- **Overall Attendance Analysis:** Calculate weighted overall attendance and generate an overall recovery plan.
- **Terminal Attendance Chart:** Display visual progress bars for each subject and overall attendance, with a marker showing the target percentage.
- **Optional Graphical Report:** Generate a Matplotlib bar chart comparing subject-wise attendance against the target.
- **Color-Coded Feedback:** Use terminal colors to distinguish attendance levels in the text chart.
- **Input Validation:** Reject invalid numbers, negative class counts, empty subject names, and attendance counts exceeding classes conducted.
- **Summary Report:** Display attendance percentages, shortage alerts, recovery recommendations, and summary metrics.

## Technologies Used

- **Language:** Python 3
- **Standard Libraries:** `math`, `os`, `sys`
- **Optional Library:** `matplotlib` for graphical charts
- **Interface:** Command-line interface (CLI)

## Getting Started

### Prerequisites

- Python 3 installed on your computer.
- A terminal or command prompt.

Matplotlib is optional. The tracker works without it and will still display the terminal report and text-based attendance chart.

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

### Optional: Enable Graphical Charts

Install Matplotlib using:

```bash
python -m pip install matplotlib
```

If Matplotlib is installed, the program can display a graphical attendance chart when prompted. Otherwise, the program skips the graphical chart and continues normally.

## How to Use

1. Run the Python program.
2. Enter the name of a subject.
3. Enter the total number of classes conducted.
4. Enter the number of classes attended.
5. Choose whether to add another subject.
6. Review the generated attendance report and terminal chart.
7. Choose whether to open the optional graphical chart.

The program then calculates subject-wise attendance, identifies shortages, and provides recommendations based on the target attendance percentage.

## How It Works

### 1. Attendance Percentage

The attendance percentage is calculated using:

\[
\text{Attendance \%} =
\frac{\text{Classes Attended}}{\text{Classes Conducted}}
\times 100
\]

### 2. Recovery Calculation

If attendance is below the target, the program calculates the minimum number of consecutive classes that must be attended to reach the required percentage.

### 3. Safe Skip Calculation

If attendance meets or exceeds the target, the program estimates the maximum number of upcoming classes that can be missed before attendance falls below the threshold.

### 4. Overall Attendance

The overall percentage is calculated using total classes attended divided by total classes conducted across all subjects. Recovery and safe-skip recommendations also account for individual subject requirements.

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
- Attended classes do not exceed classes conducted.
- The target attendance percentage is between 0% and 100%, exclusive.

## Scope and Limitations

- Attendance data is entered manually.
- Data is not saved between program executions.
- Graphical charts require the optional Matplotlib dependency.
- Attendance recommendations are mathematical estimates and assume the stated class counts are accurate.
- Official university attendance records and attendance policies take precedence over the application's recommendations.

## Learning Outcomes

This project demonstrates practical applications of:

- Python functions and modular programming.
- Conditional statements and loops.
- Input validation and exception handling.
- Mathematical calculations using `math`.
- Lists and dictionaries for managing subject data.
- Formatted terminal output and basic data visualization.
- Git and GitHub for collaborative project development.

## Academic Context

Developed as a university group assignment to apply Python programming concepts to a practical student problem: monitoring attendance and planning how to meet minimum attendance requirements.

## Contributors

- Daksh Kaushik
- Kushagra Garg
- Nidhi Goyal
- Vanshika Gupta
- Gauri Sharma