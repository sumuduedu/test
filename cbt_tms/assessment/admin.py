from django.contrib import admin
from .models import Assessment, AttitudeEvaluation, CompetencyResult, Evidence, PerformanceGuide, ProductRating

admin.site.register(Assessment)
admin.site.register(PerformanceGuide)
admin.site.register(ProductRating)
admin.site.register(AttitudeEvaluation)
admin.site.register(Evidence)
admin.site.register(CompetencyResult)
