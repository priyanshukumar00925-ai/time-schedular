"""
scheduler.py - Core Timetable Generation Algorithm

This module is responsible for defining timetable parameters (Days & Time Slots)
and implementing the random slot allocation algorithm for weekly timetable scheduling.
"""

import random

# List of working days in the college week (Monday to Friday)
DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]

# Standard class time slots per day (6 slots daily = 30 slots/week)
TIME_SLOTS = [
    "09:00 - 10:00",
    "10:00 - 11:00",
    "11:00 - 12:00",
    "12:00 - 01:00",
    "02:00 - 03:00",
    "03:00 - 04:00"
]


def generate_timetable(subjects):
    """
    Generates a weekly timetable by randomly distributing classes for given subjects.

    Algorithm steps:
    1. Initialize an empty timetable grid (Day -> Slot -> None).
    2. Generate all possible (Day, Time Slot) coordinate pairs.
    3. Shuffle the coordinate pairs randomly using Python's random module.
    4. For each subject, pop available slots and assign the subject and teacher.
    5. Return the populated timetable grid.

    :param subjects: List of dicts, e.g. [{"subject": "AI", "teacher": "Dr. Sharma", "classes": 4}]
    :return: Dictionary structured as timetable[day][slot] = {"subject": ..., "teacher": ...} or None
    """
    # 1. Create an empty timetable structure
    # Structure: timetable[Day][TimeSlot] = None initially
    timetable = {day: {slot: None for slot in TIME_SLOTS} for day in DAYS}

    # 2. Create all day/time slot combinations
    # 3. Store available slots as a list of (day, slot) tuples
    available_slots = []
    for day in DAYS:
        for slot in TIME_SLOTS:
            available_slots.append((day, slot))

    # 4. Shuffle available slots randomly
    random.shuffle(available_slots)

    # 5. Iterate through each subject
    for item in subjects:
        subject_name = item.get("subject", "").strip()
        teacher_name = item.get("teacher", "").strip()
        classes_count = int(item.get("classes", 0))

        # 6. Assign the requested number of classes
        for _ in range(classes_count):
            # If no more slots are available in the week, stop assigning
            if not available_slots:
                break

            # Pick a randomized slot from available pool
            day, slot = available_slots.pop()

            # 7. Store the class details inside the timetable
            timetable[day][slot] = {
                "subject": subject_name,
                "teacher": teacher_name
            }

    # 8. Return the completed timetable
    return timetable
