from rest_framework import generics
from .models import Paziente
from .paziente_serializer import PazienteSerializer


class ListPazienteView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Paziente.objects.all()
    serializer_class = PazienteSerializer