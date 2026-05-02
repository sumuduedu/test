from django.forms import ModelForm
from .models import Certificate


class CertificateForm(ModelForm):
    class Meta:
        model = Certificate
        fields = '__all__'
