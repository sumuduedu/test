from django.db import models
from apps.batch.models import Batch
from apps.courses.models import Course


class CoursePlan(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    overview = models.TextField()


class Timetable(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=15)
    start_time = models.TimeField()
    end_time = models.TimeField()


class LessonPlan(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    objectives = models.TextField()
