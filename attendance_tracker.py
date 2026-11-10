import math


TARGET_PERCENTAGE = 75.0  #Target attendance percentage ALWAYS keep (0,100) or Error. (100 is divide by zero error)

RED, YELLOW, GREEN, RESET = "\033[31m", "\033[33m", "\033[32m", "\033[0m"  #ANSI color codes for terminal output

def graph_colour(percentage, target_percentage=TARGET_PERCENTAGE):    #Defines colour of graph
    """Red below target, yellow from target up to target + 5, green above."""
    if percentage < target_percentage:
        return RED
    if percentage <= target_percentage + 5:
        return YELLOW
    return GREEN

def calculate_attendance(subject_name, conducted, attended, target_percentage=TARGET_PERCENTAGE):

    """Calculate percentage, identify shortage, generate alert, calculate recovery logic and safe margin logic"""
    #Feeds into records

    p = target_percentage #always keep between 0 and 100
    percentage = (attended / conducted * 100.0) if conducted > 0 else 0.0

    required_classes = 0
    safe_skips = 0

    if conducted == 0:
        status = "NO DATA"
        action = "No classes conducted yet."
    elif attended * 100 < p * conducted:
        status = "SHORTAGE ALERT"
        # Smallest x such that (a + x) / (c + x) >= p / 100
        required_classes = math.ceil((p * conducted - 100 * attended) / (100 - p))
        action = f"SHORTAGE! Must attend the NEXT {required_classes} consecutive classes."

    else:
        status = "SAFE"
        # Largest x such that a / (c + x) >= p / 100
        safe_skips = math.floor((100 * attended - p * conducted) / p)
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
        overall["action"] = (f"SHORTAGE! Must attend {overall['required_classes']} more classes in total ({breakdown}).")

    elif total_conducted > 0:
        overall["status"] = "SAFE"
        overall["required_classes"] = 0
        overall["safe_skips"] = sum(r["safe_skips"] for r in records)
        if overall["safe_skips"] == 0:
            overall["action"] = "On the margin. Do not miss any upcoming classes."
        else:
            overall["action"] = (f"Can safely skip {overall['safe_skips']} classes in total (within each subject's own limit).")
    return overall

def display_attendance_report(records, target_percentage=TARGET_PERCENTAGE):
    """Print a structured summary table, overall percentage, and alert summary."""
    overall = calculate_overall(records, target_percentage)
    width = 80
    print("\n" + "=" * width)
    print("STUDENT ATTENDANCE TRACKER & RECOVERY REPORT".center(width))
    print("=" * width)
    print(f"{'Subject':<22}{'Conducted':<12}{'Attended':<11}{'Percentage':<13}{'Status'}")
    print("-" * width)

    shortage_list = []

    for item in records:
        print(f"{item['subject']:<22}"
              f"{item['conducted']:<12}"
              f"{item['attended']:<11}"
              f"{item['percentage']:>6.2f}%     "
              f"{item['status']}")
        print(f"    -> {item['action']}")

        if item["status"] == "SHORTAGE ALERT":
            shortage_list.append(item["subject"])

    print("-" * width)
    print(f"{'OVERALL':<22}"
          f"{overall['conducted']:<12}"
          f"{overall['attended']:<11}"
          f"{overall['percentage']:>6.2f}%     "
          f"{overall['status']}")
    print(f"    -> {overall['action']}")
    print("-" * width)
    print("SUMMARY METRICS:")
    print(f"  Target Threshold       : {target_percentage:g}%")
    print(f"  Total Subjects Tracked : {len(records)}")
    print(f"  Subjects Below Target  : {len(shortage_list)}")

    if shortage_list:
        print(f"  Subjects Needing Action: {', '.join(shortage_list)}")
        print("  WARNING: Attendance shortage detected. Follow the recovery plan above.")
    else:
        print("  STATUS: All subjects meet or exceed the target.")

    print("=" * width + "\n")
    return overall

def read_non_negative_int(prompt):
    """Prompt until the user enters a non-negative integer."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Error: Please enter a valid integer.")
            continue
        if value < 0:
            print("Error: Values cannot be negative.")
            continue
        return value

def read_subject_name():
    """Prompt until the user enters a non-empty subject name."""
    while True:
        name = input("Subject Name: ").strip()
        if name:
            return name
        print("Error: Subject name cannot be empty.")

def print_graph(records, overall, target_percentage=TARGET_PERCENTAGE, bar_width=40):
    """
    Terminal bar chart (no extra libraries needed).
    Bar colour: red below the target, yellow up to target + 5%, green above.
    '^' underneath marks the target position.
    """
    target_pos = min(bar_width - 1, round(target_percentage / 100 * bar_width))
    label_width = 14
    print("ATTENDANCE CHART")
    for item in records + [overall]:
        filled = round(item["percentage"] / 100 * bar_width)
        fill = graph_colour(item["percentage"], target_percentage) + "\u2588" * filled + RESET
        bar = fill + "\u2591" * (bar_width - filled)
        print(f"  {item['subject'][:label_width]:<{label_width}} {bar} "
              f"{item['percentage']:>6.2f}%")
        print()
    marker = [" "] * bar_width
    marker[target_pos] = "^"
    print(f"  {'':<{label_width}} {''.join(marker)} target {target_percentage:g}%")
    print()

def main():
    """Interactive driver."""
    print("Welcome to the Student Attendance Tracker!")
    records = []

    while True:
        print("\n--- Enter Subject Details ---")
        name = read_subject_name()

        while True:
            conducted = read_non_negative_int(f"Total Classes Conducted for '{name}': ")
            attended = read_non_negative_int(f"Classes Attended for '{name}': ")
            if attended > conducted:
                print("Error: Attended classes cannot exceed total conducted classes.")
                continue
            break

        records.append(calculate_attendance(name, conducted, attended))

        more = input("\nAdd another subject? (y/n): ").strip().lower()
        if more != "y":
            break

    overall = display_attendance_report(records)
    print_graph(records, overall)


if __name__ == "__main__":
    main()