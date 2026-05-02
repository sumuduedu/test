# Training Management System (TMS)

Production-oriented Django scaffold for NVQ/NCS vocational training.

## Features
- Custom user model with role-based access (Admin, Staff, Teacher, Student, Parent, Alumni)
- Authentication with email login
- Course/module/outcome management with publish controls
- Enrollment requests and approval-ready domain models
- Batch, planning, LMS, assessment, certification, alumni/job modules
- NCS/NVQ competency models (unit, competency, task, record)
- Tailwind-based responsive templates and role dashboard

## Run locally
1. Create venv and install dependencies:
   - `pip install django argon2-cffi`
2. Migrate and create superuser:
   - `python manage.py makemigrations`
   - `python manage.py migrate`
   - `python manage.py createsuperuser`
3. Start server:
   - `python manage.py runserver`

## Security notes
- CSRF middleware enabled
- Argon2/PBKDF2 hashers configured
- Session cookies are HTTPOnly
- RBAC via role field + access mixins
- Login throttling setting placeholders provided for extension with middleware/package (e.g. django-axes)
