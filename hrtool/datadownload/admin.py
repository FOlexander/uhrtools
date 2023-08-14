from django.contrib import admin
from django.db import models
from .models import UploadedFile, PlotFile, ControlPlotFile

# Register your models here.
admin.site.register(UploadedFile)
admin.site.register(PlotFile)
admin.site.register(ControlPlotFile)
