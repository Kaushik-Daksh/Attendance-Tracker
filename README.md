# Student Attendance Tracker & Recovery Report

A Python-based attendance tracking tool that helps university students monitor attendance across multiple subjects, identify shortages, calculate recovery requirements, estimate how many upcoming classes they can safely miss, and test "what-if" scenarios while maintaining the required attendance percentage.

Developed as a university group assignment using Python.

## Features

- **Subject Presets or Custom Subjects:** Choose a ready-made subject list (B.Tech CSE, B.Tech ECE, Law) by entering its number, or enter your own subjects one at a time.
- **Custom Target Percentage:** Choose your own target attendance (default 75%) at the start of the program, and change it at any time from the menu. Both `80` and `80%` are accepted.
- **Subject-wise Attendance Tracking:** Calculate attendance percentages for multiple subjects in a single session.
- **Shortage Detection:** Identify subjects that fall below the target attendance threshold.
- **Recovery Planning:** Calculate the minimum number of consecutive classes that must be attended to reach the target percentage.
- **Safe-Skip Estimation:** Estimate how many upcoming classes can be missed without falling below the target.
- **What-If Calculator:** Pick one, several, or all subjects and see how attendance changes if you skip or attend the next N classes, including the effect on overall attendance.
- **Menu-Driven Interface:** After the first report, a menu lets you run the what-if calculator as many times as you like, view the report again, update a subject's data, change the target percentage, or exit.
- **Update Subject Data:** Keep your numbers current during a session by adding newly conducted classes to a subject, or fix a typing mistake by correcting its totals. The report, chart, and recommendations reflect the change.
- **Overall Attendance Analysis:** Calculate overall attendance across all subjects, with a combined recovery or safe-skip recommendation built from the subject-wise results.
- **Colourful Terminal Report:** The title, table headings, percentages, status words, menus, and error messages are all colour-coded, so the report is easy to scan.
- **Terminal Attendance Chart:** Display a progress bar for each subject and for overall attendance, with a `^` marker showing the target percentage.
- **Colour-Coded Feedback:** Bars and table percentages are red below the target, yellow from the target up to 5 points above it, and green beyond that. The status word is green for `SAFE` and red for `SHORTAGE ALERT`.
- **Input Validation:** Reject invalid numbers, negative or absurdly large class counts, empty or too-long subject names, duplicate subject names, attendance counts exceeding the number of classes conducted, invalid target percentages, and invalid menu or subject selections.
- **Summary Report:** Display attendance percentages, shortage alerts, recovery recommendations, and summary metrics.

## Technologies Used

- **Language:** Python 3.8 or newer
- **Standard Library:** `math`, `os`
- **Interface:** Command-line interface (CLI) with ANSI colours

The project uses only Python's standard library and does not require external packages.

## Getting Started

### Prerequisites

- Python 3.8 or newer installed on your computer.
- A terminal or command prompt that supports colours (Windows Terminal / PowerShell, the VS Code terminal, macOS Terminal, or a Linux terminal).

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
2. Enter your target attendance percentage, or press Enter to keep the default of 75%. The target must be strictly between 0 and 100.
3. Enter the number of a preset from the list:
   - **Presets** (e.g. B.Tech CSE) load a fixed set of subjects. You are then asked for the classes conducted and classes attended for each one, with no extra prompts in between.
   - **Custom** lets you enter your own subjects.
4. For custom mode, enter a subject name, the total classes conducted, and the classes attended, then choose whether to add another subject (`y` to continue, `n` to finish).
5. Review the subject-wise attendance report, overall attendance summary, and terminal chart.
6. Use the menu that appears after the report:
   - **1. What-if calculator**
   - **2. Show report again**
   - **3. Update a subject**
   - **4. Change target percentage**
   - **5. Exit**

### Using the What-If Calculator

1. Enter the subject numbers separated by commas (for example `1,3,4`), or type `all` to select every subject.
2. Choose a scenario, which is applied to all selected subjects:
   - **1. Skip** the next N classes
   - **2. Attend** the next N classes
3. Enter N, the number of classes.
4. A results table shows each selected subject's attendance before and after, the change, and its new status with a recovery or safe-skip recommendation. An **OVERALL** row shows the combined effect on overall attendance. The Change column is green when attendance goes up and red when it goes down.

The what-if calculator only shows a projection. It does not change your entered attendance data, so you can try as many combinations as you like. To actually change your data, use **Update a subject** (see below).

Example output (B.Tech CSE preset, skipping the next 4 classes in Calculus and Python):

```text
Subject               Scenario      Before    After     Change    Status
--------------------------------------------------------------------------------
Calculus              Skip 4         86.96%    74.07%   -12.89%   SHORTAGE ALERT
    -> SHORTAGE! Must attend the NEXT 1 consecutive classes.
Python                Skip 4         95.83%    82.14%   -13.69%   SAFE
    -> Can safely skip the NEXT 2 classes.
--------------------------------------------------------------------------------
OVERALL                              89.91%    83.76%    -6.15%   SHORTAGE ALERT
    -> SHORTAGE! Must attend 1 more classes in total (Calculus: 1).
```

### Using Update a Subject

1. Choose **3. Update a subject** from the menu and enter the number of the subject you want to change. The list shows each subject's current attended/conducted counts and percentage.
2. Choose how to update it:
   - **1. Add new classes:** Enter how many new classes were conducted and how many of them you attended. These are added to the existing totals.
   - **2. Correct the totals:** Re-enter the total classes conducted and classes attended from scratch. Use this to fix a typing mistake.
3. The program shows the subject's percentage before and after, with its new status and recovery or safe-skip recommendation. If the numbers did not change, it reports "No change made."

The updated numbers are used for the rest of the session. The what-if calculator works from them, and **Show report again** recalculates the overall attendance and redraws the chart each time.

Example output (Calculus at 15/20 attended, after adding 5 new classes that were all attended):

```text
Calculus: 75.00% -> 80.00%  (SAFE)
    -> Can safely skip the NEXT 1 classes.
```

### Using Change Target Percentage

Choose **4. Change target percentage** from the menu and enter the new target (or press Enter to keep the current one). Every subject is recalculated against the new target, and the report and chart are shown again. Your entered attendance numbers are not changed, only the statuses, recovery numbers, safe-skip numbers, and colours.

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

## What the Colours Mean

| Where | Colour | Meaning |
| --- | --- | --- |
| Chart bars and table percentages | Red | Below the target |
| Chart bars and table percentages | Yellow | At the target, up to 5 points above it (close to the edge) |
| Chart bars and table percentages | Green | More than 5 points above the target |
| Status word | Green `SAFE` | Meets the target |
| Status word | Red `SHORTAGE ALERT` | Below the target, recovery needed |
| Status word | Dim `NO DATA` | No classes conducted yet |
| Title, borders, section headings | Cyan | Structure of the screen |
| Menu numbers | Yellow | Options you can pick |
| Action lines (`->`) | Dim text | Secondary information |
| Error messages | Red | Invalid input |
| What-if "Change" column | Green / Red | Attendance went up / down |

All colouring goes through one small helper, `paint(text, *styles)`, which wraps text in ANSI colour codes. The text is padded to its column width first and painted afterwards, because the hidden colour codes would otherwise break the alignment of the table.

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

The target is converted to a whole number (for example 75% becomes 7500 out of 10000) and both calculations use whole-number maths. This means floating-point rounding can never make the recovery or safe-skip answer off by one class, and the shortage check itself is exact.

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

### 6. Updating a Subject

When a subject is updated, its record is rebuilt and the same calculations described above are rerun:

- **Add new classes:** If $h$ new classes were conducted and $n$ of them were attended (with $n \leq h$), conducted becomes $c + h$ and attended becomes $a + n$.
- **Correct the totals:** The old counts are replaced by the newly entered values (attended cannot exceed conducted).

### 7. Changing the Target

When the target is changed, every subject record is rebuilt from its existing conducted and attended counts using the new target, so statuses, recovery numbers, safe-skip numbers, and colours always match the target currently shown.

## Project Structure

```text
Attendance-Tracker/
├── attendance_tracker.py
└── README.md
```

## Input Validation

The application checks that:

- Subject names are not empty, are at most 20 characters long, are not duplicates of a subject already entered, and are not the reserved name `OVERALL`.
- Class counts are valid non-negative integers, no larger than 10000.
- Attended classes do not exceed the number of classes conducted.
- The preset selection is a valid number from the list.
- The "add another subject" answer is `y`/`yes` or `n`/`no`.
- The menu choice, scenario choice, and what-if subject selection are valid numbers from their lists (subject numbers must be within range and comma separated, or `all`).
- The subject number and update option chosen in **Update a subject** are valid numbers from their lists, the new-class counts are non-negative integers, and attended classes never exceed classes conducted.
- The target percentage is a real number strictly between 0 and 100. 0 and 100 themselves are rejected because they would cause a divide-by-zero in the safe-skip and recovery calculations. The default `TARGET_PERCENTAGE` constant is also checked once when the program starts.

Invalid input shows a red error message and asks again instead of crashing. Pressing Ctrl+C or closing the input stream exits cleanly with a short message.

## Scope and Limitations

- Attendance data is entered manually.
- Data is not saved between program executions, so updates made with **Update a subject** last only for the current session, and subjects entered in custom mode are not stored as presets.
- Subjects cannot be added or removed after the initial entry. Only the numbers of existing subjects can be updated.
- The target attendance percentage can be changed while the program runs, but it is not remembered between runs. The default of 75% is changed permanently by editing `TARGET_PERCENTAGE` in the code.
- Targets are rounded to 2 decimal places.
- The what-if calculator applies the same scenario (skip or attend, and the same N) to all selected subjects in one run.
- Subject names longer than 20 characters are not accepted, and names are cut to 20 characters in the chart labels.
- Colours use ANSI escape codes and are always printed. Terminals that do not support them may show stray characters (such as `[32m`) instead of colours.
- Attendance recommendations are mathematical estimates and assume the entered class counts are accurate.
- Display rounding: A subject at 74.996% shows as 75.00% but is marked SHORTAGE.
- Official university attendance records and attendance policies take precedence over the application's recommendations.

## Learning Outcomes

This project demonstrates practical applications of:

- Python functions and modular programming.
- Conditional statements and loops.
- Menu-driven programs built with loops and numbered choices.
- Input validation and exception handling.
- Mathematical calculations using the `math` module and whole-number (integer) maths.
- Lists and dictionaries for managing subject data and presets.
- Formatted terminal output, ANSI colours, and basic text-based data visualization.
- Git and GitHub for collaborative project development.

## Academic Context

Developed as a university group assignment to apply Python programming concepts to a practical student problem: monitoring attendance and planning how to meet minimum attendance requirements.

## Contributors

- Daksh Kaushik
- Kushagra Garg
- Nidhi Goyal
- Vanshika Gupta
- Gauri Sharma
