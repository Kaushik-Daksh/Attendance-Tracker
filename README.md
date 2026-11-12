# Student Attendance Tracker & Recovery Report

A Python-based attendance tracking tool that helps university students monitor attendance across multiple subjects, identify shortages, calculate recovery requirements, and estimate how many upcoming classes they can safely miss while maintaining the required attendance percentage.

Developed as a university group assignment using Python.

## Features

- **Subject Presets or Custom Subjects:** Choose a ready-made subject list (B.Tech CSE, B.Tech ECE, Law) or enter your own subjects one at a time.
- **Subject-wise Attendance Tracking:** Calculate attendance percentages for multiple subjects in a single session.
- **Shortage Detection:** Identify subjects that fall below the target attendance threshold (default 75%).
- **Recovery Planning:** Calculate the minimum number of consecutive classes that must be attended to reach the target percentage.
- **Safe-Skip Estimation:** Estimate how many upcoming classes can be missed without falling below the target.
- **Overall Attendance Analysis:** Calculate overall attendance across all subjects, with a combined recovery or safe-skip recommendation built from the subject-wise results.
- **Terminal Attendance Chart:** Display a progress bar for each subject and for overall attendance, with a `^` marker showing the target percentage.
- **Colour-Coded Feedback:** Bars are red below the target, yellow from the target up to 5 points above it, and green beyond that.
- **Input Validation:** Reject invalid numbers, negative class counts, empty subject names, and attendance counts exceeding the number of classes conducted.
- **Summary Report:** Display attendance percentages, shortage alerts, recovery recommendations, and summary metrics.

## Technologies Used

- **Language:** Python 3
- **Standard Library:** `math`
- **Interface:** Command-line interface (CLI)

The project uses only Python's standard library and does not require external packages.

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
2. Choose an option from the numbered list:
   - **Presets** (e.g. B.Tech CSE) load a fixed set of subjects. You are then asked for the classes conducted and classes attended for each one.
   - **Custom** lets you enter your own subjects.
3. For custom mode, enter a subject name, the total classes conducted, and the classes attended, then choose whether to add another subject (`y` to continue, anything else to finish).
4. Review the subject-wise attendance report, overall attendance summary, and terminal chart.

### Available Presets

| Preset | Subjects |
| --- | --- |
| B.Tech CSE | Calculus, Digital Design, Web Development, Python, Environmental Science |
| B.Tech ECE | ECE Sub 1 – ECE Sub 5 (placeholder names) |
| Law | Law Sub 1 – Law Sub 5 (placeholder names) |

Presets can be changed by editing the `PRESETS` dictionary in `attendance_tracker.py`.

## How It Works

### 1. Attendance Percentage

For each subject, attendance is calculated using:

$$
\text{Attendance \%} = \frac{\text{Classes Attended}}{\text{Classes Conducted}} \times 100
$$

If no classes have been conducted, the program reports `NO DATA` and displays an attendance percentage of 0%.

### 2. Recovery Calculation

If attendance is below the target, the program calculates the smallest number of consecutive classes ($x$) that must be attended to reach the target percentage $p$:

$$
\frac{a + x}{c + x} \geq \frac{p}{100}
$$

where $a$ is classes attended and $c$ is classes conducted.

### 3. Safe-Skip Calculation

If attendance meets or exceeds the target, the program estimates the maximum number of upcoming classes ($x$) that can be missed before attendance falls below the target:

$$
\frac{a}{c + x} \geq \frac{p}{100}
$$

If the result is 0, the subject is on the margin and no upcoming classes should be missed.

### 4. Overall Attendance

The overall attendance percentage is the total classes attended divided by the total classes conducted across all subjects.

The overall recommendation is built from the subject-wise results:

- **If any subject is below the target**, overall status is `SHORTAGE ALERT`. The required classes shown are the **sum** of the recovery requirements of every short subject, with a per-subject breakdown.
- **If every subject meets the target**, overall status is `SAFE`. The safe skips shown are the **sum** of each subject's own safe-skip limit. This is a conservative figure, since each subject stays at or above the target individually.

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
- The preset selection is a valid number from the list.

The target percentage is a constant (`TARGET_PERCENTAGE`) and must stay strictly between 0 and 100. A value of 100 causes a divide-by-zero error in the recovery calculation, and the program does not check this at runtime.

## Scope and Limitations

- Attendance data is entered manually.
- Data is not saved between program executions.
- The target attendance percentage is fixed at 75% and is changed by editing `TARGET_PERCENTAGE` in the code.
- Colours use ANSI escape codes and are always printed. Terminals that do not support them may show stray characters instead of colours.
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