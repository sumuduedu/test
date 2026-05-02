from datetime import datetime
from pathlib import Path
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from fpdf import FPDF

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "planner.db"

app = Flask(__name__)
app.secret_key = "dev-secret"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    schema_path = BASE_DIR / "schema.sql"
    conn = get_db_connection()
    with schema_path.open() as schema_file:
        conn.executescript(schema_file.read())
    conn.commit()
    conn.close()


def seed_sample_data():
    conn = get_db_connection()
    course = conn.execute("SELECT id FROM courses WHERE name = ?", ("Full Stack Bootcamp",)).fetchone()
    if course:
        conn.close()
        return

    conn.execute(
        """
        INSERT INTO courses (name, duration_months, days_per_week, hours_per_day, theory_percentage)
        VALUES (?, ?, ?, ?, ?)
        """,
        ("Full Stack Bootcamp", 3, 5, 3, 60),
    )
    course_id = conn.execute("SELECT id FROM courses WHERE name = ?", ("Full Stack Bootcamp",)).fetchone()[0]

    conn.executemany(
        """
        INSERT INTO modules (course_id, title, description, theory_hours, practical_hours)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (course_id, "Python Fundamentals", "Syntax, data structures, and OOP", 30, 20),
            (course_id, "Web Development", "Flask, templates, and APIs", 25, 25),
            (course_id, "Frontend Essentials", "HTML, CSS, Bootstrap", 20, 25),
        ],
    )

    generate_lesson_plans(conn, course_id)
    conn.commit()
    conn.close()


def generate_lesson_plans(conn, course_id):
    course = conn.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()
    if not course:
        return

    weeks = max(1, course["duration_months"] * 4)
    days_per_week = course["days_per_week"]
    hours_per_day = course["hours_per_day"]
    theory_pct = course["theory_percentage"]

    theory_hours_per_day = round(hours_per_day * (theory_pct / 100), 2)
    practical_hours_per_day = round(hours_per_day - theory_hours_per_day, 2)

    conn.execute("DELETE FROM lessonplans WHERE course_id = ?", (course_id,))

    for week in range(1, weeks + 1):
        for day in range(1, days_per_week + 1):
            topic = f"Week {week} - Day {day}"
            conn.execute(
                """
                INSERT INTO lessonplans (course_id, week_number, day_of_week, topic, theory_hours, practical_hours)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (course_id, week, day, topic, theory_hours_per_day, practical_hours_per_day),
            )


@app.route("/")
def index():
    conn = get_db_connection()
    courses = conn.execute("SELECT * FROM courses ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("index.html", courses=courses)


@app.route("/init-db")
def init_db_route():
    init_db()
    seed_sample_data()
    flash("Database initialized with sample data.")
    return redirect(url_for("index"))


@app.route("/courses/new", methods=["GET", "POST"])
def create_course():
    if request.method == "POST":
        name = request.form["name"].strip()
        duration_months = int(request.form["duration_months"])
        days_per_week = int(request.form["days_per_week"])
        hours_per_day = float(request.form["hours_per_day"])
        theory_percentage = int(request.form["theory_percentage"])

        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO courses (name, duration_months, days_per_week, hours_per_day, theory_percentage)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, duration_months, days_per_week, hours_per_day, theory_percentage),
        )
        course_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        generate_lesson_plans(conn, course_id)
        conn.commit()
        conn.close()

        flash("Course created and lesson plan generated.")
        return redirect(url_for("course_detail", course_id=course_id))

    return render_template("create_course.html")


@app.route("/courses/<int:course_id>")
def course_detail(course_id):
    conn = get_db_connection()
    course = conn.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()
    lessons = conn.execute(
        """
        SELECT * FROM lessonplans
        WHERE course_id = ?
        ORDER BY week_number, day_of_week
        """,
        (course_id,),
    ).fetchall()
    modules = conn.execute(
        "SELECT * FROM modules WHERE course_id = ? ORDER BY id",
        (course_id,),
    ).fetchall()
    conn.close()

    if not course:
        flash("Course not found.")
        return redirect(url_for("index"))

    weeks = max(1, course["duration_months"] * 4)
    total_hours = weeks * course["days_per_week"] * course["hours_per_day"]
    theory_hours = round(total_hours * (course["theory_percentage"] / 100), 2)
    practical_hours = round(total_hours - theory_hours, 2)

    return render_template(
        "course_detail.html",
        course=course,
        lessons=lessons,
        modules=modules,
        weeks=weeks,
        total_hours=total_hours,
        theory_hours=theory_hours,
        practical_hours=practical_hours,
    )


@app.route("/courses/<int:course_id>/export")
def export_lesson_plan(course_id):
    conn = get_db_connection()
    course = conn.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()
    lessons = conn.execute(
        "SELECT * FROM lessonplans WHERE course_id = ? ORDER BY week_number, day_of_week",
        (course_id,),
    ).fetchall()
    conn.close()

    if not course:
        flash("Course not found.")
        return redirect(url_for("index"))

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"Lesson Plan: {course['name']}", ln=True)
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 8, f"Generated on {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(25, 8, "Week", 1)
    pdf.cell(25, 8, "Day", 1)
    pdf.cell(80, 8, "Topic", 1)
    pdf.cell(30, 8, "Theory", 1)
    pdf.cell(30, 8, "Practical", 1, ln=True)

    pdf.set_font("Helvetica", size=10)
    for lesson in lessons:
        pdf.cell(25, 8, str(lesson["week_number"]), 1)
        pdf.cell(25, 8, str(lesson["day_of_week"]), 1)
        pdf.cell(80, 8, lesson["topic"], 1)
        pdf.cell(30, 8, f"{lesson['theory_hours']} h", 1)
        pdf.cell(30, 8, f"{lesson['practical_hours']} h", 1, ln=True)

    export_path = BASE_DIR / f"lesson_plan_{course_id}.pdf"
    pdf.output(str(export_path))
    return send_file(export_path, as_attachment=True)


if __name__ == "__main__":
    if not DB_PATH.exists():
        init_db()
        seed_sample_data()
    app.run(host="0.0.0.0", port=5000, debug=True)
