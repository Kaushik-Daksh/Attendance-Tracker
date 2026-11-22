import math
import os


TARGET_PERCENTAGE = 75.0   # DEFAULT target attendance percentage (must be strictly between 0 and 100)
MAX_CLASSES = 10000        # Upper limit for any class count typed by the user (blocks absurd / overflow values)
MAX_NAME_LENGTH = 20       # Longest allowed subject name (keeps the report tables aligned)


def validate_target(value):
    """Raise ValueError unless value is a real number strictly between 0 and 100.
    0 would make 'safe skips' divide by zero, 100 would make 'required classes' divide by zero."""
    if (isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or not 0 < value < 100):
        raise ValueError("Target percentage must be a number strictly between 0 and 100.")
    return value


validate_target(TARGET_PERCENTAGE)   # checks the default constant once, at start-up

# ANSI colour / style codes for terminal output
RED, YELLOW, GREEN, CYAN = "\033[31m", "\033[33m", "\033[32m", "\033[36m"
BOLD, DIM, RESET = "\033[1m", "\033[2m", "\033[0m"
if os.name == "nt":
    os.system("")   # switches on ANSI colour support in the Windows terminal

# Block characters used to draw the bar chart
FILL_CHAR, EMPTY_CHAR = "\u2588", "\u2591"

# Colour used for each status word in the report
STATUS_COLOURS = {"SAFE": GREEN, "SHORTAGE ALERT": RED, "NO DATA": DIM}

# Preset classes for subjects
PRESETS = {
    "btech cse": [
        "Calculus",
        "Digital Design",
        "Web Development",
        "Python",
        "Environmental Science",
    ],
    "btech ece": [
        "ECE Sub 1",
        "ECE Sub 2",
        "ECE Sub 3",
        "ECE Sub 4",
        "ECE Sub 5",
    ],
    "law": [
        "Law Sub 1",
        "Law Sub 2",
        "Law Sub 3",
        "Law Sub 4",
        "Law Sub 5",
    ],
}


# ---------------------------------------------------------------------------
# COLOUR HELPER
# ---------------------------------------------------------------------------

def paint(text, *styles):
    """Wrap text in colour/style codes. Pad the text BEFORE painting it
    (e.g. paint(f"{x:<12}", CYAN)), because the hidden colour codes would break alignment."""
    return "".join(styles) + str(text) + RESET


# ---------------------------------------------------------------------------
# INPUT HELPERS (every user input goes through one of these, so bad input never crashes the program)
# ---------------------------------------------------------------------------

def read_non_negative_int(prompt, maximum=MAX_CLASSES):
    """Prompt until the user enters an integer between 0 and maximum."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print(paint("Error: Please enter a valid integer.", RED))
            continue
        if value < 0:
            print(paint("Error: Values cannot be negative.", RED))
            continue
        if value > maximum:
            print(paint(f"Error: Value is too large (maximum allowed is {maximum}).", RED))
            continue
        return value


def read_choice(prompt, low, high):
    """Prompt until the user enters an integer between low and high (inclusive)."""
    while True:
        raw = input(prompt).strip()
        if raw.isdecimal() and low <= int(raw) <= high:
            return int(raw)
        print(paint(f"Error: Please enter a number between {low} and {high}.", RED))


def read_yes_no(prompt):
    """Prompt until the user answers y or n. Returns True for yes."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print(paint("Error: Please enter 'y' or 'n'.", RED))


def read_subject_name():
    """Prompt until the user enters a valid subject name."""
    while True:
        name = input("Subject Name: ").strip()
        if not name:
            print(paint("Error: Subject name cannot be empty.", RED))
        elif len(name) > MAX_NAME_LENGTH:
            print(paint(f"Error: Subject name cannot be longer than {MAX_NAME_LENGTH} characters.", RED))
        elif name.casefold() == "overall":
            print(paint("Error: 'OVERALL' is reserved for the total row. Choose another name.", RED))
        else:
            return name


def read_target_percentage(default=TARGET_PERCENTAGE):
    """Prompt until the user enters a target strictly between 0 and 100 (just Enter keeps the default).
    Accepts '80' or '80%'. The value is rounded to 2 decimal places."""
    while True:
        raw = input(f"Enter target attendance % (press Enter to keep {default:g}%): ").strip()
        if raw == "":
            return default
        try:
            value = round(float(raw.rstrip("%").strip()), 2)
        except ValueError:
            print(paint("Error: Please enter a valid number (example: 75 or 80.5).", RED))
            continue
        try:
            return validate_target(value)
        except ValueError:
            print(paint("Error: Target must be strictly between 0 and 100 (0 and 100 themselves are not allowed).", RED))


# ---------------------------------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------------------------------

def graph_colour(percentage, target_percentage=TARGET_PERCENTAGE):    # Defines colour of graph
    """Red below target, yellow from target up to target + 5, green above."""
    if percentage < target_percentage:
        return RED
    if percentage <= target_percentage + 5:
        return YELLOW
    return GREEN


def calculate_attendance(subject_name, conducted, attended, target_percentage=TARGET_PERCENTAGE):
    """Calculate percentage, identify shortage, generate alert, calculate recovery logic and safe margin logic"""
    # Defensive checks: the input functions already prevent these, but the maths must never get bad data
    validate_target(target_percentage)
    if conducted < 0 or attended < 0:
        raise ValueError("Class counts cannot be negative.")
    if attended > conducted:
        raise ValueError("Attended classes cannot exceed conducted classes.")

    # Turn the target into a whole number (2 decimals max): 75.0 -> 7500, 70.1 -> 7010.
    # Doing the maths with integers means float rounding can never make the answer off by one class.
    P = round(target_percentage * 100)
    if not 1 <= P <= 9999:
        raise ValueError("Target percentage is too close to 0 or 100.")

    percentage = (attended / conducted * 100.0) if conducted > 0 else 0.0

    required_classes = 0
    safe_skips = 0

    if conducted == 0:
        status = "NO DATA"
        action = "No classes conducted yet."
    elif attended * 10000 < P * conducted:
        status = "SHORTAGE ALERT"
        # Smallest x such that (a + x) / (c + x) >= P / 10000, using integer ceiling division: -(-a // b)
        required_classes = -(-(P * conducted - 10000 * attended) // (10000 - P))
        action = f"SHORTAGE! Must attend the NEXT {required_classes} consecutive classes."
    else:
        status = "SAFE"
        # Largest x such that a / (c + x) >= P / 10000, using integer floor division: a // b
        safe_skips = (10000 * attended - P * conducted) // P
        if safe_skips == 0:
            action = "On the margin. Do not miss any upcoming classes."
        else:
            action = f"Can safely skip the NEXT {safe_skips} classes."

    return {
        "subject": subject_name,
        "conducted": conducted,
        "attended": attended,
        "percentage": round(percentage, 2),
        "status": status,
        "required_classes": required_classes,
        "safe_skips": safe_skips,
        "action": action,
    }


def calculate_overall(records, target_percentage=TARGET_PERCENTAGE):
    """Overall attendance: percentage, status, recovery and safe skips summed per subject."""
    total_conducted = sum(r["conducted"] for r in records)
    total_attended = sum(r["attended"] for r in records)
    overall = calculate_attendance("OVERALL", total_conducted, total_attended, target_percentage)

    short = [r for r in records if r["status"] == "SHORTAGE ALERT"]

    if short:
        overall["status"] = "SHORTAGE ALERT"
        overall["required_classes"] = sum(r["required_classes"] for r in short)
        overall["safe_skips"] = 0
        breakdown = ", ".join(f"{r['subject']}: {r['required_classes']}" for r in short)
        overall["action"] = f"SHORTAGE! Must attend {overall['required_classes']} more classes in total ({breakdown})."

    elif total_conducted > 0:
        overall["status"] = "SAFE"
        overall["required_classes"] = 0
        overall["safe_skips"] = sum(r["safe_skips"] for r in records)
        if overall["safe_skips"] == 0:
            overall["action"] = "On the margin. Do not miss any upcoming classes."
        else:
            overall["action"] = f"Can safely skip {overall['safe_skips']} classes in total (within each subject's own limit)."
    return overall


def recalculate_records(records, target_percentage):
    """Rebuild every record so status, recovery and safe skips match a new target."""
    return [calculate_attendance(r["subject"], r["conducted"], r["attended"], target_percentage)
            for r in records]


# ---------------------------------------------------------------------------
# REPORT AND CHART
# ---------------------------------------------------------------------------

def print_report_row(item, target_percentage, bold=False):
    """Print one coloured table row (a subject or the OVERALL line) plus its action line.
    Percentage uses the same colour as the chart; status and the '->' arrow use the status colour."""
    status_colour = STATUS_COLOURS[item["status"]]
    name_style = BOLD if bold else ""
    print(paint(f"{item['subject']:<22}", name_style)
          + f"{item['conducted']:<12}"
          + f"{item['attended']:<11}"
          + paint(f"{item['percentage']:>6.2f}%", BOLD, graph_colour(item["percentage"], target_percentage))
          + "      "
          + paint(item["status"], BOLD, status_colour))
    print("    " + paint("->", status_colour) + " " + paint(item["action"], DIM))


def display_attendance_report(records, target_percentage=TARGET_PERCENTAGE):
    """Print a structured summary table, overall percentage, and alert summary."""
    overall = calculate_overall(records, target_percentage)
    width = 80
    print("\n" + paint("=" * width, CYAN))
    print(paint("STUDENT ATTENDANCE TRACKER & RECOVERY REPORT".center(width), BOLD, CYAN))
    print(paint("=" * width, CYAN))
    print(paint(f"{'Subject':<22}{'Conducted':<12}{'Attended':<11}{'Percentage':<13}{'Status'}", BOLD, CYAN))
    print(paint("-" * width, CYAN))

    shortage_list = []

    for item in records:
        print_report_row(item, target_percentage)

        if item["status"] == "SHORTAGE ALERT":
            shortage_list.append(item["subject"])

    print(paint("-" * width, CYAN))
    print_report_row(overall, target_percentage, bold=True)
    print(paint("-" * width, CYAN))

    print(paint("SUMMARY METRICS:", BOLD, CYAN))
    print(f"  Target Threshold       : {paint(f'{target_percentage:g}%', BOLD)}")
    print(f"  Total Subjects Tracked : {paint(len(records), BOLD)}")
    below_colour = RED if shortage_list else GREEN
    print(f"  Subjects Below Target  : {paint(len(shortage_list), BOLD, below_colour)}")

    if shortage_list:
        print(f"  Subjects Needing Action: {paint(', '.join(shortage_list), BOLD, RED)}")
        print(paint("  WARNING: Attendance shortage detected. Follow the recovery plan above.", RED))
    else:
        print(paint("  STATUS: All subjects meet or exceed the target.", GREEN))

    print(paint("=" * width, CYAN) + "\n")
    return overall


def print_graph(records, overall, target_percentage=TARGET_PERCENTAGE, bar_width=40):
    """
    Terminal bar chart (no extra libraries needed).
    Bar colour: red below the target, yellow up to target + 5%, green above.
    '^' underneath marks the target position.
    """
    target_pos = max(0, min(bar_width - 1, round(target_percentage / 100 * bar_width)))
    label_width = MAX_NAME_LENGTH
    print(paint("ATTENDANCE CHART", BOLD, CYAN))
    for item in records + [overall]:
        filled = max(0, min(bar_width, round(item["percentage"] / 100 * bar_width)))
        fill = graph_colour(item["percentage"], target_percentage) + FILL_CHAR * filled + RESET
        bar = fill + EMPTY_CHAR * (bar_width - filled)
        print(f"  {item['subject'][:label_width]:<{label_width}} {bar} "
              f"{item['percentage']:>6.2f}%")
        print()
    marker = [" "] * bar_width
    marker[target_pos] = "^"
    print(f"  {'':<{label_width}} {''.join(marker)} target {target_percentage:g}%")
    print()


# ---------------------------------------------------------------------------
# DATA ENTRY
# ---------------------------------------------------------------------------

def read_subject_data(name, target_percentage=TARGET_PERCENTAGE):
    """Read conducted/attended for one subject and return its record."""
    print(paint(f"\n--- {name} ---", BOLD, CYAN))
    while True:
        conducted = read_non_negative_int(f"Total Classes Conducted for '{name}': ")
        attended = read_non_negative_int(f"Classes Attended for '{name}': ")
        if attended > conducted:
            print(paint("Error: Attended classes cannot exceed total conducted classes.", RED))
            continue
        return calculate_attendance(name, conducted, attended, target_percentage)


def collect_custom_records(target_percentage=TARGET_PERCENTAGE):
    """Custom mode: take one subject's details at a time, then ask whether to add another."""
    records = []
    while True:
        print(paint("\n--- Enter Subject Details ---", BOLD, CYAN))
        name = read_subject_name()

        if any(r["subject"].casefold() == name.casefold() for r in records):
            print(paint("Error: That subject was already entered.", RED))
            continue

        records.append(read_subject_data(name, target_percentage))

        if not read_yes_no("\nAdd another subject? (y/n): "):
            break
    return records


def choose_subjects(presets):
    """Show numbered presets; return the chosen preset's subjects, or None for custom."""
    names = list(presets)
    custom_option = len(names) + 1

    print(paint("\nAvailable presets:", BOLD, CYAN))
    for number, name in enumerate(names, start=1):
        print(f"  {paint(number, BOLD, YELLOW)}. {paint(name.upper(), BOLD)}  ({', '.join(presets[name])})")
    print(f"  {paint(custom_option, BOLD, YELLOW)}. {paint('CUSTOM', BOLD)}  (enter your own subjects)")

    choice = read_choice("\nPlease enter the desired number of the preset: ", 1, custom_option)
    if choice == custom_option:
        return None
    name = names[choice - 1]
    print(paint(f"\nPreset '{name.upper()}' loaded: {len(presets[name])} subjects.", GREEN))
    return presets[name]


# ---------------------------------------------------------------------------
# UPDATE A SUBJECT
# ---------------------------------------------------------------------------

def update_subject(records, target_percentage=TARGET_PERCENTAGE):
    """Pick a subject, then re-enter its total classes conducted and classes attended.
    Changes records in place. Returns True if something was changed."""
    if not records:
        print(paint("\nNo subjects to update.", YELLOW))
        return False

    print(paint("\n--- UPDATE A SUBJECT ---", BOLD, CYAN))
    for number, item in enumerate(records, start=1):
        print(f"  {paint(number, BOLD, YELLOW)}. {item['subject']}  "
              f"(attended {item['attended']}/{item['conducted']}, {item['percentage']:.2f}%)")
    index = read_choice("Enter the subject number: ", 1, len(records)) - 1
    old = records[index]

    # Goes straight to the two questions: total conducted, then attended
    new = read_subject_data(old["subject"], target_percentage)

    if new["conducted"] == old["conducted"] and new["attended"] == old["attended"]:
        print(paint("\nNo change made.", YELLOW))
        return False

    records[index] = new
    new_text = paint(f"{new['percentage']:.2f}%", BOLD, graph_colour(new["percentage"], target_percentage))
    status_text = paint(new["status"], BOLD, STATUS_COLOURS[new["status"]])
    print(f"\n{new['subject']}: {old['percentage']:.2f}% -> {new_text}  ({status_text})")
    print("    " + paint("->", STATUS_COLOURS[new["status"]]) + " " + paint(new["action"], DIM))
    return True


# ---------------------------------------------------------------------------
# WHAT-IF CALCULATOR
# ---------------------------------------------------------------------------

def read_subject_selection(records):
    """Prompt until the user picks one or more subjects ('1,3,4' or 'all'). Returns a list of indexes."""
    total = len(records)
    while True:
        raw = input("\nEnter subject numbers separated by commas (e.g. 1,3,4) or 'all': ").strip().lower()
        if raw == "all":
            return list(range(total))
        parts = [part.strip() for part in raw.split(",") if part.strip()]
        if parts and all(part.isdecimal() and 1 <= int(part) <= total for part in parts):
            indexes = []
            for part in parts:
                index = int(part) - 1
                if index not in indexes:
                    indexes.append(index)
            return indexes
        print(paint(f"Error: Enter valid numbers between 1 and {total} (comma separated), or 'all'.", RED))


def read_scenario(label):
    """Ask for scenario (skip/attend) and N. Returns (scenario, n)."""
    print(f"\nScenario for {label}:")
    print(f"  {paint(1, BOLD, YELLOW)}. SKIP the next N classes")
    print(f"  {paint(2, BOLD, YELLOW)}. ATTEND the next N classes")
    scenario = read_choice("Enter the scenario number: ", 1, 2)
    n = read_non_negative_int("Enter N (number of classes): ")
    return scenario, n


def apply_scenario(record, scenario, n, target_percentage=TARGET_PERCENTAGE):
    """Return the record that results from skipping or attending n more classes."""
    conducted = record["conducted"] + n
    attended = record["attended"] + (n if scenario == 2 else 0)
    return calculate_attendance(record["subject"], conducted, attended, target_percentage)


def print_what_if_row(name, label, before, after, status, action, target_percentage, bold=False):
    """Print one coloured What-If row. The 'Change' column is green if attendance went up, red if down."""
    change = after - before
    change_colour = GREEN if change >= 0 else RED
    status_colour = STATUS_COLOURS[status]
    print(paint(f"{name[:20]:<22}", BOLD if bold else "")
          + f"{label:<14}"
          + f"{before:>6.2f}%   "
          + paint(f"{after:>6.2f}%", BOLD, graph_colour(after, target_percentage)) + "   "
          + paint(f"{change:>+6.2f}%", change_colour) + "   "
          + paint(status, BOLD, status_colour))
    print("    " + paint("->", status_colour) + " " + paint(action, DIM))


def what_if_calculator(records, target_percentage=TARGET_PERCENTAGE):
    """What-if for one or many subjects at once, plus the effect on the overall attendance."""
    if not records:
        print(paint("\nNo subjects to analyse.", YELLOW))
        return

    print(paint("\n--- WHAT-IF CALCULATOR ---", BOLD, CYAN))
    for number, item in enumerate(records, start=1):
        print(f"  {paint(number, BOLD, YELLOW)}. {item['subject']}  ({item['percentage']:.2f}%)")

    selected = read_subject_selection(records)

    # One scenario (skip/attend + N) is applied to every selected subject.
    scenario, n = read_scenario("the selected subjects" if len(selected) > 1 else f"'{records[selected[0]]['subject']}'")

    new_records = list(records)
    for index in selected:
        new_records[index] = apply_scenario(records[index], scenario, n, target_percentage)

    width = 80
    print("\n" + paint("=" * width, CYAN))
    print(paint("WHAT-IF RESULTS".center(width), BOLD, CYAN))
    print(paint("=" * width, CYAN))
    print(paint(f"{'Subject':<22}{'Scenario':<14}{'Before':<10}{'After':<10}{'Change':<10}{'Status'}", BOLD, CYAN))
    print(paint("-" * width, CYAN))
    label = f"{'Skip' if scenario == 1 else 'Attend'} {n}"
    for index in selected:
        before, after = records[index], new_records[index]
        print_what_if_row(before["subject"], label, before["percentage"], after["percentage"],
                          after["status"], after["action"], target_percentage)

    old_overall = calculate_overall(records, target_percentage)
    new_overall = calculate_overall(new_records, target_percentage)
    print(paint("-" * width, CYAN))
    print_what_if_row("OVERALL", "", old_overall["percentage"], new_overall["percentage"],
                      new_overall["status"], new_overall["action"], target_percentage, bold=True)
    print(paint("=" * width, CYAN))


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    """Interactive driver."""
    print(paint("Welcome to the Student Attendance Tracker!", BOLD, CYAN))
    target = read_target_percentage()
    subjects = choose_subjects(PRESETS)

    if subjects is None:
        records = collect_custom_records(target)
    else:
        records = [read_subject_data(name, target) for name in subjects]

    overall = display_attendance_report(records, target)
    print_graph(records, overall, target)

    while True:
        print(paint("\n--- MENU ---", BOLD, CYAN))
        for number, text in enumerate(["What-if calculator", "Show report again", "Update a subject",
                                       "Change target percentage", "Exit"], start=1):
            print(f"  {paint(number, BOLD, YELLOW)}. {text}")
        option = read_choice("Enter your choice: ", 1, 5)
        if option == 1:
            what_if_calculator(records, target)
        elif option == 2:
            overall = display_attendance_report(records, target)   # recalculated every time, never stale
            print_graph(records, overall, target)
        elif option == 3:
            update_subject(records, target)
        elif option == 4:
            target = read_target_percentage(target)
            records = recalculate_records(records, target)   # statuses depend on the target, so rebuild them
            overall = display_attendance_report(records, target)
            print_graph(records, overall, target)
        else:
            print(paint("Goodbye!", GREEN))
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C or closed input stream: exit cleanly instead of showing a traceback
        print("\n\nProgram interrupted. Goodbye!")