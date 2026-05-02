from django.db.models import Prefetch
from django.forms import inlineformset_factory
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from reportlab.pdfgen import canvas

from .forms import ActivityFormSet, CourseForm, LearningResourceFormSet, LessonPlanForm, ModuleFormSet, TaskFormSet
from .models import Course, LessonPlan, Module, Task


class CourseListView(ListView):
    model = Course


class CourseDetailView(DetailView):
    model = Course
    queryset = Course.objects.prefetch_related(
        Prefetch('modules', queryset=Module.objects.prefetch_related('tasks__lesson_plans__activities', 'tasks__lesson_plans__resources'))
    )


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('course_list')


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('course_list')


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('course_list')


class LessonPlanBuilderView(UpdateView):
    model = LessonPlan
    form_class = LessonPlanForm
    template_name = 'lesson_planner/lessonplan_builder.html'

    def get_success_url(self):
        return reverse('course_detail', kwargs={'pk': self.object.task.module.course_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity_formset'] = ActivityFormSet(self.request.POST or None, instance=self.object)
        context['resource_formset'] = LearningResourceFormSet(
            self.request.POST or None, self.request.FILES or None, instance=self.object
        )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        a_formset = context['activity_formset']
        r_formset = context['resource_formset']
        self.object = form.save()
        if a_formset.is_valid() and r_formset.is_valid():
            a_formset.instance = self.object
            r_formset.instance = self.object
            a_formset.save()
            r_formset.save()
            return redirect(self.get_success_url())
        return self.form_invalid(form)


class CourseBuilderWizardView(View):
    template_name = 'lesson_planner/course_builder.html'

    def get(self, request, step=1, pk=None):
        course = Course.objects.filter(pk=pk).first() if pk else None
        return self.render_step(request, step, course)

    def post(self, request, step=1, pk=None):
        course = Course.objects.filter(pk=pk).first() if pk else None
        if step == 1:
            form = CourseForm(request.POST, instance=course)
            if form.is_valid():
                course = form.save()
                return redirect('course_builder', step=2, pk=course.pk)
            return self.render_step(request, step, course, {'form': form})
        if not course:
            return redirect('course_builder', step=1)
        if step == 2:
            formset = ModuleFormSet(request.POST, instance=course)
            if formset.is_valid():
                formset.save()
                first_module = course.modules.first()
                return redirect('course_builder', step=3, pk=first_module.pk if first_module else course.pk)
            return self.render_step(request, step, course, {'formset': formset})
        module = get_object_or_404(Module, pk=pk)
        if step == 3:
            formset = TaskFormSet(request.POST, instance=module)
            if formset.is_valid():
                formset.save()
                task = module.tasks.first()
                return redirect('course_builder', step=4, pk=task.pk if task else module.pk)
            return self.render_step(request, step, course, {'formset': formset, 'module': module})
        task = get_object_or_404(Task, pk=pk)
        form = LessonPlanForm(request.POST)
        if form.is_valid():
            lp = form.save(commit=False)
            lp.task = task
            lp.save()
            return redirect('course_detail', pk=task.module.course_id)
        return self.render_step(request, step, course, {'form': form, 'task': task})

    def render_step(self, request, step, course, extra_context=None):
        context = {'step': step, 'course': course}
        if step == 1:
            context['form'] = (extra_context or {}).get('form') or CourseForm(instance=course)
        elif step == 2 and course:
            context['formset'] = (extra_context or {}).get('formset') or ModuleFormSet(instance=course)
        elif step == 3:
            module = (extra_context or {}).get('module') or Module.objects.filter(pk=course.pk).first()
            context['module'] = module
            context['formset'] = (extra_context or {}).get('formset') or TaskFormSet(instance=module)
        elif step == 4:
            context['task'] = (extra_context or {}).get('task')
            context['form'] = (extra_context or {}).get('form') or LessonPlanForm(initial={'task': context['task']})
        return render(request, self.template_name, context)


def module_options(request, course_id):
    data = list(Module.objects.filter(course_id=course_id).values('id', 'title', 'code'))
    return JsonResponse(data, safe=False)


def task_options(request, module_id):
    data = list(Task.objects.filter(module_id=module_id).values('id', 'title'))
    return JsonResponse(data, safe=False)


def lessonplan_options(request, task_id):
    data = list(LessonPlan.objects.filter(task_id=task_id).values('id', 'title', 'session_number'))
    return JsonResponse(data, safe=False)


class LessonPlanPDFView(View):
    def get(self, request, pk):
        lesson_plan = get_object_or_404(LessonPlan, pk=pk)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="lesson_plan_{pk}.pdf"'
        p = canvas.Canvas(response)
        p.drawString(50, 800, f'Lesson Plan: {lesson_plan.title}')
        p.drawString(50, 780, f'Session: {lesson_plan.session_number}')
        p.drawString(50, 760, f'Duration: {lesson_plan.duration_minutes} minutes')
        p.drawString(50, 740, f'Objectives: {lesson_plan.objectives[:100]}')
        p.showPage()
        p.save()
        return response
