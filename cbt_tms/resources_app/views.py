from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import EquipmentForm, LabForm, MaterialForm
from .models import Equipment, Lab, Material


@login_required
def lab_list(request):
    return render(request, 'learning/resource_list.html', {'resources': Lab.objects.all(), 'resource_type': 'Labs'})


@login_required
def lab_create(request):
    form = LabForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lab_list')
    return render(request, 'learning/form.html', {'form': form, 'title': 'Create Lab'})


@login_required
def equipment_create(request):
    form = EquipmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lab_list')
    return render(request, 'learning/form.html', {'form': form, 'title': 'Add Equipment'})


@login_required
def material_create(request):
    form = MaterialForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lab_list')
    return render(request, 'learning/form.html', {'form': form, 'title': 'Add Material'})
