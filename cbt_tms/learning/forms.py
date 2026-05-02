from django.forms import ModelForm
from .models import Activity, Assignment, LearningResource


class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'


class LearningResourceForm(ModelForm):
    class Meta:
        model = LearningResource
        fields = '__all__'
