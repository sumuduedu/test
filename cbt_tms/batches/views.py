from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import AttendanceForm, BatchForm, EnrollmentForm, SessionForm, TimetableForm
from .models import Batch, Enrollment, Session


@login_required
def batch_list(request):
    batches = Batch.objects.select_related('course', 'trainer')
    return render(request, 'batches/batch_list.html', {'batches': batches})


@login_required
def batch_create(request):
    form = BatchForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('batch_list')
    return render(request, 'batches/form.html', {'form': form, 'title': 'Create Batch'})


@login_required
def enrollment_create(request):
    form = EnrollmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('batch_list')
    return render(request, 'batches/form.html', {'form': form, 'title': 'Enroll Student'})


@login_required
def session_list(request):
    return render(request, 'batches/session_list.html', {'sessions': Session.objects.select_related('batch', 'lesson_plan')})


@login_required
def session_create(request):
    form = SessionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('session_list')
    return render(request, 'batches/form.html', {'form': form, 'title': 'Create Session'})


@login_required
def timetable_create(request):
    form = TimetableForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('batch_list')
    return render(request, 'batches/form.html', {'form': form, 'title': 'Create Timetable'})


@login_required
def attendance_mark(request):
    form = AttendanceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('session_list')
    return render(request, 'batches/form.html', {'form': form, 'title': 'Mark Attendance'})


@login_required
def progress_overview(request):
    enrollments = Enrollment.objects.select_related('student', 'batch')
    return render(request, 'batches/progress_overview.html', {'enrollments': enrollments})
