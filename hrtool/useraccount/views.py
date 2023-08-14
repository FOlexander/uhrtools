from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import PlotFile, ControlPlotFile


# Create your views here.
@login_required
def user_page(request):
    survplot = PlotFile.objects.filter(plot_user=request.user)
    last_model = survplot[len(survplot) - 1]
    print()
    print(last_model.plot_avr_surv)
    data = {'survplot': last_model.plot,
            'Name': last_model.plot_name,
            'Hazard3m': last_model.plot_hazard3m,
            'Hazard6m': last_model.plot_hazard6m,
            'Hazard12m': last_model.plot_hazard12m,
            'AvarageSurvivalb': last_model.plot_avr_surv
            }
    return render(request, 'account.html', data)

