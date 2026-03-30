from django.forms import ModelForm
from .models import Assessment, AttitudeEvaluation, CompetencyResult, Evidence, PerformanceGuide, ProductRating


class AssessmentForm(ModelForm):
    class Meta:
        model = Assessment
        fields = '__all__'


class PerformanceGuideForm(ModelForm):
    class Meta:
        model = PerformanceGuide
        fields = '__all__'


class ProductRatingForm(ModelForm):
    class Meta:
        model = ProductRating
        fields = '__all__'


class AttitudeEvaluationForm(ModelForm):
    class Meta:
        model = AttitudeEvaluation
        fields = '__all__'


class EvidenceForm(ModelForm):
    class Meta:
        model = Evidence
        fields = '__all__'


class CompetencyResultForm(ModelForm):
    class Meta:
        model = CompetencyResult
        fields = ['enrollment', 'assessment']
