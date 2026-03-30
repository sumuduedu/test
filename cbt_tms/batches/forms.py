from django.forms import ModelForm
from .models import Attendance, Batch, Enrollment, Session, Timetable


class BatchForm(ModelForm):
    class Meta:
        model = Batch
        fields = '__all__'


class EnrollmentForm(ModelForm):
    class Meta:
        model = Enrollment
        fields = '__all__'


class TimetableForm(ModelForm):
    class Meta:
        model = Timetable
        fields = '__all__'


class SessionForm(ModelForm):
    class Meta:
        model = Session
        fields = '__all__'


class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'
