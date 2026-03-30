from django.conf import settings
from django.db import models
from courses.models import Course, LessonPlan


class Batch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='batches')
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='batches_as_trainer')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_on = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='active')

    class Meta:
        unique_together = ('batch', 'student')

    def __str__(self):
        return f"{self.student} in {self.batch}"

    @property
    def attendance_percentage(self):
        sessions = self.batch.sessions.count()
        if sessions == 0:
            return 0
        present = self.attendance_records.filter(status=Attendance.Status.PRESENT).count()
        return round((present / sessions) * 100, 2)


class Timetable(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='timetables')
    day_of_week = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.batch.name} {self.day_of_week}"


class Session(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='sessions')
    lesson_plan = models.ForeignKey(LessonPlan, on_delete=models.PROTECT, related_name='sessions')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    trainer_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.batch} - {self.lesson_plan} - {self.date}"


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        LATE = 'late', 'Late'

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='attendance_records')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attendance')
    status = models.CharField(max_length=10, choices=Status.choices)
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('enrollment', 'session')

    def __str__(self):
        return f"{self.enrollment.student} - {self.session.date} - {self.status}"
