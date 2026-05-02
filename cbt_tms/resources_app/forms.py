from django.forms import ModelForm
from .models import Equipment, Lab, Material


class LabForm(ModelForm):
    class Meta:
        model = Lab
        fields = '__all__'


class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'


class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = '__all__'
