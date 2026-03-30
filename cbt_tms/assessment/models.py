from django.conf import settings
from django.db import models
from batches.models import Enrollment, Session


class Assessment(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='assessments')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='assessments')
    assessor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='assessments_as_assessor')
    conducted_on = models.DateField(auto_now_add=True)
    comments = models.TextField(blank=True)

    class Meta:
        unique_together = ('enrollment', 'session')

    def __str__(self):
        return f"Assessment {self.enrollment.student} - {self.session}"


class PerformanceGuide(models.Model):
    assessment = models.OneToOneField(Assessment, on_delete=models.CASCADE, related_name='performance_guide')
    checklist_score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    observations = models.TextField(blank=True)


class ProductRating(models.Model):
    assessment = models.OneToOneField(Assessment, on_delete=models.CASCADE, related_name='product_rating')
    quality_score = models.DecimalField(max_digits=5, decimal_places=2)
    standards_met = models.BooleanField(default=False)
    notes = models.TextField(blank=True)


class AttitudeEvaluation(models.Model):
    assessment = models.OneToOneField(Assessment, on_delete=models.CASCADE, related_name='attitude_evaluation')
    punctuality = models.PositiveIntegerField(default=0)
    teamwork = models.PositiveIntegerField(default=0)
    communication = models.PositiveIntegerField(default=0)

    @property
    def average_score(self):
        return (self.punctuality + self.teamwork + self.communication) / 3


class Evidence(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='evidence')
    evidence_type = models.CharField(max_length=50, default='observation')
    note = models.TextField(blank=True)
    file = models.FileField(upload_to='assessment_evidence/', blank=True)
    captured_at = models.DateTimeField(auto_now_add=True)


class CompetencyResult(models.Model):
    class Status(models.TextChoices):
        COMPETENT = 'competent', 'Competent'
        NYC = 'not_yet_competent', 'Not Yet Competent'

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='competency_results')
    assessment = models.OneToOneField(Assessment, on_delete=models.CASCADE, related_name='competency_result')
    final_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NYC)
    decided_on = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        pg = getattr(self.assessment, 'performance_guide', None)
        pr = getattr(self.assessment, 'product_rating', None)
        ae = getattr(self.assessment, 'attitude_evaluation', None)
        performance = float(pg.checklist_score) if pg else 0
        product = float(pr.quality_score) if pr else 0
        attitude = float(ae.average_score * 10) if ae else 0
        self.final_score = round((performance * 0.5) + (product * 0.3) + (attitude * 0.2), 2)
        self.status = self.Status.COMPETENT if self.final_score >= 70 else self.Status.NYC
        super().save(*args, **kwargs)
