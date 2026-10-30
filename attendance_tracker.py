import math
import os
import sys

TARGET_PERCENTAGE = 75.0

# ANSI colours for the terminal chart (disabled automatically if output is piped)
RED, YELLOW, GREEN, RESET = "\033[31m", "\033[33m", "\033[32m", "\033[0m"
if os.name == "nt":
    os.system("")  # enables ANSI colour support in the Windows console


def colour_for(percentage, target_percentage=TARGET_PERCENTAGE):
    """Red below target, yellow from target up to target + 5, green above."""
    if percentage < target_percentage:
        return RED
    if percentage <= target_percentage + 5:
        return YELLOW
    return GREEN


def calculate_attendance_metrics(subject_name, conducted, attended,
                                 target_percentage=TARGET_PERCENTAGE):
    """
    Core engine:
    1. Percentage calculation
    2. Shortage identification (below target)
    3. Alert generation
    4. Recovery logic (consecutive classes needed to reach target)
    5. Safe margin logic (classes that can be skipped while staying at target)
    """
    p = target_percentage
    if not 0 < p < 100:
        raise ValueError("target_percentage must be between 0 and 100 (exclusive).")

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
        # Largest s such that a / (c + s) >= p / 100
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
    """
    Overall attendance, respecting BOTH rules: the target must hold in every
    subject AND overall.

    - Percentage: total attended / total conducted.
    - Recovery: the sum of each short subject's recovery classes. Once every
      subject is at the target, the overall figure is automatically at the target.
    - Safe skips: the sum of each subject's safe skips, capped by what the overall
      figure can afford. Skipping more than this would break at least one rule.
    """
    total_conducted = sum(r["conducted"] for r in records)
    total_attended = sum(r["attended"] for r in records)
    overall = calculate_attendance_metrics("OVERALL", total_conducted, total_attended,
                                           target_percentage)

    short = [r for r in records if r["status"] == "SHORTAGE ALERT"]

    if short:
        overall["status"] = "SHORTAGE ALERT"
        overall["required_classes"] = sum(r["required_classes"] for r in short)
        overall["safe_skips"] = 0
        breakdown = ", ".join(f"{r['subject']}: {r['required_classes']}" for r in short)
        overall["action"] = (f"SHORTAGE! Must attend {overall['required_classes']} more "
                             f"classes in total ({breakdown}).")
    elif total_conducted > 0:
        overall["status"] = "SAFE"
        overall["required_classes"] = 0
        overall["safe_skips"] = min(sum(r["safe_skips"] for r in records),
                                    overall["safe_skips"])
        if overall["safe_skips"] == 0:
            overall["action"] = "On the margin. Do not miss any upcoming classes."
        else:
            overall["action"] = (f"Can safely skip {overall['safe_skips']} classes in total "
                                 f"(within each subject's own limit).")
    return overall


def print_text_chart(records, overall, target_percentage=TARGET_PERCENTAGE, bar_width=40):
    """
    Terminal bar chart (no extra libraries needed).
    Bar colour: red below the target, yellow up to target + 5%, green above.
    '^' underneath marks the target position.
    """
    use_colour = sys.stdout.isatty()
    target_pos = min(bar_width - 1, round(target_percentage / 100 * bar_width))
    label_width = 14
    print("ATTENDANCE CHART")
    for item in records + [overall]:
        filled = round(item["percentage"] / 100 * bar_width)
        fill = "\u2588" * filled
        if use_colour:
            fill = colour_for(item["percentage"], target_percentage) + fill + RESET
        bar = fill + "\u2591" * (bar_width - filled)
        print(f"  {item['subject'][:label_width]:<{label_width}} {bar} "
              f"{item['percentage']:>6.2f}%")
        print()
    marker = [" "] * bar_width
    marker[target_pos] = "^"
    print(f"  {'':<{label_width}} {''.join(marker)} target {target_percentage:g}%")
    print()


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


def main():
    """Interactive driver."""
    print("Welcome to the Student Attendance Tracker!")
    subjects_data = []

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

        subjects_data.append(calculate_attendance_metrics(name, conducted, attended))

        more = input("\nAdd another subject? (y/n): ").strip().lower()
        if more != "y":
            break

    overall = display_attendance_report(subjects_data)
    print_text_chart(subjects_data, overall)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")