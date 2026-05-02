from django.contrib import admin
from .models import Equipment, Lab, Material

admin.site.register(Lab)
admin.site.register(Equipment)
admin.site.register(Material)
