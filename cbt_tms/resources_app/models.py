from django.db import models


class Lab(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=120)
    capacity = models.PositiveIntegerField(default=20)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    title = models.CharField(max_length=120)
    unit = models.CharField(max_length=30, default='pcs')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
