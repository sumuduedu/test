from django.db import models
from batches.models import Batch, Enrollment


class Feedback(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='feedback')
    reaction_score = models.PositiveIntegerField(default=0)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TrainerEvaluation(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='trainer_evaluations')
    trainer_score = models.PositiveIntegerField(default=0)
    pedagogy_score = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)


class BatchPerformance(models.Model):
    batch = models.OneToOneField(Batch, on_delete=models.CASCADE, related_name='performance')
    attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    assignment_completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    avg_assessment_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Performance: {self.batch.name}"
