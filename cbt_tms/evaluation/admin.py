from django.contrib import admin
from .models import BatchPerformance, Feedback, TrainerEvaluation

admin.site.register(Feedback)
admin.site.register(TrainerEvaluation)
admin.site.register(BatchPerformance)
