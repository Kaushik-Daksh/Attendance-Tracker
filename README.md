# Student Attendance Tracker & Recovery Report

A Python-based attendance tracking tool that helps university students monitor attendance across multiple subjects, identify shortages, calculate recovery requirements, estimate how many upcoming classes they can safely miss, and test "what-if" scenarios while maintaining the required attendance percentage.

Developed as a university group assignment using Python.

## Features

- **Subject Presets or Custom Subjects:** Choose a ready-made subject list (B.Tech CSE, B.Tech ECE, Law) by entering its number, or enter your own subjects one at a time.
- **Subject-wise Attendance Tracking:** Calculate attendance percentages for multiple subjects in a single session.
- **Shortage Detection:** Identify subjects that fall below the target attendance threshold (default 75%).
- **Recovery Planning:** Calculate the minimum number of consecutive classes that must be attended to reach the target percentage.
- **Safe-Skip Estimation:** Estimate how many upcoming classes can be missed without falling below the target.
- **What-If Calculator:** Pick one, several, or all subjects and see how attendance changes if you skip or attend the next N classes, including the effect on overall attendance.
- **Menu-Driven Interface:** After the first report, a menu lets you run the what-if calculator as many times as you like, view the report again, or exit.
- **Overall Attendance Analysis:** Calculate overall attendance across all subjects, with a combined recovery or safe-skip recommendation built from the subject-wise results.
- **Terminal Attendance Chart:** Display a progress bar for each subject and for overall attendance, with a `^` marker showing the target percentage.
- **Colour-Coded Feedback:** Bars are red below the target, yellow from the target up to 5 points above it, and green beyond that.
- **Input Validation:** Reject invalid numbers, negative class counts, empty subject names, attendance counts exceeding the number of classes conducted, and invalid menu or subject selections.
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
2. Enter the number of a preset from the list:
   - **Presets** (e.g. B.Tech CSE) load a fixed set of subjects. You are then asked for the classes conducted and classes attended for each one, with no extra prompts in between.
   - **Custom** lets you enter your own subjects.
3. For custom mode, enter a subject name, the total classes conducted, and the classes attended, then choose whether to add another subject (`y` to continue, anything else to finish).
4. Review the subject-wise attendance report, overall attendance summary, and terminal chart.
5. Use the menu that appears after the report:
   - **1. What-if calculator**
   - **2. Show report again**
   - **3. Exit**

### Using the What-If Calculator

1. Enter the subject numbers separated by commas (for example `1,3,4`), or type `all` to select every subject.
2. Choose a scenario, which is applied to all selected subjects:
   - **1. Skip** the next N classes
   - **2. Attend** the next N classes
3. Enter N, the number of classes.
4. A results table shows each selected subject's attendance before and after, the change, and its new status with a recovery or safe-skip recommendation. An **OVERALL** row shows the combined effect on overall attendance.

The what-if calculator only shows a projection. It does not change your entered attendance data, so you can try as many combinations as you like.

Example output:

```text
Subject               Scenario      Before    After     Change    Status
--------------------------------------------------------------------------------
Calculus              Skip 3         80.00%    69.57%   -10.43%   SHORTAGE ALERT
    -> SHORTAGE! Must attend the NEXT 5 consecutive classes.
Digital Design        Skip 3         90.00%    69.23%   -20.77%   SHORTAGE ALERT
    -> SHORTAGE! Must attend the NEXT 3 consecutive classes.
--------------------------------------------------------------------------------
OVERALL                              86.67%    78.79%    -7.88%   SHORTAGE ALERT
    -> SHORTAGE! Must attend 8 more classes in total (Calculus: 5, Digital Design: 3).
```

### Available Presets

| Preset | Subjects |
| --- | --- |
| B.Tech CSE | Calculus, Digital Design, Web Development, Python, Environmental Science |
| B.Tech ECE | ECE Sub 1 – ECE Sub 5 (placeholder names) |
| Law | Law Sub 1 – Law Sub 5 (placeholder names) |

Presets can be added or changed by editing the `PRESETS` dictionary in `attendance_tracker.py`. For example:

```python
"btech me": ["Subject 1", "Subject 2", "Subject 3"],
```

New presets appear in the numbered menu automatically, and the **Custom** option always stays as the last number.

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

### 5. What-If Scenarios

For each selected subject, the calculator adjusts the class counts and then reruns the same calculations described above:

- **Skip N classes:** conducted becomes $c + N$ and attended stays $a$.
- **Attend N classes:** conducted becomes $c + N$ and attended becomes $a + N$.

The new percentage, status, and recovery or safe-skip recommendation are computed from these projected counts. Subjects that were not selected keep their current values, and the overall figures are recalculated from the combined result.

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
- The menu choice, scenario choice, and what-if subject selection are valid numbers from their lists (subject numbers must be within range and comma separated, or `all`).

The target percentage is a constant (`TARGET_PERCENTAGE`) and must stay strictly between 0 and 100. A value of 100 causes a divide-by-zero error in the recovery calculation, and the program does not check this at runtime.

## Scope and Limitations

- Attendance data is entered manually.
- Data is not saved between program executions, and subjects entered in custom mode are not stored as presets.
- The target attendance percentage is fixed at 75% and is changed by editing `TARGET_PERCENTAGE` in the code.
- The what-if calculator applies the same scenario (skip or attend, and the same N) to all selected subjects in one run.
- Colours use ANSI escape codes and are always printed. Terminals that do not support them may show stray characters instead of colours.
- Attendance recommendations are mathematical estimates and assume the entered class counts are accurate.
- Official university attendance records and attendance policies take precedence over the application's recommendations.

## Learning Outcomes

This project demonstrates practical applications of:

- Python functions and modular programming.
- Conditional statements and loops.
- Menu-driven programs built with loops and numbered choices.
- Input validation and exception handling.
- Mathematical calculations using the `math` module.
- Lists and dictionaries for managing subject data and presets.
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