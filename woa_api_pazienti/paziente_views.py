from rest_framework import generics, viewsets
from .models import Paziente
from .paziente_serializer import PazienteSerializer, PazienteFullSerializer
from rest_framework.response import Response


class ListPazienteView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Paziente.objects.all()
    serializer_class = PazienteSerializer



class PazienteDetailView(generics.RetrieveAPIView):
    queryset = Paziente.objects.all()
    serializer_class = PazienteFullSerializer


class PazienteViewSet(viewsets.ModelViewSet):
    queryset = Paziente.objects.all()
    serializer_class = PazienteSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PazienteFullSerializer(instance)
        return Response(serializer.data)