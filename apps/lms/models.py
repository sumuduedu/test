from django.conf import settings
from django.db import models
from apps.batch.models import Batch


class Content(models.Model):
    CONTENT_TYPES = [('pdf', 'PDF'), ('video', 'Video'), ('link', 'Link')]
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    file = models.FileField(upload_to='content/', blank=True, null=True)
    external_url = models.URLField(blank=True)


class Activity(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
