from django.urls import path
from .lookup_views import ListLkpProvinciaView
from .paziente_views import ListPazienteView, PazienteDetailView, PazienteViewSet, PazientiPagedView
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('pazienti', PazienteViewSet, base_name='pazienti')


urlpatterns = [
    path('lkp-province/', ListLkpProvinciaView.as_view(), name="province"),
    #PazientiPagedViewSet.as_view({'get': 'page'})
    url(r'^pazienti/page/(?P<skip>[0-9]+)/(?P<take>[0-9]+)$', PazientiPagedView.as_view(), name='paziente-paged'), 
    # path('pazienti/', ListPazienteView.as_view(), name="pazienti"),
    # url(r'^pazienti/(?P<pk>\d+)$', PazienteDetailView.as_view(), name="paziente-details"),
]

urlpatterns += router.urls
