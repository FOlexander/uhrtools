from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="chart_surv.html"), name='chart_surv'),
    path('', TemplateView.as_view(template_name="chart_cont.html"), name='chart_cont'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)