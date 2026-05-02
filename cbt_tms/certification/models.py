from django.db import models
from batches.models import Enrollment


class NVQLevel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Certificate(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    nvq_level = models.ForeignKey(NVQLevel, on_delete=models.PROTECT)
    certificate_no = models.CharField(max_length=100, unique=True)
    issued_on = models.DateField(auto_now_add=True)
    is_eligible = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        competent = self.enrollment.competency_results.filter(status='competent').exists()
        self.is_eligible = competent
        super().save(*args, **kwargs)

    def __str__(self):
        return self.certificate_no
