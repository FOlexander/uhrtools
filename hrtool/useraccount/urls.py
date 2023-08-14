from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('account/', views.user_page, name='account'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)