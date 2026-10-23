import math

def calculate_attendance_metrics(subject_name, conducted, attended, target_percentage=75.0):
    """
    Core engine addressing Project Objectives:
    1. Percentage Calculation
    2. Shortage Identification (< 75%)
    3. Alert System Generation
    4. Recovery Logic (classes needed to reach 75%)
    5. Safe Margin Logic (classes allowed to skip)
    """
    if conducted <= 0:
        percentage = 0.0
    else:
        percentage = (attended / conducted) * 100.0

    percentage_rounded = round(percentage, 2)

    # Shortage Identification (< 75%)
    if percentage < target_percentage:
        status = "SHORTAGE ALERT"
        # Recovery Logic: ceil(3 * conducted - 4 * attended) for 75% threshold
        required_classes = max(0, math.ceil((0.75 * conducted) - attended) / (1 - 0.75))
        required_classes = math.ceil(required_classes)
        safe_skips = 0
        action = f"⚠️ SHORTAGE! Must attend NEXT {required_classes} consecutive classes."
    else:
        status = "SAFE"
        required_classes = 0
        # Safe Margin Logic: floor((4 * attended - 3 * conducted) / 3) for 75% threshold
        safe_skips = max(0, math.floor((attended - 0.75 * conducted) / 0.75))
        if safe_skips == 0:
            action = " On the margin. Do not miss any upcoming classes."
        else:
            action = f" Can safely skip NEXT {safe_skips} classes."

    return {
        "subject": subject_name,
        "conducted": conducted,
        "attended": attended,
        "percentage": percentage_rounded,
        "status": status,
        "required_classes": required_classes,
        "safe_skips": safe_skips,
        "action": action
    }


def display_attendance_report(records):
    """
    Objective: Clear Output
    Delivers a clean, structured summary table and alert summary.
    """
    print("\n" + "=" * 90)
    print("                    STUDENT ATTENDANCE TRACKER & RECOVERY REPORT                   ")
    print("=" * 90)
    print(f"{'Subject':<20}{'Conducted':<12}{'Attended':<10}{'Percentage':<14}{'Status':<16}{'Action / Guidance'}")
    print("-" * 90)

    shortage_count = 0
    shortage_list = []

    for item in records:
        print(f"{item['subject']:<20}"
              f"{item['conducted']:<12}"
              f"{item['attended']:<10}"
              f"{item['percentage']:>5.1f}%        "
              f"{item['status']:<16}"
              f"{item['action']}")

        if item['percentage'] < 75.0:
            shortage_count += 1
            shortage_list.append(item['subject'])

    print("-" * 90)
    print("SUMMARY METRICS:")
    print(f" Total Subjects Tracked : {len(records)}")
    print(f" Subjects Below 75%     : {shortage_count}")
    
    if shortage_count > 0:
        print(f" Subjects Needing Action: {', '.join(shortage_list)}")
        print(" 🚨 WARNING: Attendance shortage detected. Follow recovery plan above.")
    else:
        print(" 🎉 STATUS: Excellent! All subjects meet or exceed the 75% threshold.")
        
    print("=" * 90 + "\n")


def main():
    """
    Objective: Simple Tracking
    Main interactive driver function.
    """
    print("Welcome to the Student Attendance Tracker!")
    subjects_data = []

    # Interactive input loop
    while True:
        print("\n--- Enter Subject Details ---")
        name = input("Subject Name: ").strip()
        
        while True:
            try:
                conducted = int(input(f"Total Classes Conducted for '{name}': "))
                attended = int(input(f"Classes Attended for '{name}': "))
                
                if conducted < 0 or attended < 0:
                    print("Error: Values cannot be negative.")
                    continue
                if attended > conducted:
                    print("Error: Attended classes cannot exceed total conducted classes.")
                    continue
                break
            except ValueError:
                print("Error: Please enter valid integers.")

        metrics = calculate_attendance_metrics(name, conducted, attended)
        subjects_data.append(metrics)

        more = input("\nAdd another subject? (y/n): ").strip().lower()
        if more != 'y':
            break

    # Objective: Clear Output Display
    display_attendance_report(subjects_data)


if __name__ == "__main__":
    main()