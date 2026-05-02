from django.forms import ModelForm
from .models import Course, Module, LessonPlan


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = '__all__'


class LessonPlanForm(ModelForm):
    class Meta:
        model = LessonPlan
        fields = '__all__'
