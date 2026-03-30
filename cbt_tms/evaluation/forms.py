from django.forms import ModelForm
from .models import Feedback, TrainerEvaluation


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'


class TrainerEvaluationForm(ModelForm):
    class Meta:
        model = TrainerEvaluation
        fields = '__all__'
