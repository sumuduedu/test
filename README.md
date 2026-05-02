# CBT-TMS (Competency-Based Training Management System)

A modular Django system for TVET/NVQ institutes using the competency-based training model.

## 1) Project Setup

```bash
cd cbt_tms
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 2) Architecture (Modular Apps)

- `accounts`: Custom user + role-based dashboards.
- `courses`: Course, module, lesson plan, outcomes.
- `batches`: Batch-centric delivery, enrollment bridge, timetable, sessions, attendance.
- `learning`: Activities, assignments, learning resources.
- `assessment`: Competency-based assessment, evidence, final competency result.
- `resources_app`: Labs, equipment, materials.
- `evaluation`: Kirkpatrick level-1 feedback + trainer evaluation + batch analytics.
- `certification`: NVQ levels and certificate generation.

## 3) Core Entity Flow

`Student -> Enrollment -> Batch -> Session -> Assessment -> Competency`

## 4) Built-in Analytics

- Attendance % via `Enrollment.attendance_percentage`
- Assignment completion rate in learning views
- Batch performance metrics in `evaluation/services.py`

## 5) AI-Readiness

The analytics service layer (`evaluation/services.py`) centralizes computed indicators for future predictive models.

## 6) URLs

- `/accounts/` auth + dashboards
- `/courses/` curriculum management
- `/batches/` batch/session/attendance
- `/learning/` activities + assignments + resources
- `/assessment/` competency assessment flow
- `/evaluation/` feedback + batch performance
- `/certification/` certificate management

## Note

`0001_initial.py` files are included per app to keep migration structure in place. After dependency install, run `makemigrations` to generate full schema migrations matching your environment.
