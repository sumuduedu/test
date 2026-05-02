from django.contrib import admin

from .models import Activity, Assessment, Course, LearningResource, LessonPlan, Module, StudentGroup, Task


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'nvq_level', 'total_hours', 'module_hours')
    search_fields = ('title', 'code', 'nvq_level')
    list_filter = ('nvq_level',)
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'code', 'duration_hours', 'task_hours')
    search_fields = ('title', 'code', 'course__title')
    list_filter = ('course',)
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'hours')
    search_fields = ('title', 'module__title')


@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'session_number', 'duration_minutes')
    search_fields = ('title', 'task__title')
    inlines = [ActivityInline]


admin.site.register(Activity)
admin.site.register(Assessment)
admin.site.register(LearningResource)
admin.site.register(StudentGroup)
