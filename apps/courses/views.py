from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import CourseForm
from .models import Course


class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'

    def get_queryset(self):
        return Course.objects.filter(is_published=True)


class StaffOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['admin', 'staff']


class CourseCreateView(LoginRequiredMixin, StaffOnlyMixin, CreateView):
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:list')


class CourseUpdateView(LoginRequiredMixin, StaffOnlyMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:list')


class CourseDeleteView(LoginRequiredMixin, StaffOnlyMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:list')
