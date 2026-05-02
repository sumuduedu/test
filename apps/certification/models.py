from django.conf import settings
from django.db import models
from apps.courses.models import Course


class Certificate(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    certificate_no = models.CharField(max_length=80, unique=True)
    issued_at = models.DateField(auto_now_add=True)
    pdf = models.FileField(upload_to='certificates/', blank=True, null=True)
