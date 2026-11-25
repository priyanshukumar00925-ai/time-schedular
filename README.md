# Timetable Scheduler

A small Flask web application for generating a weekly college timetable. Enter subjects, teachers, and the number of weekly classes for each subject; the app randomly assigns those classes to available periods and displays the resulting schedule.

## Features

- Add or remove subject rows in the browser.
- Fill the form with sample data for a quick demonstration.
- Validate subject names, teacher names, class counts, and the weekly slot limit.
- Generate a timetable for Monday through Friday, with six periods per day.
- View the most recently saved timetable at `/timetable`.
- Print the timetable or save it as a PDF from the browser.
- Save timetable data as JSON in `data/timetable.json`.

The scheduler randomizes period assignments. It does not model room capacity, teacher availability, or other scheduling constraints.

## Requirements

- Python 3
- Flask (listed in `requirements.txt`)

## Setup and run

From the project directory:

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
# macOS or Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies and start the application:

```bash
pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. The app uses Flask's development server and is intended for local development and demonstrations.

## Using the application

1. Enter a subject name, teacher name, and positive number of classes per week.
2. Use **Add Subject** to add more subjects, or **Fill Sample Data** to populate an example.
3. Select **Generate Timetable**. The requested total must not exceed the 30 available weekly periods.
4. Use **Print / Save PDF** to print or export the displayed schedule.

Generating a new timetable overwrites the saved schedule in `data/timetable.json`.

## Project structure

```text
.
├── app.py                 # Flask routes, input validation, and JSON persistence
├── scheduler.py           # Weekly timetable generation logic
├── data/
│   └── timetable.json     # Saved timetable data
├── static/
│   ├── script.js          # Dynamic form behavior and client-side validation
│   └── style.css          # Application styles
├── templates/
│   ├── index.html         # Subject input form
│   └── timetable.html     # Generated timetable view
└── requirements.txt
```
