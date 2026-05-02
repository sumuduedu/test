from django import forms
from django.forms import inlineformset_factory

from .models import Activity, Course, LearningResource, LessonPlan, Module, Task


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'code', 'description', 'nvq_level', 'total_hours']


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'code', 'duration_hours', 'learning_outcomes']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'hours']


class LessonPlanForm(forms.ModelForm):
    class Meta:
        model = LessonPlan
        fields = [
            'task', 'title', 'session_number', 'duration_minutes', 'objectives', 'introduction', 'development', 'conclusion'
        ]


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'duration_minutes']


class LearningResourceForm(forms.ModelForm):
    class Meta:
        model = LearningResource
        fields = ['name', 'type', 'file', 'url', 'description']


ModuleFormSet = inlineformset_factory(Course, Module, form=ModuleForm, extra=1, can_delete=True)
TaskFormSet = inlineformset_factory(Module, Task, form=TaskForm, extra=1, can_delete=True)
ActivityFormSet = inlineformset_factory(LessonPlan, Activity, form=ActivityForm, extra=1, can_delete=True)
LearningResourceFormSet = inlineformset_factory(
    LessonPlan, LearningResource, form=LearningResourceForm, extra=1, can_delete=True
)
