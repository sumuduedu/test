from django.db import models


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_weeks = models.PositiveIntegerField(default=12)

    def __str__(self):
        return f"{self.code} - {self.title}"


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    sequence = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return f"{self.course.code} / {self.title}"


class LearningOutcome(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='learning_outcomes')
    description = models.TextField()

    def __str__(self):
        return self.description[:80]


class LessonPlan(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lesson_plans')
    title = models.CharField(max_length=255)
    objectives = models.TextField()
    duration_minutes = models.PositiveIntegerField(default=60)
    outcomes = models.ManyToManyField(LearningOutcome, blank=True, related_name='lesson_plans')

    def __str__(self):
        return self.title
