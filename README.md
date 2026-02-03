# Course & Lesson Planning System

A small Flask-based system to help training institutes create course plans, weekly timetables, and lesson plans with PDF export.

## Features
- Admin can create courses with duration, days/week, and hours/day.
- Automatic weekly timetable generation with theory vs. practical split.
- Trainers can view lesson plans in a structured table.
- Export lesson plans to PDF.

## Tech Stack
- Backend: Flask (Python)
- Frontend: HTML, CSS, Bootstrap
- Database: SQLite

## Project Structure
```
test_project/
├── app.py
├── planner.db (auto-generated)
├── requirements.txt
├── schema.sql
├── static/
│   └── styles.css
└── templates/
    ├── base.html
    ├── create_course.html
    ├── course_detail.html
    └── index.html
```

## Database Schema
The schema is defined in `test_project/schema.sql` and includes:
- Users
- Courses
- Modules
- LessonPlans

## Sample Data
The app includes a sample "Full Stack Bootcamp" course and modules. Use the **Load Sample Data** button on the dashboard or run the `/init-db` route to seed data.

## Setup Instructions
1. **Create a virtual environment (optional):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies:**
   ```bash
   pip install -r test_project/requirements.txt
   ```
3. **Run the app:**
   ```bash
   python test_project/app.py
   ```
4. **Open the app in your browser:**
   ```
   http://localhost:5000
   ```
5. **Initialize the database (if needed):**
   Visit `http://localhost:5000/init-db` or click **Load Sample Data** on the dashboard.

## Notes
- The database file `planner.db` is generated automatically when the app starts.
- PDF export is available from the course detail page.
