from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from batches.models import Batch
from .forms import FeedbackForm, TrainerEvaluationForm
from .models import BatchPerformance, Feedback, TrainerEvaluation
from .services import refresh_batch_performance


@login_required
def feedback_list(request):
    return render(request, 'evaluation/feedback_list.html', {'feedback_items': Feedback.objects.select_related('enrollment')})


@login_required
def feedback_create(request):
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('feedback_list')
    return render(request, 'evaluation/form.html', {'form': form, 'title': 'Submit Feedback'})


@login_required
def trainer_evaluation_create(request):
    form = TrainerEvaluationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('feedback_list')
    return render(request, 'evaluation/form.html', {'form': form, 'title': 'Trainer Evaluation'})


@login_required
def batch_performance_dashboard(request):
    for batch in Batch.objects.all():
        refresh_batch_performance(batch)
    performance = BatchPerformance.objects.select_related('batch').all()
    return render(request, 'evaluation/batch_performance.html', {'performance': performance})
