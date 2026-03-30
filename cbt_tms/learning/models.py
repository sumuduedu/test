from django.db import models
from batches.models import Enrollment, Session


class Activity(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class Assignment(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='assignments')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    submitted = models.BooleanField(default=False)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('session', 'enrollment', 'title')

    def __str__(self):
        return self.title


class LearningResource(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='learning_resources')
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=50, default='document')
    link = models.URLField(blank=True)
    file = models.FileField(upload_to='learning_resources/', blank=True)

    def __str__(self):
        return self.title
