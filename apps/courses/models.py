from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    duration_weeks = models.PositiveIntegerField()
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    letter = models.CharField(max_length=2)
    title = models.CharField(max_length=255)
    details = models.TextField(blank=True)


class CourseOutcome(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='outcomes')
    outcome = models.CharField(max_length=300)

class NCSUnit(models.Model):
    code = models.CharField(max_length=40, unique=True)
    title = models.CharField(max_length=255)
    standard_level = models.CharField(max_length=50)


class Competency(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    ncs_unit = models.ForeignKey(NCSUnit, on_delete=models.CASCADE)
    description = models.TextField()


class Task(models.Model):
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    rubric = models.TextField()


class CompetencyRecord(models.Model):
    STATUS = [('pending', 'Pending'), ('competent', 'Competent'), ('nyc', 'Not Yet Competent')]
    student_id = models.BigIntegerField()
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS, default='pending')
    assessed_on = models.DateField(null=True, blank=True)
