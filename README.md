# Student Attendance Tracker & Recovery Report

A Python-based university group project that helps students monitor subject-wise attendance, identify attendance shortages, and calculate the classes required to reach a 75% attendance threshold.

## Project Overview

The Student Attendance Tracker is a command-line application developed as part of a university group assignment. It accepts attendance data for multiple subjects and generates a structured report containing attendance percentages, shortage alerts, recovery requirements, and estimated safe skips.

## Features

- **Attendance Calculation:** Computes attendance percentages for each subject.
- **Shortage Detection:** Identifies subjects below the 75% attendance threshold.
- **Recovery Planning:** Calculates how many consecutive classes must be attended to reach the threshold.
- **Safe Skip Estimation:** Calculates how many upcoming classes can be missed while maintaining the threshold.
- **Input Validation:** Handles invalid inputs, negative class counts, and attendance exceeding classes conducted.
- **Summary Report:** Displays subject-wise attendance metrics and an overall shortage summary.
- **Multi-Subject Tracking:** Allows users to enter information for multiple subjects in one session.

## Technologies Used

- **Language:** Python 3
- **Standard Library:** `math`
- **Interface:** Command-line interface (CLI)

## Getting Started

### Prerequisites

Install Python 3. No external packages are required.

### Installation

Clone the repository:

```bash
git clone https://github.com/Kaushik-Daksh/Attendance-Tracker.git
```

Navigate to the project directory:

```bash
cd Attendance-Tracker
```

Run the application:

```bash
python attendance_tracker.py
```

## How It Works

1. Enter a subject name.
2. Enter the number of classes conducted.
3. Enter the number of classes attended.
4. Add more subjects if needed.
5. Review the generated attendance report.

## Project Structure

```text
Attendance-Tracker/
├── attendance_tracker.py
└── README.md
```

## Scope and Limitations

- Attendance information is entered manually.
- Data is not saved between program executions.
- The tool is intended to assist with attendance planning; official university attendance records and policies take precedence.

## Academic Context

Developed as a university group assignment to apply Python programming concepts, including functions, conditional logic, loops, input validation, mathematical calculations, and formatted output.

## Contributors
- Daksh Kaushik 
- Kushagra Garg
- Nidhi Goyal
- Vanshika Gupta
- Gauri Sharma 