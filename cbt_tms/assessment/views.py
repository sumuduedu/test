from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import redirect, render
from .forms import (
    AssessmentForm,
    AttitudeEvaluationForm,
    CompetencyResultForm,
    EvidenceForm,
    PerformanceGuideForm,
    ProductRatingForm,
)
from .models import Assessment, CompetencyResult


@login_required
def assessment_list(request):
    assessments = Assessment.objects.select_related('enrollment', 'session', 'assessor')
    return render(request, 'assessment/assessment_list.html', {'assessments': assessments})


@login_required
def assessment_create(request):
    form = AssessmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('assessment_list')
    return render(request, 'assessment/form.html', {'form': form, 'title': 'Create Assessment'})


def _simple_create(request, form_cls, title, redirect_name='assessment_list'):
    form = form_cls(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect(redirect_name)
    return render(request, 'assessment/form.html', {'form': form, 'title': title})


@login_required
def performance_guide_create(request):
    return _simple_create(request, PerformanceGuideForm, 'Add Performance Guide')


@login_required
def product_rating_create(request):
    return _simple_create(request, ProductRatingForm, 'Add Product Rating')


@login_required
def attitude_evaluation_create(request):
    return _simple_create(request, AttitudeEvaluationForm, 'Add Attitude Evaluation')


@login_required
def evidence_create(request):
    return _simple_create(request, EvidenceForm, 'Add Evidence')


@login_required
def competency_result_create(request):
    return _simple_create(request, CompetencyResultForm, 'Generate Competency Result', 'competency_result_list')


@login_required
def competency_result_list(request):
    results = CompetencyResult.objects.select_related('enrollment', 'assessment')
    avg_score = results.aggregate(avg=Avg('final_score'))['avg'] if results.exists() else None
    return render(request, 'assessment/competency_result_list.html', {'results': results, 'avg_score': avg_score})
