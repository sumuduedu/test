from django.db.models import Avg
from assessment.models import CompetencyResult
from batches.models import Attendance, Enrollment
from learning.models import Assignment
from .models import BatchPerformance


def refresh_batch_performance(batch):
    enrollments = Enrollment.objects.filter(batch=batch)
    attendance_rate = 0
    assignments = Assignment.objects.filter(enrollment__batch=batch)
    assignment_rate = 0
    assessments = CompetencyResult.objects.filter(enrollment__batch=batch)
    avg_assessment = assessments.aggregate(avg=Avg('final_score'))['avg'] or 0

    total_sessions = batch.sessions.count() * max(enrollments.count(), 1)
    if total_sessions:
        present = Attendance.objects.filter(enrollment__batch=batch, status=Attendance.Status.PRESENT).count()
        attendance_rate = (present / total_sessions) * 100

    if assignments.exists():
        assignment_rate = (assignments.filter(submitted=True).count() / assignments.count()) * 100

    obj, _ = BatchPerformance.objects.get_or_create(batch=batch)
    obj.attendance_rate = round(attendance_rate, 2)
    obj.assignment_completion_rate = round(assignment_rate, 2)
    obj.avg_assessment_score = round(avg_assessment, 2)
    obj.save()
    return obj
