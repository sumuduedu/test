from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Sum


class Course(models.Model):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    nvq_level = models.CharField(max_length=30)
    total_hours = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.code} - {self.title}"

    @property
    def module_hours(self):
        return self.modules.aggregate(total=Sum('duration_hours'))['total'] or 0


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    code = models.CharField(
        max_length=1,
        validators=[RegexValidator(r'^[A-K]$', 'Module code must be a single letter from A to K.')],
    )
    duration_hours = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    learning_outcomes = models.TextField()

    class Meta:
        unique_together = ('course', 'code')
        ordering = ['course', 'code']

    def __str__(self):
        return f"{self.course.code}-{self.code} {self.title}"

    def clean(self):
        super().clean()
        module_total = self.course.modules.exclude(pk=self.pk).aggregate(total=Sum('duration_hours'))['total'] or 0
        if module_total + (self.duration_hours or 0) > self.course.total_hours:
            raise ValidationError({'duration_hours': 'Total module hours cannot exceed course total hours.'})

    @property
    def task_hours(self):
        return self.tasks.aggregate(total=Sum('hours'))['total'] or 0


class Task(models.Model):
    module = models.ForeignKey(Module, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    hours = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.title


class LessonPlan(models.Model):
    task = models.ForeignKey(Task, related_name='lesson_plans', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    session_number = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    objectives = models.TextField()
    introduction = models.TextField()
    development = models.TextField()
    conclusion = models.TextField()

    class Meta:
        unique_together = ('task', 'session_number')
        ordering = ['task', 'session_number']

    def __str__(self):
        return f"{self.title} (Session {self.session_number})"


class Activity(models.Model):
    lesson_plan = models.ForeignKey(LessonPlan, related_name='activities', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField(validators=[MinValueValidator(1)])


class Assessment(models.Model):
    ASSESSMENT_TYPES = [
        ('Project', 'Project'),
        ('Module', 'Module'),
        ('Competency', 'Competency'),
    ]
    course = models.ForeignKey(Course, related_name='assessments', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=ASSESSMENT_TYPES)
    description = models.TextField()
    criteria = models.TextField()


class LearningResource(models.Model):
    RESOURCE_TYPES = [('File', 'File'), ('URL', 'URL'), ('Video', 'Video')]
    lesson_plan = models.ForeignKey(LessonPlan, related_name='resources', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)


class StudentGroup(models.Model):
    name = models.CharField(max_length=255)
    intake_date = models.DateField()

    def __str__(self):
        return self.name
