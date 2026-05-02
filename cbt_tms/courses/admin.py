from django.contrib import admin
from .models import Course, LessonPlan, LearningOutcome, Module

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(LessonPlan)
admin.site.register(LearningOutcome)
