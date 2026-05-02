from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import CertificateForm
from .models import Certificate


@login_required
def certificate_list(request):
    return render(request, 'certification/certificate_list.html', {'certificates': Certificate.objects.select_related('enrollment', 'nvq_level')})


@login_required
def certificate_create(request):
    form = CertificateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('certificate_list')
    return render(request, 'certification/form.html', {'form': form, 'title': 'Generate Certificate'})
