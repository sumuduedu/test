from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import ActivityForm, AssignmentForm, LearningResourceForm
from .models import Activity, Assignment, LearningResource


@login_required
def activity_list(request):
    return render(request, 'learning/activity_list.html', {'activities': Activity.objects.select_related('session', 'session__batch')})


@login_required
def activity_create(request):
    form = ActivityForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('activity_list')
    return render(request, 'learning/form.html', {'form': form, 'title': 'Add Activity'})


@login_required
def assignment_list(request):
    assignments = Assignment.objects.select_related('enrollment', 'session', 'enrollment__student')
    completion_rate = 0
    if assignments:
        completion_rate = round((assignments.filter(submitted=True).count() / assignments.count()) * 100, 2)
    return render(request, 'learning/assignment_list.html', {'assignments': assignments, 'completion_rate': completion_rate})


@login_required
def assignment_create(request):
    form = AssignmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('assignment_list')
    return render(request, 'learning/form.html', {'form': form, 'title': 'Create Assignment'})


@login_required
def resource_list(request):
    return render(request, 'learning/resource_list.html', {'resources': LearningResource.objects.select_related('session')})


@login_required
def resource_create(request):
    form = LearningResourceForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('resource_list')
    return render(request, 'learning/form.html', {'form': form, 'title': 'Add Learning Resource'})
