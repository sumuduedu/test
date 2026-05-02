from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import CourseForm, LessonPlanForm, ModuleForm
from .models import Course, LessonPlan, Module


@login_required
def course_list(request):
    return render(request, 'courses/course_list.html', {'courses': Course.objects.all()})


@login_required
def course_create(request):
    form = CourseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('course_list')
    return render(request, 'courses/form.html', {'form': form, 'title': 'Create Course'})


@login_required
def module_list(request):
    return render(request, 'courses/module_list.html', {'modules': Module.objects.select_related('course')})


@login_required
def module_create(request):
    form = ModuleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('module_list')
    return render(request, 'courses/form.html', {'form': form, 'title': 'Create Module'})


@login_required
def lesson_plan_list(request):
    lesson_plans = LessonPlan.objects.select_related('module', 'module__course')
    return render(request, 'courses/lesson_plan_list.html', {'lesson_plans': lesson_plans})


@login_required
def lesson_plan_create(request):
    form = LessonPlanForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lesson_plan_list')
    return render(request, 'courses/form.html', {'form': form, 'title': 'Create Lesson Plan'})
