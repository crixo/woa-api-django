from django.urls import path
from .lookup_views import ListLkpProvinciaView
from .paziente_views import ListPazienteView


urlpatterns = [
    path('lkp-province/', ListLkpProvinciaView.as_view(), name="province"),
    path('pazienti/', ListPazienteView.as_view(), name="pazienti"),
]