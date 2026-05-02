from django.conf import settings
from django.db import models
from apps.batch.models import Batch


class Assignment(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    due_date = models.DateField()


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)


class Assessment(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    max_marks = models.PositiveIntegerField(default=100)


class Result(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    attendance_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
