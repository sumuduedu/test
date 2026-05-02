from django.contrib import admin
from .models import Attendance, Batch, Enrollment, Session, Timetable

admin.site.register(Batch)
admin.site.register(Enrollment)
admin.site.register(Timetable)
admin.site.register(Session)
admin.site.register(Attendance)
