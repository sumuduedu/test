from django.conf import settings
from django.db import models
from apps.courses.models import Course


class Batch(models.Model):
    STATUS = [('planned', 'Planned'), ('active', 'Active'), ('completed', 'Completed')]
    name = models.CharField(max_length=120)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='batches_taught')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='batches')
    status = models.CharField(max_length=15, choices=STATUS, default='planned')
