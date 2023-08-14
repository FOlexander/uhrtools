from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class PlotFile(models.Model):
    plot = models.ImageField(upload_to='uploads/', null=True)
    plot_hazard3m = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    plot_hazard6m = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    plot_hazard12m = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    plot_avr_surv = models.CharField (max_length=50)
    plot_name = models.CharField(max_length=20)
    plot_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class ControlPlotFile(models.Model):
    plot = models.ImageField(upload_to='uploads/', null=True)
    plot_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)