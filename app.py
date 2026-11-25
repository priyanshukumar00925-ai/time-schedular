"""
app.py - Main Flask Application for Timetable Scheduler

Handles web routing, user form input processing, input validation,
calling the scheduling algorithm, and persisting the timetable to JSON.
"""

import os
import json
from flask import Flask, render_template, request, redirect, url_for
from scheduler import generate_timetable, DAYS, TIME_SLOTS

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATA_FILE = os.path.join(DATA_DIR, 'timetable.json')

MAX_WEEKLY_SLOTS = len(DAYS) * len(TIME_SLOTS)


def load_saved_timetable():
    """
    Safely loads the timetable from data/timetable.json if it exists.
    Returns the timetable dictionary, or None if file doesn't exist or is invalid.
    """
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if data else None
        except (json.JSONDecodeError, IOError):
            return None
    return None


def save_timetable(timetable_data):
    """
    Saves the generated timetable to data/timetable.json with clean formatting.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(timetable_data, f, indent=4)


@app.route('/')
def index():
    """
    Display the initial subject input form page.
    """
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """
    Process form submissions from index.html:
    1. Read subject[], teacher[], classes[] from POST form data.
    2. Validate inputs (non-empty strings, positive integers, capacity checks).
    3. Invoke generate_timetable().
    4. Save result to data/timetable.json.
    5. Render templates/timetable.html with results.
    """
    # Read list data from the form
    subjects = request.form.getlist('subject[]')
    teachers = request.form.getlist('teacher[]')
    classes_list = request.form.getlist('classes[]')

    # Basic check: Was at least one subject submitted?
    if not subjects or len(subjects) == 0:
        return render_template(
            'index.html',
            error="Please provide at least one subject."
        )

    subject_data = []
    total_classes = 0

    # Validate each row submitted
    for idx, (sub, teacher, count_str) in enumerate(zip(subjects, teachers, classes_list), start=1):
        clean_sub = sub.strip()
        clean_teacher = teacher.strip()
        clean_count = count_str.strip()

        # Reject empty subject or teacher names
        if not clean_sub:
            return render_template(
                'index.html',
                error=f"Row {idx}: Subject name cannot be empty."
            )
        if not clean_teacher:
            return render_template(
                'index.html',
                error=f"Row {idx}: Teacher name cannot be empty."
            )

        # Validate class count as positive integer
        if not clean_count:
            return render_template(
                'index.html',
                error=f"Row {idx}: Classes per week is required."
            )

        try:
            class_count = int(clean_count)
            if class_count <= 0:
                return render_template(
                    'index.html',
                    error=f"Row {idx}: Classes per week must be a positive number greater than 0."
                )
        except ValueError:
            return render_template(
                'index.html',
                error=f"Row {idx}: Classes per week must be a valid integer number."
            )

        total_classes += class_count
        subject_data.append({
            "subject": clean_sub,
            "teacher": clean_teacher,
            "classes": class_count
        })

    # Capacity validation: Ensure total requested classes does not exceed available slots
    if total_classes > MAX_WEEKLY_SLOTS:
        return render_template(
            'index.html',
            error=f"Total requested classes ({total_classes}) exceed total weekly available slots ({MAX_WEEKLY_SLOTS}). Please reduce the class count."
        )

    # Generate timetable using the scheduling algorithm
    timetable = generate_timetable(subject_data)

    # Persist the generated timetable into data/timetable.json
    save_timetable(timetable)

    # Display the generated timetable page
    return render_template(
        'timetable.html',
        timetable=timetable,
        days=DAYS,
        time_slots=TIME_SLOTS,
        total_classes=total_classes,
        available_slots=MAX_WEEKLY_SLOTS
    )


@app.route('/timetable')
def view_timetable():
    """
    Optional direct view of the last generated timetable if available.
    """
    saved_data = load_saved_timetable()
    if saved_data:
        # Calculate scheduled classes
        scheduled_count = sum(
            1 for day in DAYS for slot in TIME_SLOTS if saved_data.get(day, {}).get(slot) is not None
        )
        return render_template(
            'timetable.html',
            timetable=saved_data,
            days=DAYS,
            time_slots=TIME_SLOTS,
            total_classes=scheduled_count,
            available_slots=MAX_WEEKLY_SLOTS
        )
    return redirect(url_for('index'))


@app.route('/reset')
def reset():
    """
    Route that redirects user back to the input form.
    """
    return redirect(url_for('index'))


if __name__ == "__main__":
    # Start the Flask development server
    app.run(debug=True)
