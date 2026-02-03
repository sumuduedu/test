DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS modules;
DROP TABLE IF EXISTS lessonplans;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    duration_months INTEGER NOT NULL,
    days_per_week INTEGER NOT NULL,
    hours_per_day REAL NOT NULL,
    theory_percentage INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    theory_hours REAL NOT NULL,
    practical_hours REAL NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE lessonplans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    week_number INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    topic TEXT NOT NULL,
    theory_hours REAL NOT NULL,
    practical_hours REAL NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

INSERT INTO users (name, role) VALUES
('Admin User', 'Admin'),
('Trainer User', 'Trainer');
